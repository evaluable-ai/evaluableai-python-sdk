#!/usr/bin/env -S poetry run python

from evaluableai import OpenAI

# gets API Key from environment variable OPENAI_API_KEY and EVALUABLEAI_API_KEY
client = OpenAI(
    evaluableai_params={
        "token": "YOUR EVALUABLEAI API KEY",
        "eval": True,  # Optional
        "sampling": 1,  # Optional Value between 0 and 1
        "eval_list": ["general_eval", "bleu", "word_error_rate", "rouge", "semantic_similarity"],  # Optional
        "async": False  # Optional default is False
    }
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Say this was a demo run",
        },
    ],
)
print(completion.choices[0].message.content)
