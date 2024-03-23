from openai import OpenAI as BaseOpenAI, AsyncOpenAI as BaseAsyncOpenAI
from evaluableai.client import EvaluableAI, AsyncEvaluableAI
from .chat_overloader import ChatOverloader, AsyncChatOverloader
from typing import Any, Dict
from evaluableai.util import validate_evaluableai_params


class OpenAiOverloader(BaseOpenAI):
    chat: ChatOverloader
    eval_client: EvaluableAI

    def __init__(self, api_key: str = None, evaluableai_params: Dict[str, Any] = None, **kwargs) -> None:
        try:
            super().__init__(api_key=api_key, **kwargs)
            
            if evaluableai_params is None:
                evaluableai_params = {}
            
            # Pop out the 'token' value if it exists, otherwise None
            token = evaluableai_params.pop("token", None)
            validate_evaluableai_params(evaluableai_params)
            
            if token is not None:
                self.eval_client = EvaluableAI(token)
            else:
                self.eval_client = EvaluableAI()
            
            self.chat = ChatOverloader(self, self.eval_client, evaluableai_params)
        
        except Exception as e:
            print(f"An error occurred during initialization: {str(e)}")


class OpenAiAsyncOverloader(BaseAsyncOpenAI):
    chat: AsyncChatOverloader
    eval_client: AsyncEvaluableAI

    def __init__(self, api_key: str = None, evaluableai_params: Dict[str, Any] = None, **kwargs) -> None:
        try:
            super().__init__(api_key=api_key, **kwargs)
            
            if evaluableai_params is None:
                evaluableai_params = {}
            
            # Pop out the 'token' value if it exists, otherwise None
            token = evaluableai_params.pop("token", None)
            validate_evaluableai_params(evaluableai_params)
            
            if token is not None:
                self.eval_client = AsyncEvaluableAI(token)
            else:
                self.eval_client = AsyncEvaluableAI()
            
            self.chat = AsyncChatOverloader(self, self.eval_client, evaluableai_params)
        
        except Exception as e:
            print(f"An error occurred during initialization: {str(e)}")