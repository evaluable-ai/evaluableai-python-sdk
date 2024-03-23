import os
from evaluableai import MistralClient
from mistralai.models.chat_completion import ChatMessage

#The following settings will ontl send data to evlauable ai and will not run eval
client = MistralClient(
    api_key=os.environ["MISTRAL_API_KEY"],
    evaluableai_params={
        "token": "YOUR EVALUABLEAI API KEY"
    }
)

messages = [
    ChatMessage(role="user", content="what comes after tank in dictionary")
]


chat_response = client.chat(
    model="mistral-tiny",
    messages=messages,
)

################################################################
#Demo 2 Running with eval

import os
from evaluableai import MistralClient
from mistralai.models.chat_completion import ChatMessage

client = MistralClient(
    api_key=os.environ["MISTRAL_API_KEY"],
    evaluableai_params={
        "token": "YOUR EVALUABLEAI API KEY",
        "eval": True,
        "sampling": 1,
        "eval_list": ["general_eval", "bleu", "word_error_rate", "rouge", "semantic_similarity"],
        "async": False
    }
)

messages = [
    ChatMessage(role="user", content="what comes after tank in dictionary")
]

# No streaming
chat_response = client.chat(
    model="mistral-tiny",
    messages=messages,
)
