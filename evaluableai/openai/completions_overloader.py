from openai import OpenAI as BaseOpenAI, AsyncOpenAI as BaseAsyncOpenAI, OpenAIError
from openai.resources.chat.completions import Completions as BaseCompletions
from openai.resources.chat.completions import AsyncCompletions as BaseAsyncCompletions
from openai._streaming import Stream, AsyncStream
from openai.types.chat import ChatCompletionChunk
from .ChatCompletion_overloader import ChatCompletion
from evaluableai.client import EvaluableAI, AsyncEvaluableAI
from evaluableai.exceptions import EvaluableAIError
import threading, time, random
import asyncio
from typing import Union, Any, Dict


def is_selected_for_eval(probability):
    # Generate a random number between 0 and 1
    rand_num = random.random()

    # If the random number is less than or equal to the given probability, select the item
    if rand_num <= probability:
        return True  # Selected
    else:
        return False  # Not selected


class CompletionsOverloader(BaseCompletions):
    eval_client: EvaluableAI
    base_client: BaseOpenAI

    def __init__(self, base_client: BaseOpenAI, eval_client: EvaluableAI, evaluableai_params: Dict[str, Any]) -> None:
        super().__init__(base_client)
        self.eval_client = eval_client
        self.evaluableai_params = evaluableai_params

    def create(self, *args, **kwargs) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:

        local_evaluableai_params = self.evaluableai_params.copy()
        ground_truth = kwargs.pop("ground_truth", None)
        # Add ground_truth to the local copy if it's provided
        if ground_truth is not None:
            local_evaluableai_params["ground_truth"] = ground_truth

        request_data = self.prepare_request_data(kwargs)
        try:
            start_time = time.time()
            chat_completion = super().create(*args, **kwargs)
            end_time = time.time()
            duration_in_ms = (end_time - start_time) * 1000
            local_evaluableai_params["time_taken"] = round(duration_in_ms, 3)

            if isinstance(chat_completion, Stream):
                return chat_completion
            else:
                response_data = chat_completion if isinstance(chat_completion, ChatCompletion) else None
                skip_submit = local_evaluableai_params.pop("skip_submit", None)
                if skip_submit:
                    return chat_completion
                if "async" in local_evaluableai_params and local_evaluableai_params["async"]:
                    def run_async_post():
                        asyncio.run(
                            self.post_to_server_async(request_data, response_data, local_evaluableai_params))

                    thread = threading.Thread(target=run_async_post)
                    thread.start()
                else:
                    response  = self.post_to_server(request_data, response_data, local_evaluableai_params)
                return chat_completion
        except Exception as e:
            raise

    def prepare_request_data(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return kwargs

    def aggregate_stream_content(self, stream: Stream[ChatCompletionChunk]) -> str:
        aggregated_content = ""
        for chunk in stream:
            aggregated_content += chunk.choices[0].delta.content or ""
        return aggregated_content

    def post_to_server(self, request_data: Dict[str, Any], response_data: Union[ChatCompletion, None],
                       local_evaluableai_params: Dict[str, Any]) -> None:
        sampling_rate = local_evaluableai_params.pop("sampling", None)
        sampling_flag = True
        if sampling_rate is not None:
            sampling_flag = is_selected_for_eval(sampling_rate)
            local_evaluableai_params["sampling_flag"] = sampling_flag

        endpoint = "/pythonsdk/openai/submitdata"
        if "eval" in local_evaluableai_params and local_evaluableai_params["eval"] and sampling_flag:
            endpoint = "/pythonsdk/openai/submitdataandeval"

        body = {
            "openai_request": request_data,
            "openai_response": response_data.model_dump() if response_data else None,
            "evaluableai_params": local_evaluableai_params
        }

        try:
            response = self.eval_client.make_request(method="POST", endpoint=endpoint, data=body)
            if response.status_code not in [200, 201]:
                raise EvaluableAIError(f"Failed to post data to evaluable ai server: {response.status_code}, {response.text}")
        except Exception as e:
            raise EvaluableAIError(
                f"Failed to post data to evaluable ai server"
            )

    async def post_to_server_async(self, request_data: Dict[str, Any], response_data: Union[ChatCompletion, None],
                                   local_evaluableai_params: Dict[str, Any]) -> None:

        sampling_rate = local_evaluableai_params.pop("sampling", None)
        sampling_flag = True
        if sampling_rate is not None:
            sampling_flag = is_selected_for_eval(sampling_rate)
            local_evaluableai_params["sampling_flag"] = sampling_flag

        endpoint = "/pythonsdk/openai/submitdata"
        if "eval" in local_evaluableai_params and local_evaluableai_params["eval"] and sampling_flag:
            endpoint = "/pythonsdk/openai/submitdataandeval"

        body = {
            "openai_request": request_data,
            "openai_response": response_data.model_dump() if response_data else None,
            "evaluableai_params": local_evaluableai_params
        }

        try:
            response = await self.eval_client.async_make_request(method="POST", endpoint=endpoint, data=body)
            if response.status_code not in [200, 201]:
                raise EvaluableAIError(f"Failed to post data to evaluable ai server: {response.status_code}, {response.text}")
        except Exception as e:
            raise EvaluableAIError(f"Exception occurred while posting data to evaluable ai server: {str(e)}")


class AsyncCompletionsOverloader(BaseAsyncCompletions):
    eval_client: AsyncEvaluableAI
    base_client: BaseAsyncOpenAI

    def __init__(self, base_client: BaseAsyncOpenAI, eval_client: AsyncEvaluableAI,
                 evaluableai_params: Dict[str, Any]) -> None:
        super().__init__(base_client)
        self.eval_client = eval_client
        self.evaluableai_params = evaluableai_params

    async def create(self, *args, **kwargs) -> Union[ChatCompletion, AsyncStream[ChatCompletionChunk]]:
        local_evaluableai_params = self.evaluableai_params.copy()
        ground_truth = kwargs.pop("ground_truth", None)
        if ground_truth is not None:
            local_evaluableai_params["ground_truth"] = ground_truth

        request_data = kwargs
        try:
            start_time = time.time()
            chat_completion = await super().create(*args, **kwargs)
            end_time = time.time()
            duration_in_ms = (end_time - start_time) * 1000
            local_evaluableai_params["time_taken"] = round(duration_in_ms, 3)
            response_data = chat_completion if isinstance(chat_completion, ChatCompletion) else None
            skip_submit = local_evaluableai_params.pop("skip_submit", None)
            if not skip_submit:
                await self.post_to_server_async(request_data, response_data, local_evaluableai_params)

            return chat_completion
        except OpenAIError as e:
            # Handle OpenAI specific errors here
            pass
        except Exception as e:
            # Handle other exceptions or re-raise
            raise

    async def post_to_server_async(self, request_data: Dict[str, Any], response_data: Union[ChatCompletion, None],
                                   local_evaluableai_params: Dict[str, Any]) -> None:

        sampling_rate = local_evaluableai_params.pop("sampling", None)
        sampling_flag = True
        if sampling_rate is not None:
            sampling_flag = is_selected_for_eval(sampling_rate)
            local_evaluableai_params["sampling_flag"] = sampling_flag

        endpoint = "/pythonsdk/openai/submitdata"
        if "eval" in local_evaluableai_params and local_evaluableai_params["eval"] and sampling_flag:
            endpoint = "/pythonsdk/openai/submitdataandeval"

        body = {
            "openai_request": request_data,
            "openai_response": response_data.model_dump() if response_data else None,
            "evaluableai_params": local_evaluableai_params
        }

        try:
            response = await self.eval_client.async_make_request(method="POST", endpoint=endpoint, data=body)
            if response.status_code not in [200, 201]:
                raise EvaluableAIError(f"Failed to post data to evaluable ai server: {response.status_code}, {response.text}")
        except Exception as e:
            raise EvaluableAIError(f"Exception occurred while posting data to evaluable ai server: {str(e)}")
