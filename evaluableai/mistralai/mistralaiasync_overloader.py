import random
import time
from typing import Dict, Any
from mistralai.async_client import MistralAsyncClient as BaseAsyncMistralClient
from mistralai.models.chat_completion import ChatCompletionResponse
from pydantic import BaseModel
from evaluableai.client import AsyncEvaluableAI
from evaluableai.exceptions import EvaluableAIError
from evaluableai.util import validate_evaluableai_params


def serialize_pydantic_model(model):
    """
    Serialize a Pydantic model to a dictionary, handling lists of models.
    """
    if isinstance(model, BaseModel):
        return model.dict()
    elif isinstance(model, list):
        return [serialize_pydantic_model(item) for item in model]
    else:
        return model


def handle_kwargs_for_chat(**kwargs) -> Dict[str, Any]:
    """
    Inspect and serialize kwargs for the chat function, particularly handling lists of Pydantic models.
    """
    serialized_kwargs = {}
    for key, value in kwargs.items():
        # Check if the value is a Pydantic model or a list of Pydantic models
        serialized_kwargs[key] = serialize_pydantic_model(value)
    return serialized_kwargs


def is_selected_for_eval(probability):
    # Generate a random number between 0 and 1
    rand_num = random.random()

    # If the random number is less than or equal to the given probability, select the item
    if rand_num <= probability:
        return True  # Selected
    else:
        return False  # Not selected


class MistralAsyncClientOverloader(BaseAsyncMistralClient):
    eval_client: AsyncEvaluableAI

    def __init__(self, api_key: str, evaluableai_params: Dict[str, Any] = None, **kwargs) -> None:
        super().__init__(api_key=api_key, **kwargs)
        if evaluableai_params is None:
            evaluableai_params = {}
        token = evaluableai_params.pop("token", None)
        validate_evaluableai_params(evaluableai_params)
        self.evaluableai_params = evaluableai_params
        if token is not None:
            self.eval_client = AsyncEvaluableAI(token)
        else:
            self.eval_client = AsyncEvaluableAI()

    async def chat(self, *args, **kwargs) -> ChatCompletionResponse:
        local_evaluableai_params = self.evaluableai_params.copy()
        ground_truth = kwargs.pop("ground_truth", None)
        # Add ground_truth to the local copy if it's provided
        if ground_truth is not None:
            local_evaluableai_params["ground_truth"] = ground_truth
        try:
            start_time = time.time()
            chat_completion = await super().chat(*args, **kwargs)
            end_time = time.time()
            duration_in_ms = (end_time - start_time) * 1000
            local_evaluableai_params["time_taken"] = round(duration_in_ms, 3)
            response_data = chat_completion
            skip_submit = local_evaluableai_params.pop("skip_submit", None)
            if not skip_submit:
                request_data = self.handle_kwargs_for_chat(**kwargs)
                await self.post_to_server_async(request_data, response_data, local_evaluableai_params)
            return chat_completion
        except Exception as e:
            raise

    def serialize_pydantic_model(self, model):
        """
        Serialize a Pydantic model to a dictionary, handling lists of models.
        """
        if isinstance(model, BaseModel):
            return model.dict()
        elif isinstance(model, list):
            return [serialize_pydantic_model(item) for item in model]
        else:
            return model

    def handle_kwargs_for_chat(self, **kwargs) -> Dict[str, Any]:
        serialized_kwargs = {}
        for key, value in kwargs.items():
            serialized_kwargs[key] = self.serialize_pydantic_model(value)  # Adjusted to use self
        return serialized_kwargs

    async def post_to_server_async(self, request_data: Dict[str, Any], response_data: ChatCompletionResponse,
                                   local_evaluableai_params: Dict[str, Any]):
        sampling_rate = local_evaluableai_params.pop("sampling", None)
        sampling_flag = is_selected_for_eval(sampling_rate) if sampling_rate is not None else True
        local_evaluableai_params["sampling_flag"] = sampling_flag

        endpoint = "/pythonsdk/mistralai/submitdata"
        if "eval" in local_evaluableai_params and local_evaluableai_params["eval"] and sampling_flag:
            endpoint = "/pythonsdk/mistralai/submitdataandeval"

        body = {
            "mistralai_request": request_data,
            "mistralai_response": response_data.dict() if response_data else None,
            "evaluableai_params": local_evaluableai_params
        }

        try:
            response = await self.eval_client.async_make_request(method="POST", endpoint=endpoint, data=body)
            if response.status_code not in [200, 201]:
                raise EvaluableAIError(f"Failed to post data to evaluable ai server: {response.status_code}, {response.text}")
        except Exception as e:
            raise EvaluableAIError(f"Failed to post data to evaluable ai server")
