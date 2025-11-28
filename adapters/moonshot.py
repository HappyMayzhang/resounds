from .template import template, extract
from ..core.config import read_config
from openai import OpenAI
import json, logging

class MoonShot:
    def __init__(
        self,
        model: str = "moonshot-v1-8k",
        **kwargs
    ):
        login = {}
        config = read_config()[type(self).__name__]
        if 'api_key' in config:
            login['api_key'] = config['api_key']
        if 'base_url' in config:
            login['base_url'] = config['base_url']
        self.client = OpenAI(**login)
        self.model_type = "chat"
        self.kwargs = {
            "model": model,
            "temperature": 0.0,
            "max_tokens": 2048,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "n": 1,
            **kwargs,
        }

    def chat_completions(self, kwargs: dict) -> str | list:
        logging.info(kwargs)
        choice = self.client.chat.completions.create(**kwargs).choices[0]
        logging.info(choice)
        match choice.finish_reason:
            case "tool_calls":
                kwargs["messages"].append(choice.message)
                return [
                    {
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    }
                    for tool_call in choice.message.tool_calls
                ]
            case "stop":
                kwargs["messages"].append(choice.message)
                return choice.message.content
            case "length":
                kwargs["messages"].append(choice.message)
                return choice.message.content

    def completions(self, kwargs: dict) -> str:
        logging.info(kwargs)
        choice = self.client.completions.create(**kwargs).choices[0]
        logging.info(choice)
        match choice.finish_reason:
            case "stop":
                return choice.text
            case "length":
                return choice.text

    def __call__(self, example) -> list:
        kwargs = self.kwargs.copy()
        if self.model_type == "text":
            if "tools" in kwargs:
                kwargs.pop("tools")
            if "tool_choice" in kwargs:
                kwargs.pop("tool_choice")
            kwargs["prompt"] = template(example, "text")
            return extract(self.completions(kwargs), "text")
        elif "tools" in example:
            kwargs["tools"] = example["tools"]
            if "tool_choice" in example:
                kwargs["tool_choice"] = example["tool_choice"]
            kwargs["messages"] = [{
                "role": "system",
                "content": example['instructions']
            }] if example['instructions'] else []
            kwargs["messages"].append({
                "role": "user",
                "content": json.dumps(example['inputs']["kwargs"], ensure_ascii=False)
            })
            return [self.chat_completions(kwargs)]
        else:
            kwargs["messages"] = [{
                "role": "user",
                "content": template(example, "chat")
            }]
            return extract(self.chat_completions(kwargs), "chat")
