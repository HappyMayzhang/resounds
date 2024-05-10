# resounds使用手册

## 概述
resounds由三部分组成：
- 库函数
- 优化器
- 配置文件

### 库函数
```python
from resounds import (
    predictor, GPT, MoonShot, FastAPI,
    function_calling, func_to_tool,
    completions
)
```

### 优化器
```
# resounds -h
usage: resounds [-h] [--redo] func_name

Semantic function optimizer

positional arguments:
  func_name   module.func_name

options:
  -h, --help  show this help message and exit
  --redo      Redo or not
```

### 配置文件
```
# cat ~/.config/resounds/config.ini
```

## 库函数使用说明

### predictor - 语义函数修饰符
```python
def predictor(request):
    # request - GPT／MoonShot／FastAPI的实例
```
举例：
```python
from resounds import predictor, GPT
from typing import Annotated
import json

@predictor(GPT())
def answer_correctness(
    predicted_answer: Annotated[str, "predicted answer"],
    gold_answer: Annotated[str, "gold answer"]
) -> bool:
    """Verify that predicted answer and gold answer are expressing the same meaning."""
    try:
        predicted = json.loads(predicted_answer)
        gold = json.loads(gold_answer)
    except:
        predicted = predicted_answer
        gold = gold_answer
    if isinstance(predicted, str) and isinstance(gold, str):
        return True if predicted == gold else ...
    else:
        return predicted == gold
```

### function_calling - 语义匹配函数列表
```python
def function_calling(question: str, tools: list) -> dict:
    # tools - [func_to_tool(func) for func in <函数列表>]
    # return - {"name": <函数名>, "arguments": <函数参数>}
```
举例：
```python
from typing import Annotated
from pydantic import Field

def extract_student_info(
    name: Annotated[str, 'Name of the person'],
    major: Annotated[str, 'Major subject.'],
    school: Annotated[str, 'The university name.'],
    grades: Annotated[int, 'GPA of the student.'],
    club: Annotated[str, 'School club for extracurricular activities.']
) -> dict:
    """抽取学生信息"""

def extract_school_info(
    name: Annotated[str, 'Name of the school.'],
    ranking: Annotated[int, 'QS world ranking of the school.'],
    country: Annotated[str, 'Country of the school.'],
    no_of_students: Annotated[int, 'Number of students enrolled in the school.']
) -> dict:
    """抽取学校信息"""

def query_weather(
    province: Annotated[str, "省、自治区、直辖市"],
    city: Annotated[str, "地级市"],
    day: Annotated[int, Field(ge=-1, le=14, description="0:今天 1:明天")] = 0
) -> dict:
    """查询天气预报"""

def other(
    question: Annotated[str, "question"]
) -> None:
    """抽取任何信息或查询任何资料"""

#####

from resounds import function_calling, func_to_tool

tools = [
    func_to_tool(func)
    for func in (extract_student_info, extract_school_info, query_weather, other)
]

for text in [
    student_1_description,
    school_1_description,
    "LLM根据函数描述，参数描述以及用户的输入，来决定要调用哪个函数。",
    '明天北京海淀的天气怎么样？',
    student_2_description
]:
    kwargs = function_calling(text, tools)
    print(kwargs)
```

### completions - 补全python程序
```python
def completions(obj) -> str:
    # obj - 字符串／函数／类
    # return - 生成的代码
```
举例：
```python
from resounds import completions

declare = '''
from typing import Annotated

Complex = Annotated[tuple[float, float], "a complex number"]

def div(x: Complex, y: Complex) -> Complex:
    """复数除法"""
'''

code = completions(declare)
print('-' * 8)
print(code)
print('-' * 8)
exec(code)

if __name__ == "__main__":
    print(div((-1, -2), (3, 1)))
```

## 优化器使用说明

## 配置文件使用说明
```
[Example]
# resounds保存数据目录
save_dir = /root/.config/resounds/save_dir
# resounds读取数据目录
read_dir = /root/.config/resounds/read_dir

[LLM]
# resounds自身使用的LLM
module_name = resounds
class_name = GPT
# 还可以在下面设置一些参数

[GPT]
# openai gpt模型，默认使用"gpt-3.5-turbo-instruct"
api_key = sk-
base_url = https://api.openai.com/v1
# 还可以在下面设置一些参数

[MoonShot]
# 默认使用"moonshot-v1-8k"
api_key = sk-
base_url = https://api.moonshot.cn/v1
# 还可以在下面设置一些参数

[logging]
# LLM的日志文件
filename = /var/log/gpt.log
```

