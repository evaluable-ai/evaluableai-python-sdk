# Evaluable AI Python SDK

The SDK facilitates seamless integration between performing inferences using various AI models and evaluating those responses on the Evaluable AI platform. 

## Documentation

For detailed documentation, please refer to [Evaluable AI Docs](https://docs.evaluable.ai/).

## Installation

- Register using this [link](https://portal.evaluable.ai/signin) 
- Navigate to the [settings page](https://portal.evaluable.ai/settings)
- Under the section `Evaluable AI keys` provide a key name and click generate. Securly save the api key. The key can only be copied at time of creation.
- Optional: Add your key to an env variable "EVALUABLEAI_API_KEY"


```sh
pip install -e /path/to/evaluableai_package
```

## Open AI

### Usage
In your code, you only need to change the import from openai to evaluableai for client creation.

```python
import os
from evaluableai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
    evaluableai_params={
        "token": "EVALUABLEAI_API_KEY"
    }
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)
```

While you can provide an `api_key` keyword argument,
we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
to add your keys : `EVALUABLEAI_API_KEY="My API Key"` to your `.env` file
so that your API Key is not stored in source control.

All the parmeters required for evaluating responses and for seeing the evaluation runs on the UI are passed in the evaluableai_params. Below is list of all parameters: 

![image](https://github.com/evaluable-ai/private-evaluableai-python-sdk/assets/149981851/b6e77cd5-8496-4128-a519-a20d84c0efd9)


## Async usage
In your code, you only need to change the import from openai to evaluableai for client creation.
Simply import `AsyncOpenAI` instead of `OpenAI` and use `await` with each API call:

```python
import os
import asyncio
from evaluableai import AsyncOpenAI

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
    evaluableai_params={
        "token": "EVALUABLEAI_API_KEY"
    }
)


async def main() -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise identical.

## Mistral AI

### Usage

In your code, you only need to change the import from mistralai to evaluableai for client creation.

```python
from evaluableai import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

print(chat_response.choices[0].message.content)
```

## Async usage
In your code, you only need to change the import from mistralai to evaluableai for client creation.
Simply import `MistralAsyncClient` instead of `MistralClient` and use `await` with each API call:

```python
import asyncio
import os
from evaluableai import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage

async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-tiny"

    client = MistralAsyncClient(
        api_key=api_key,
        evaluableai_params={
            "token": "EVALUABLEAI_API_KEY",
        }
    )

    messages = [
        ChatMessage(role="user", content="What is the best French cheese?")
    ]

    # Await the async chat method
    async_response = await client.chat(model=model, messages=messages)

    # Assuming async_response has a method or attribute to retrieve the response content
    # The specific way to print or process the response will depend on the implementation
    # of your ChatCompletionResponse class and the data structure it provides.
    print("Response:", async_response)

if __name__ == "__main__":
    asyncio.run(main())

```

## Requirements

Python 3.9 or higher.
