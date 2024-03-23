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
            "token": "YOUR EVALUABLEAI API KEY",
            "eval": False,
            "sampling": 1,
            "eval_list": ["general_eval", "bleu", "word_error_rate", "rouge", "semantic_similarity"],
            "async": False  # This parameter seems to be redundant for async operations
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
