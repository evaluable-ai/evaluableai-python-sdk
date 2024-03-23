from openai import OpenAI as BaseOpenAI, AsyncOpenAI as BaseAsyncOpenAi
from openai.resources import Chat as BaseChat, AsyncChat as BaseAsyncChat
from .completions_overloader import CompletionsOverloader, AsyncCompletionsOverloader
from evaluableai.client import EvaluableAI, AsyncEvaluableAI
from typing import Any, Dict


class ChatOverloader(BaseChat):
    completions: CompletionsOverloader

    def __init__(self, base_client: BaseOpenAI, eval_client: EvaluableAI, evaluableai_params: Dict[str, Any]) -> None:
        try:
            super().__init__(base_client)
            self.completions = CompletionsOverloader(base_client, eval_client, evaluableai_params)
        except Exception as e:
            raise ConnectionError(f"Failed to initialize ChatOverloader: {e}") from e


class AsyncChatOverloader(BaseAsyncChat):
    completions: AsyncCompletionsOverloader

    def __init__(self, base_client: BaseAsyncOpenAi, eval_client: AsyncEvaluableAI, evaluableai_params: Dict[str, Any]) -> None:
        try:
            super().__init__(base_client)
            self.completions = AsyncCompletionsOverloader(base_client, eval_client, evaluableai_params)
        except Exception as e:
            raise ConnectionError(f"Failed to initialize AsyncChatOverloader: {e}") from e
