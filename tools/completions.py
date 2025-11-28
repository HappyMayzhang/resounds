from ..core.func_to_signature import signature
from ..core.predictor import Env
from .program_of_thought import pot
import inspect, re

def func_to_tool(func) -> str:
    if isinstance(func, Env):
        func = func.func
    sig = signature(func)
    return {
        "type": "function",
        "function": {
            "name": sig['name'].replace('.', '-'),
            "description": sig['description'],
            "parameters": sig['inputs']["schema"]
        }
    }

def completions(obj):
    if isinstance(obj, str):
        declare = obj
    else:
        if isinstance(obj, Env):
            obj = obj.func
        declare = inspect.getsource(obj)
    return pot(re.sub(
        r'(?=[^\s])(return\s+)?\.\.\.',
        '<Complete the code here>',
        declare
    ))
