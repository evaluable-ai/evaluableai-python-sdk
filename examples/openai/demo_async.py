#!/usr/bin/env -S poetry run python

import asyncio

from evaluableai import AsyncOpenAI

# gets API Key from environment variable OPENAI_API_KEY and
client = AsyncOpenAI()


async def main() -> None:
    stream = await client.completions.create(
        model="gpt-3.5-turbo",
        prompt="Say this is a async demo run",
        stream=True,
    )
    async for completion in stream:
        print(completion.choices[0].text, end="")
    print()


asyncio.run(main())