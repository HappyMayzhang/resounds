import inspect
from typing import Annotated, get_origin, get_args
from pydantic.fields import Field, FieldInfo
from pydantic import TypeAdapter

def get_field_info(annotations, name):
    annotation = annotations.get(name, str)
    if get_origin(annotation) is Annotated:
        annotation, field_info, *metadata = get_args(annotation)
        if not isinstance(field_info, FieldInfo):
            if isinstance(field_info, str):
                field_info = Field(description=field_info)
            else:
                raise TypeError("Annotated[<type>, Field(description='...')]?")
    else:
        field_info = Field()
    return annotation, field_info

def trim(docstring):
    if not docstring:
        return ''
    lines = docstring.splitlines()
    indent = 256
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    trimmed = [lines[0].strip()]
    for line in lines[1:]:
        trimmed.append(line[indent:].rstrip())
    return '\n'.join(trimmed).strip()

def signature(func):
    func_name = func.__module__ + '.' + func.__qualname__
    instructions = trim(func.__doc__)
    parameters = inspect.signature(func).parameters
    annotations = inspect.getfullargspec(func).annotations

    to_json = {}
    properties = {}
    required = []
    for param in parameters.values():
        annotation, field_info = get_field_info(annotations, param.name)
        if isinstance(param.default, FieldInfo):
            field_info = param.default
        elif param.default is not param.empty:
            field_info.default = param.default
        typeadapter = TypeAdapter(Annotated[annotation, field_info])
        to_json[param.name] = typeadapter.dump_python
        properties[param.name] = typeadapter.json_schema()
        if field_info.is_required():
            required.append(param.name)

    annotation, field_info = get_field_info(annotations, "return")
    typeadapter = TypeAdapter(Annotated[annotation, field_info])
    return {
        'name': func_name,
        'description': instructions,
        'inputs': {
            "to_json": to_json,
            "schema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        },
        'output': {
            "from_json": typeadapter.validate_python,
            "schema": typeadapter.json_schema()
        }
    }
