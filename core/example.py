from .func_to_signature import signature
from .config import save_example
from pydantic import TypeAdapter

class Example:
    def __init__(self, func, kwargs):
        sig = signature(func)

        inputs = sig['inputs']
        to_json = inputs['to_json']
        _schema = inputs['schema']
        properties = _schema["properties"]

        output = sig['output']
        self.from_json = output['from_json']
        schema_ = output['schema']

        kwargs_ = {}
        for name, check in to_json.items():
            if name in kwargs:
                kwargs_[name] = check(kwargs[name])
            elif 'default' in properties[name]:
                kwargs_[name] = check(properties[name]['default'])
            else:
                raise NameError(f"Miss argument '{name}'")

        self.example = {
            'func_name': sig['name'],
            'instructions': sig['description'],
            'inputs': {
                "schema": _schema,
                "kwargs": kwargs_
            },
            'output': {
                "schema": schema_
            }
        }

    def setenv(self, env):
        if not env: return
        if isinstance(env, str):
            self.example['context'] = env
        else:
            typeadapter = TypeAdapter(type(env))
            self.example['context'] = {
                "schema": typeadapter.json_schema(),
                "kwargs": typeadapter.dump_python(env)
            }

    def settools(self, tools, tool_choice = "auto"):
        if not tools: return
        self.example['tools'] = tools
        if tool_choice != "auto":
            self.example['tool_choice'] = tool_choice

    def save(self):
        save_example(self.example)

    def __call__(self, request):
        results = request(self.example)
        for result in results:
            try:
                answer = self.from_json(result)
            except:
                pass
            else:
                output = self.example['output']
                output['return'] = result
                return answer
        raise ValueError("Invalid format string")
