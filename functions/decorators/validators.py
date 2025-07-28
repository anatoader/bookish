from functools import wraps

from azure.functions import HttpRequest, HttpResponse


def validate_request_params(**expected_params):
    """
    Decorator used for validating request parameters.
    :param expected_params: Keyword arguments of expected request parameters, with their expected types
    and a boolean "required" value.
    :return: Decorated function.
    """

    def validation_decorator(func):
        @wraps(func)
        def wrapped_function(req: HttpRequest, *args, **kwargs):
            try:
                req_body = req.get_json()
            except ValueError:
                req_body = {}

            for param_name, rules in expected_params.items():
                param_value = req_body.get(param_name)
                param_type = rules.get('type', str)
                param_required = rules.get('required', False)

                if param_value is not None:
                    if not isinstance(param_value, param_type):
                        return HttpResponse(f"Expected {param_name} to be of type {param_type}", status_code=400)

                elif param_required:
                    return HttpResponse(f"Missing required parameter {param_name}", status_code=400)

            return func(req, *args, **kwargs)

        return wrapped_function

    return validation_decorator
