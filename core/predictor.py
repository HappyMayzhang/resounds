from inspect import getfullargspec
from .example import Example

class Env:
    def __init__(self, func, request):
        self.func = func
        self.request = request
        self.env = None

    def setenv(self, env):
        self.env = env

    def __call__(self, *args, **kwargs):
        func_args = getfullargspec(self.func).args
        kwargs.update(dict(zip(func_args, args)))
        answer = self.func(**kwargs)
        if answer is ...:
            request = self.request
            if hasattr(request, "kwargs") and "messages" in request.kwargs:
                return request.chat_completions(request.kwargs)
            example = Example(self.func, kwargs)
            example.setenv(self.env)
            if hasattr(request, "kwargs") and "tools" in request.kwargs:
                example.settools(
                    request.kwargs["tools"],
                    request.kwargs.get("tool_choice", "auto")
                )
            answer = example(request)
            example.save()
        return answer

def predictor(request):
    def decorator(func):
        return Env(func, request)
    return decorator
