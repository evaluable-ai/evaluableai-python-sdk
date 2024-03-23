import os
from evaluableai.exceptions import EvaluableAIError

class Auth:
    def __init__(self, token):
        self.token = token
        if token is None:
            self.token = os.environ.get("EVALUABLEAI_API_KEY")
        if self.token is None:
            raise EvaluableAIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the "
                "EVALUABLEAI_API_KEY environment variable"
            )

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }
