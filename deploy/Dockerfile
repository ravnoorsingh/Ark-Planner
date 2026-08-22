# The ARK Scrapper web app, for the Azure VM.
#
# Runtime only: docs, scripts and tests are not in the repo, and the container never
# needs them. What it does need is the package itself, because `ark.web.app` is
# imported by uvicorn.
FROM python:3.12-slim

# uv resolves and installs from the committed lockfile, so the image matches what was
# tested locally rather than whatever is newest on PyPI today.
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# Dependencies first: this layer is cached until the lockfile changes, so a code-only
# deploy does not reinstall langchain and friends.
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

EXPOSE 8000
CMD ["uv", "run", "--no-dev", "uvicorn", "ark.web.app:app", \
     "--host", "0.0.0.0", "--port", "8000", "--log-level", "warning"]
