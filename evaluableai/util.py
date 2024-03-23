from .exceptions import InvalidEvaluableAIParameterError
from typing import Any, Dict


def validate_evaluableai_params(evaluableai_params: Dict[str, Any]):
    if 'sampling' in evaluableai_params:
        sampling_value = evaluableai_params['sampling']
        if not 0 <= sampling_value <= 1:
            raise InvalidEvaluableAIParameterError("The 'sampling' value must be between 0 and 1 inclusive.")

    if 'async' in evaluableai_params:
        async_value = evaluableai_params['async']
        if not isinstance(async_value, bool):
            raise InvalidEvaluableAIParameterError("The 'async' value must be either True or False.")

    if 'eval' in evaluableai_params:
        eval_value = evaluableai_params['eval']
        if not isinstance(eval_value, bool):
            raise InvalidEvaluableAIParameterError("The 'eval' value must be either True or False.")
