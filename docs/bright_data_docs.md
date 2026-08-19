> ## Documentation Index
> Fetch the complete documentation index at: https://docs.brightdata.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Bright Data Scraper Studio API quickstart

> Trigger a published Bright Data Scraper Studio collector and download structured JSON in three steps. Copy-paste examples in cURL, Node.js and Python.

This guide sends your first request to the Bright Data Scraper Studio API: trigger a published collector from your own code and get structured JSON back.

<Note>
  **No collector yet?** A collector is the published scraper you trigger here. Build one in minutes, then come back with its Collector ID (`c_...`):

  * **Fastest, from your terminal or coding agent:** [Build a scraper with the Bright Data CLI](/datasets/scraper-studio/build-with-the-cli). Three commands; the AI Agent writes the scraper. Runs as-is inside Claude Code, Cursor or Codex.
  * **No code, in the control panel:** [Build a scraper with the AI Agent](/datasets/scraper-studio/ai-agent).
  * **Full control:** [Build a scraper in the IDE](/datasets/scraper-studio/develop-a-scraper).

  This quickstart picks up once you have a Collector ID.
</Note>

The Bright Data Scraper Studio API is built around two HTTP calls:

1. `POST /dca/trigger`, which queues one or more inputs and returns a snapshot ID.
2. `GET /dca/dataset?id=<snapshot_id>`, which serves the snapshot once it is ready.

<Tip>
  Typical time to first record is about three minutes for a collector with one to ten inputs.
</Tip>

## Prerequisites

* An active [Bright Data account](https://brightdata.com/?hs_signup=1\&utm_source=docs) with a payment method on file
* An **API token** from [Account Settings → API Tokens](https://brightdata.com/cp/setting)
* A **Collector ID** from a scraper you built with the [CLI](/datasets/scraper-studio/build-with-the-cli), [AI Agent](/datasets/scraper-studio/ai-agent) or [IDE](/datasets/scraper-studio/develop-a-scraper); the ID starts with `c_`

Set both values as environment variables once and reuse them across every snippet below:

```bash theme={null}
export BRIGHT_DATA_API_TOKEN="your_api_token_here"
export BRIGHT_DATA_COLLECTOR_ID="c_xxxxxxxxxxxxxxxx"
```

## Make your first request

<Steps>
  <Step title="Authenticate every call">
    Every Bright Data Scraper Studio API call uses bearer-token authentication. Add this header to every request:

    ```http theme={null}
    Authorization: Bearer YOUR_BRIGHT_DATA_API_TOKEN
    ```

    A missing or invalid token returns `401 Unauthorized`.
  </Step>

  <Step title="Trigger your collector">
    Send the inputs you want the collector to process as a JSON array in the request body. Each object in the array must match the input schema you defined when you built the collector. The default schema is a single `url` field.

    <CodeGroup>
      ```bash cURL theme={null}
      curl -X POST \
        "https://api.brightdata.com/dca/trigger?collector=$BRIGHT_DATA_COLLECTOR_ID&queue_next=1" \
        -H "Authorization: Bearer $BRIGHT_DATA_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '[
          {"url": "https://ecommerce-shop-brd.vercel.app/product/echo-portable-speaker"},
          {"url": "https://ecommerce-shop-brd.vercel.app/product/nimbus-cloud-storage"}
        ]'
      ```

      ```python Python theme={null}
      import os
      import requests

      API_TOKEN    = os.environ["BRIGHT_DATA_API_TOKEN"]
      COLLECTOR_ID = os.environ["BRIGHT_DATA_COLLECTOR_ID"]

      response = requests.post(
          f"https://api.brightdata.com/dca/trigger?collector={COLLECTOR_ID}&queue_next=1",
          headers={
              "Authorization": f"Bearer {API_TOKEN}",
              "Content-Type": "application/json",
          },
          json=[
              {"url": "https://ecommerce-shop-brd.vercel.app/product/echo-portable-speaker"},
              {"url": "https://ecommerce-shop-brd.vercel.app/product/nimbus-cloud-storage"},
          ],
      )
      response.raise_for_status()
      snapshot_id = response.json()["collection_id"]
      print(snapshot_id)  # j_abc123def456
      ```

      ```js Node.js theme={null}
      const triggerUrl =
        `https://api.brightdata.com/dca/trigger` +
        `?collector=${process.env.BRIGHT_DATA_COLLECTOR_ID}&queue_next=1`;

      const response = await fetch(triggerUrl, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.BRIGHT_DATA_API_TOKEN}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify([
          { url: "https://ecommerce-shop-brd.vercel.app/product/echo-portable-speaker" },
          { url: "https://ecommerce-shop-brd.vercel.app/product/nimbus-cloud-storage" },
        ]),
      });

      const { collection_id: snapshotId } = await response.json();
      console.log(snapshotId); // j_abc123def456
      ```
    </CodeGroup>

    The Bright Data Scraper Studio API responds with a single snapshot ID:

    ```json theme={null}
    {
      "collection_id": "j_abc123def456"
    }
    ```

    Keep this ID. You will use it as the `snapshot_id` in step 3.

    <Note>
      `queue_next=1` runs your inputs immediately. Omit it (or set `0`) to enqueue them behind any in-flight work for the same collector.
    </Note>
  </Step>

  <Step title="Poll until ready, then download">
    The same `/dca/dataset` endpoint serves both the in-progress and ready responses. Poll it every five seconds until the response is a JSON array.

    <CodeGroup>
      ```bash cURL theme={null}
      # Poll every 5 seconds until the response is a JSON array (not an object).
      while :; do
        response=$(curl -s \
          "https://api.brightdata.com/dca/dataset?id=$SNAPSHOT_ID" \
          -H "Authorization: Bearer $BRIGHT_DATA_API_TOKEN")
        if [[ "${response:0:1}" == "[" ]]; then
          echo "$response" > results.json
          break
        fi
        sleep 5
      done
      ```

      ```python Python theme={null}
      import json
      import time

      while True:
          response = requests.get(
              f"https://api.brightdata.com/dca/dataset?id={snapshot_id}",
              headers={"Authorization": f"Bearer {API_TOKEN}"},
          )
          response.raise_for_status()
          body = response.json()
          if isinstance(body, list) and body:
              with open("results.json", "w") as f:
                  json.dump(body, f, indent=2)
              break
          time.sleep(5)
      ```

      ```js Node.js theme={null}
      const datasetUrl =
        `https://api.brightdata.com/dca/dataset?id=${snapshotId}`;

      while (true) {
        const response = await fetch(datasetUrl, {
          headers: { Authorization: `Bearer ${process.env.BRIGHT_DATA_API_TOKEN}` },
        });
        const body = await response.json();
        if (Array.isArray(body) && body.length > 0) {
          await fs.writeFile("results.json", JSON.stringify(body, null, 2));
          break;
        }
        await new Promise((r) => setTimeout(r, 5000));
      }
      ```
    </CodeGroup>

    While the snapshot is building, the response is a status object:

    ```json theme={null}
    { "status": "building" }
    ```

    When the snapshot is ready, the response is a JSON array. One row per successful input by default:

    ```json theme={null}
    [
      {
        "url": "https://ecommerce-shop-brd.vercel.app/product/echo-portable-speaker",
        "title": "Echo Portable Speaker",
        "price": 49.99,
        "availability": "in stock",
        "input": { "url": "https://ecommerce-shop-brd.vercel.app/product/echo-portable-speaker" }
      },
      {
        "url": "https://ecommerce-shop-brd.vercel.app/product/nimbus-cloud-storage",
        "title": "Nimbus Cloud Storage",
        "price": 12.99,
        "availability": "in stock",
        "input": { "url": "https://ecommerce-shop-brd.vercel.app/product/nimbus-cloud-storage" }
      }
    ]
    ```

    The exact field set depends on the output schema you defined when you built the collector.
  </Step>
</Steps>

## How long does this take?

The first record usually arrives within a minute, but total time depends on the collector and the target site. Measured against a typical e-commerce product page collector:

| Input count    | Typical wall-clock time                                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1 to 10 URLs   | 30 to 90 seconds                                                                                                               |
| 11 to 100 URLs | 2 to 5 minutes                                                                                                                 |
| 100+ URLs      | 5+ minutes. Use [push delivery](/api-reference/scraper-studio-api/Choose_a_delivery_type_on_request_level) instead of polling. |

For long-running jobs, swap polling for a [push delivery destination](/api-reference/scraper-studio-api/Choose_a_delivery_type_on_request_level) (webhook, S3, GCS, Azure, SFTP or email) so Bright Data calls you when the snapshot is ready.

## What do the IDs mean?

Three identifiers appear in Bright Data Scraper Studio. They are easy to confuse because the trigger response uses one name for a value that another endpoint reads under a different name.

| Term                                            | Looks like           | What it identifies                                                                                                                                                     |
| ----------------------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Collector ID**                                | `c_xxxxxxxxxxxxxxxx` | The published scraper definition. Stable. You pass it as the `collector` query parameter on `/dca/trigger`.                                                            |
| **Collection ID** (returned as `collection_id`) | `j_xxxxxxxxxxxxxxxx` | One run of the collector. The trigger response field is `collection_id`, but every other endpoint refers to the same value as `snapshot_id`. They are the same string. |
| **Dataset**                                     | a JSON array         | The result rows produced by one run. The `/dca/dataset` endpoint returns this when the run is finished.                                                                |

<Tip>
  Treat `collection_id` from the trigger response as your `snapshot_id` everywhere else. They are the same value under two names.
</Tip>

## What errors might I see?

| Status                     | Meaning                                                                    | Fix                                                                                                                                 |
| -------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `401 Unauthorized`         | Token missing, malformed or revoked                                        | Re-copy from [Account Settings → API Tokens](https://brightdata.com/cp/setting)                                                     |
| `404 Not Found`            | Collector ID does not exist or your account does not have access           | Open the collector in [Scraper Studio](https://brightdata.com/cp/scrapers) and re-copy the ID                                       |
| `422 Unprocessable Entity` | The objects in your request body do not match the collector's input schema | Confirm field names against the **Inputs** tab of your collector                                                                    |
| `5xx`                      | Transient Bright Data API error                                            | Retry with exponential backoff, for example 1s, 2s, 4s                                                                              |
| `[]` (empty array)         | Snapshot has no rows, or the snapshot expired                              | Batch results are retained for 16 days, real-time results for 7 days. See [Specifications](/datasets/scraper-studio/specifications) |

## Use a production-grade starter template

These open-source repositories are exactly the calls above, hardened with environment-variable config, retry/backoff for transient failures, library helpers and a complete `README`. Fork either and you have a runnable client in 30 seconds.

<CardGroup cols={2}>
  <Card title="Node.js starter" icon="node-js" href="https://github.com/brightdata/bright-data-scraper-studio-nodejs-project">
    Node 18+, ES modules, dotenv, retry/backoff, \~150 LOC
  </Card>

  <Card title="Python starter" icon="python" href="https://github.com/brightdata/bright-data-scraper-studio-python-project">
    Python 3.8+, `requests`, `python-dotenv`, retry/backoff, \~150 LOC
  </Card>
</CardGroup>

Both repositories ship with a CodeSandbox devcontainer so you can fork and run in your browser without any local setup.

## Next steps

<CardGroup cols={2}>
  <Card title="Choose a delivery type" icon="paper-plane" href="/api-reference/scraper-studio-api/Choose_a_delivery_type_on_request_level">
    Skip polling. Have Bright Data push results to a webhook, S3, GCS or email when the snapshot is ready.
  </Card>

  <Card title="Trigger a batch collection" icon="layer-group" href="/api-reference/scraper-studio-api/Trigger_a_scraper_for_batch_collection_method">
    Send hundreds or thousands of inputs in a single request and receive results in batches.
  </Card>

  <Card title="Run a synchronous real-time job" icon="bolt" href="/api-reference/scraper-studio-api/initiate-a-realtime-job/sync-realtime-job">
    For low-input, latency-sensitive workloads. Trigger and receive results in a single HTTP call.
  </Card>

  <Card title="Build a new collector" icon="screwdriver-wrench" href="/datasets/scraper-studio/build-with-the-cli">
    Need a collector that does not exist yet? Build one with the CLI, the AI Agent or the IDE.
  </Card>
</CardGroup>

## Frequently asked questions

<AccordionGroup>
  <Accordion title="How do I create the collector in the first place?">
    Build a Scraper Studio scraper with any of three paths, then use the Collector ID (`c_...`) it returns here:

    * [**Bright Data CLI**](/datasets/scraper-studio/build-with-the-cli) is the fastest. Run `bdata scraper create <url> "<what to extract>"` and the AI Agent writes the scraper. The CLI runs as-is inside Claude Code, Cursor or Codex.
    * [**AI Agent**](/datasets/scraper-studio/ai-agent) builds the scraper from a natural-language prompt in the control panel, no code required.
    * [**IDE**](/datasets/scraper-studio/develop-a-scraper) gives you full control over the scraper code.
  </Accordion>

  <Accordion title="What is the difference between the Collection API and the AI Flow API?">
    The **Collection API** (`/dca/*`, this page) runs an existing collector to **get data**. The [**AI Flow API**](/api-reference/scraper-studio-api/ai-flow/overview) runs the AI Agent to **create or self-heal** a collector. Most developers integrating Bright Data Scraper Studio into a product use the Collection API.
  </Accordion>

  <Accordion title="Can I send different input shapes in the same request?">
    Yes, as long as every object in the array conforms to the collector's input schema. If your collector accepts both `url` and `keyword` as input fields, you can mix them in one request. Fields you do not include are treated as `null`.
  </Accordion>

  <Accordion title="How do I retry failed inputs of batch job without re-running the successful ones?">
    Open **My Scrapers**, select the relevant scraper, and go to the **Runs** tab. Find the failed batch job, click the three-dot actions menu on the job row, and select **Rerun job**.

    Choose **Rerun failed pages** to retry only the failed pages, or **Rerun all from beginning** to run all original inputs again.

    For API workflows, use the [**<u>Rerun job API</u>**](https://docs.brightdata.com/api-reference/scraper-studio-api/rerun-job) with the `failed_only` option.

    Only jobs whose data has not expired can be rerun.
  </Accordion>

  <Accordion title="Is there a rate limit?">
    Yes. Per-account concurrency limits apply per collector. See [Specifications](/datasets/scraper-studio/specifications) for current limits. The starter templates linked above already implement exponential backoff for transient `5xx` responses.
  </Accordion>
</AccordionGroup>