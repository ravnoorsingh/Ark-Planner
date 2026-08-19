---
library: "openai"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction, LangChain for the retrieval chain, ChromaDB for storage, and Pydantic models for request and response validation. Include streaming responses and health checks. Use openai for the embedding model."
url: "https://developers.openai.com/api/docs"
role: "primary"
rank: 0
fetched_at: "2026-08-18T08:56:29.063258+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "7ee6e72224a4329d7105816074bf9c87b2001d0654f70aa90d1bb0bc00356365"
---

# API Platform

## Developer quickstart

Make your first API request in minutes. Learn the basics of the OpenAI platform.

[Get started](/api/docs/quickstart)   [Create API key](https://platform.openai.com/api-keys)

JavaScript

```
1234567
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-5.6",
    "input": "Write a short bedtime story about a unicorn."
  }'
```

```
123456789
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5.6",
  input: "Write a short bedtime story about a unicorn.",
});

console.log(response.output_text);
```

```
1234567
from openai import OpenAI

client = OpenAI()

response = client.responses.create(model="gpt-5.6", input="Write a short bedtime story about a unicorn.")

print(response.output_text)
```

```
12345678910111213141516171819202122232425
package main

import (
	"context"
	"fmt"

	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/responses"
)

func main() {
	client := openai.NewClient()

	response, err := client.Responses.New(context.Background(), responses.ResponseNewParams{
		Model: "gpt-5.6",
		Input: responses.ResponseNewParamsInputUnion{
			OfString: openai.String("Write a short bedtime story about a unicorn."),
		},
	})
	if err != nil {
		panic(err)
	}

	fmt.Println(response.OutputText())
}
```

```
1234567891011121314151617181920
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

public class PlatformOverviewExample {
  public static void main(String[] args) {
    OpenAIClient client = OpenAIOkHttpClient.fromEnv();

    ResponseCreateParams params =
        ResponseCreateParams.builder().model("gpt-5.6").input("Write a short bedtime story about a unicorn.").build();

    Response response = client.responses().create(params);
    response.output().stream()
        .flatMap(item -> item.message().stream())
        .flatMap(message -> message.content().stream())
        .flatMap(content -> content.outputText().stream())
        .forEach(outputText -> System.out.println(outputText.text()));
  }
}
```

```
123456789101112
using OpenAI.Responses;
#pragma warning disable OPENAI001

string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
ResponsesClient client = new(key);

ResponseResult response = await client.CreateResponseAsync(
    "gpt-5.6",
    "Write a short bedtime story about a unicorn."
);

Console.WriteLine(response.GetOutputText());
```

```
12345678910
require "openai"

openai = OpenAI::Client.new

response = openai.responses.create(
  model: "gpt-5.6",
  input: "Write a short bedtime story about a unicorn."
)

puts(response.output_text)
```

```
12345
openai responses create \
  --model gpt-5.6 \
  --input "Write a short bedtime story about a unicorn." \
  --raw-output \
  --transform 'output.#(type=="message").content.0.text'
```

## Build paths

[### Responses API

Make direct model requests for text, structured output, tools, and multimodal workflows.

 Start with Responses](/api/docs/guides/text)  [### Agents SDK

Build code-first agents that orchestrate tools, handoffs, approvals, tracing, and container-based execution.

 Start with the Agents SDK](/api/docs/guides/agents/quickstart)

## Models

Start with  GPT-5.6 Sol  for complex reasoning and coding, choose  GPT-5.6 Terra  to balance intelligence and cost, or use  GPT-5.6 Luna  for cost-sensitive, high-volume workloads.

[View all](/api/docs/models)

[GPT-5.6 Sol

Frontier model for complex professional work](/api/docs/models/gpt-5.6-sol)

[GPT-5.6 Terra

GPT-5.6 model that balances intelligence and cost](/api/docs/models/gpt-5.6-terra)

[GPT-5.6 Luna

GPT-5.6 model optimized for cost-sensitive workloads](/api/docs/models/gpt-5.6-luna)

## Start building

[Read and generate text

Use the API to prompt a model and generate text](/api/docs/guides/text) [Use a model's vision capabilities

Allow models to see and analyze images in your application](/api/docs/guides/images-vision) [Generate images as output

Create images with GPT Image 2](/api/docs/guides/image-generation) [Build apps with audio

Analyze, transcribe, and generate audio with API endpoints](/api/docs/guides/audio) [Build agentic applications

Use the API to build agents that use tools and computers](/api/docs/guides/agents) [Achieve complex tasks with reasoning

Use reasoning models to carry out complex tasks](/api/docs/guides/reasoning) [Get structured data from models

Use Structured Outputs to get model responses that adhere to a JSON schema](/api/docs/guides/structured-outputs) [Tailor to your use case

Adjust our models to perform specifically for your use case with fine-tuning, evals, and distillation](/api/docs/guides/model-optimization)

[Help center

Frequently asked account and billing questions](https://help.openai.com) [Developer forum

Discuss topics with other developers](https://community.openai.com/) [Cookbook

Open-source collection of examples and guides](/cookbook) [Status

Check the status of OpenAI services](https://status.openai.com)
