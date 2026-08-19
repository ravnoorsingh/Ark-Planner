"""Groq LLM factory plus a structured-output helper.

Why not `with_structured_output()`: Groq's strict `json_schema` response format is
only supported on the `openai/gpt-oss-*` models. Qwen is not on that list. JSON
Object Mode, however, is supported on every Groq model — so we ask for a JSON
object, inject the schema into the prompt ourselves (json_mode guarantees *valid*
JSON, not *your* JSON), and validate with Pydantic, repairing once on failure.
"""

from __future__ import annotations

import asyncio
import json
import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, ValidationError

from .config import Settings
from .tracing import annotate, traced


def build_llm(settings: Settings, *, json_mode: bool = False) -> ChatGroq:
    kwargs: dict = {
        "model": settings.model,
        "api_key": settings.groq_api_key,
        "temperature": settings.temperature,
    }
    if json_mode:
        kwargs["model_kwargs"] = {"response_format": {"type": "json_object"}}
    return ChatGroq(**kwargs)


def _schema_block(schema: type[BaseModel]) -> str:
    return json.dumps(schema.model_json_schema(), indent=2)


_FAILED_GENERATION_KEY = re.compile(r"['\"]failed_generation['\"]\s*:\s*")
_ERROR_TAIL = re.compile(r"['\"]?\s*\}*\s*$")


def _bracket_state(text: str) -> tuple[list[str], bool]:
    """Return (unclosed brackets, whether we ended inside a string literal)."""
    stack: list[str] = []
    in_string = escape = False
    for char in text:
        if escape:
            escape = False
        elif char == "\\":
            escape = True
        elif char == '"':
            in_string = not in_string
        elif not in_string:
            if char == "{":
                stack.append("}")
            elif char == "[":
                stack.append("]")
            elif char in "}]" and stack:
                stack.pop()
    return stack, in_string


@traced("repair_truncated_json", run_type="tool")
def repair_truncated_json(text: str) -> str:
    """Close a JSON document that was cut off mid-generation.

    Groq returns `json_validate_failed` with the partial output in
    `failed_generation` when the response hits the token ceiling. That content was
    already generated and paid for; discarding a plan because its last phase was
    clipped wastes the whole call.
    """
    text = text.strip()
    _, in_string = _bracket_state(text)

    if in_string:
        # Drop the unterminated string, then the incomplete element holding it.
        # Prefer cutting at the last comma: that removes the whole half-written
        # element. Cutting at its opening brace instead would leave `{}` behind,
        # which validates as a real entry and silently invents an empty phase.
        text = text[: text.rfind('"')].rstrip()
        comma = text.rfind(",")
        opener = max(text.rfind("["), text.rfind("{"))
        if comma != -1:
            text = text[:comma]
        elif opener != -1:
            text = text[: opener + 1]

    text = text.rstrip().rstrip(",")
    stack, _ = _bracket_state(text)
    return text + "".join(reversed(stack))


@traced("salvage_partial_json", run_type="tool")
def salvage_partial_json(exc: Exception) -> str | None:
    """Pull the partial JSON out of a `json_validate_failed` error, if present.

    Deliberately tolerant about the envelope around it: the value is a truncated
    JSON document, so it can contain any number of quotes and braces, and anchoring
    on a fixed closing sequence loses the recovery whenever the tail differs.
    Everything after the key is taken, then trimmed back to the JSON.
    """
    text = str(exc)
    match = _FAILED_GENERATION_KEY.search(text)
    if not match:
        return None

    raw = text[match.end() :].strip()
    quote = raw[:1] if raw[:1] in {"'", '"'} else ""
    if quote:
        raw = raw[1:]
        # The envelope quotes with one character and the JSON payload inside uses
        # the other, so the envelope's own closing quote — followed by a comma and
        # the error object's next key — is an unambiguous end marker. Without this,
        # keys after `failed_generation` get swallowed into the payload.
        closing = re.compile(quote + r"\s*,\s*['\"][A-Za-z_][A-Za-z0-9_]*['\"]\s*:")
        end = closing.search(raw)
        if end:
            # Exact boundary found; trimming further would eat the payload's own
            # closing quote and turn a complete string into a truncated one.
            raw = raw[: end.start()]
        else:
            raw = _ERROR_TAIL.sub("", raw)
    else:
        raw = _ERROR_TAIL.sub("", raw)

    start = raw.find("{")
    if start == -1:
        return None
    raw = raw[start:].encode().decode("unicode_escape", errors="ignore")
    return repair_truncated_json(raw)


def _extract_json(text: str) -> str:
    """Pull the JSON object out of a response.

    Reasoning models such as Qwen may wrap output in prose or a ``` fence even in
    JSON mode, so fall back to the outermost braces rather than failing outright.
    """
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.lstrip().startswith("json"):
            text = text.lstrip()[4:]
        text = text.strip()
    if text.startswith("{"):
        return text
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text


# Groq states the wait as "8.415s", but also as "8m37.968s" or "1h2m3s" once the
# window is a daily one — an "([0-9.]+)s" pattern silently misses those.
_RETRY_AFTER_RE = re.compile(
    r"try again in (?:(\d+)h)?(?:(\d+)m)?([0-9.]+)s", re.IGNORECASE
)


def parse_retry_after(text: str) -> float | None:
    """Seconds Groq asked us to wait, or None if it did not say."""
    match = _RETRY_AFTER_RE.search(text)
    if not match:
        return None
    hours, minutes, seconds = match.groups()
    return int(hours or 0) * 3600 + int(minutes or 0) * 60 + float(seconds)


# Long enough for the per-minute token window to move on, short enough that a run
# of eight libraries doesn't stall noticeably.
RETRY_PAUSE = 20.0


def is_truncated_generation(exc: Exception) -> bool:
    """Groq's `json_validate_failed`: the response was cut off mid-JSON.

    Despite the 400 status this is rarely a prompt problem — it happens when the
    per-minute budget runs down partway through a long answer, so the identical
    call succeeds once the window rolls over.
    """
    return "json_validate_failed" in str(exc)


def is_daily_limit(exc: Exception) -> bool:
    """A tokens-per-day cap, as opposed to the per-minute one.

    Worth separating: a per-minute limit clears in seconds and is worth waiting
    out, while a daily cap can be hours away. Retrying that just burns four
    attempts before failing with the same error.
    """
    text = str(exc)
    return "per day" in text or "TPD" in text


def explain_quota(exc: Exception) -> str:
    """Short, actionable text for a rate-limit error.

    Groq's 429 body is ~400 characters of JSON; repeated once per library it buries
    the run's real output in the warnings panel.
    """
    if is_daily_limit(exc):
        wait = parse_retry_after(str(exc))
        when = f" Resets in about {wait / 60:.0f} min." if wait else ""
        return f"Groq daily token quota (TPD) exhausted.{when}"
    if is_too_large(exc):
        return "Request exceeded the per-request token ceiling."
    wait = parse_retry_after(str(exc))
    if wait is not None:
        return f"Groq per-minute token limit; needed {wait:.0f}s of headroom."
    return str(exc)[:160]


class RequestTooLarge(RuntimeError):
    """The prompt exceeds the tier's per-request token ceiling.

    Distinct from a rate limit: waiting cannot help, only sending less can.
    """


def is_too_large(exc: Exception) -> bool:
    """Groq returns 413 for an oversized single request.

    Its body also carries `rate_limit_exceeded`, so this must be checked *before*
    the rate-limit path — otherwise a permanently-too-big prompt gets retried
    several times before failing anyway.
    """
    text = str(exc)
    return "413" in text or "Request too large" in text


def _rate_limit_delay(exc: Exception) -> float | None:
    """Return how long to wait if `exc` is a retryable rate-limit error, else None.

    Groq's 429 body states the exact wait ("Please try again in 8.415s"); honour it
    when present, otherwise back off a fixed amount.
    """
    text = str(exc)
    if is_too_large(exc):
        return None  # shrink the prompt instead — waiting will never help
    if is_daily_limit(exc):
        return None  # hours away; fail now and let the caller say so plainly
    if "rate_limit" not in text and "429" not in text:
        return None
    wait = parse_retry_after(text)
    return wait + 0.5 if wait is not None else 5.0


@traced("groq.invoke", run_type="chain", tags=["groq"])
async def _invoke_with_backoff(llm, messages, attempts: int = 4):
    """Call the model, waiting out Groq's per-minute token limit rather than failing.

    The ChatGroq call inside traces itself through LangChain's callbacks and nests
    under this run; what this span adds is the retry story around it, which is
    invisible from the model call alone.
    """
    for attempt in range(attempts):
        try:
            response = await llm.ainvoke(messages)
            annotate(attempts_used=attempt + 1)
            return response
        except Exception as exc:
            delay = _rate_limit_delay(exc)
            if delay is None or attempt == attempts - 1:
                annotate(attempts_used=attempt + 1, gave_up=explain_quota(exc))
                raise
            annotate(**{f"retry_{attempt + 1}_after_s": delay * (attempt + 1)})
            await asyncio.sleep(delay * (attempt + 1))
    raise AssertionError("unreachable")


@traced("structured", run_type="chain")
async def structured[T: BaseModel](
    llm: ChatGroq,
    schema: type[T],
    system: str,
    user: str,
    *,
    retries: int = 1,
) -> T:
    """Ask the model for JSON matching `schema`, repairing up to `retries` times."""
    system_prompt = (
        f"{system}\n\n"
        "Respond with a single JSON object and nothing else — no prose, no markdown "
        "fence. It must validate against this JSON Schema:\n"
        f"{_schema_block(schema)}"
    )
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user)]
    annotate(schema=schema.__name__, model=getattr(llm, "model_name", ""))

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            response = await _invoke_with_backoff(llm, messages)
        except Exception as exc:
            # The model may have produced most of a valid answer before running out
            # of output budget. Recover it rather than paying for the call twice.
            partial = salvage_partial_json(exc)
            if partial is not None:
                try:
                    validated = schema.model_validate_json(partial)
                    annotate(salvaged_from_truncation=True, attempt=attempt + 1)
                    return validated
                except (ValidationError, ValueError):
                    pass  # unusable; fall through to a retry

            # A truncated generation is usually contention, not a bad prompt: the
            # per-minute budget ran down mid-response, so the same call often
            # succeeds moments later. Spend a retry before giving up.
            if partial is None and not is_truncated_generation(exc):
                raise
            if attempt == retries:
                raise
            last_error = exc
            await asyncio.sleep(RETRY_PAUSE)
            continue

        raw = response.content if isinstance(response.content, str) else str(response.content)
        candidate = _extract_json(raw)
        try:
            return schema.model_validate_json(candidate)
        except (ValidationError, ValueError) as exc:
            last_error = exc
            annotate(**{f"repair_attempt_{attempt + 1}": str(exc)[:300]})
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user),
                HumanMessage(
                    content=(
                        "Your previous reply was not valid for the schema:\n"
                        f"{exc}\n\nReturn corrected JSON only."
                    )
                ),
            ]

    raise ValueError(f"Model did not return schema-valid JSON for {schema.__name__}: {last_error}")
