from importlib import import_module
from ..core.config import read_config

def LLM(**kwargs):
    config = read_config()
    module_obj = import_module(config['LLM']["module_name"])
    class_obj = getattr(module_obj, config['LLM']["class_name"])
    _kwargs = {
        key: value
        for key, value in config['LLM'].items()
        if key not in ["module_name", "class_name"]
    }
    _kwargs.update(kwargs)
    return class_obj(**_kwargs)
