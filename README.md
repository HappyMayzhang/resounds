# About
resounds是一个语义函数开发框架，遵循以下三点开发原则：
1. 语义函数是最基本的开发组件，语义函数独立于LLM；
2. 语义函数执行过程中自动形成测试样本库，每个样本都可重现；
3. 可为语义函数编写测试工具，基于样本库测试结果评估语义函数质量；

resounds现在支持GPT和MoonShot两个LLM。

# Install
`$ pip3 install -U resounds`

# resounds使用手册

## 概述
resounds由三部分组成：
- 库函数
- 优化器
- 配置文件

### 库函数
```python
from resounds import (
    predictor,
    GPT, MoonShot, FastAPI,
    func_to_tool,
    completions
)
```

### 优化器
```
# resounds -h
usage: resounds [-h] func_name

Semantic function optimizer

positional arguments:
  func_name   module.func_name

options:
  -h, --help  show this help message and exit
```

### 配置文件
```
# cat ~/.config/resounds/config.ini
```

## 库函数使用示例

### 会话过程感知
```python
from resounds import predictor, GPT
from typing import Literal

topics = {"旅游", "美食", "编程", "英语"}
@predictor(GPT())
def focus(text: str) -> Literal["无", *topics]:
    """Extract topic"""
    return ...
    
if __name__ == "__main__":
    print(focus("北京周边有什么好玩的地方？")) #旅游
    print(focus("都有什么特点？"))            #无
    print(focus("周末去吃烧烤吧。"))          #美食
    print(focus("烤鸭也很好吃。"))            #美食
```

### 使用本地知识库
```python
from resounds import predictor, GPT

@predictor(GPT())
def greet(question: str) -> str:
    return ...

greet.setenv("""
    北京人见面打招呼：您现在还好吧？家里人都好吧？
    老北京人见面打招呼：吃了吗？您呢。
""")

if __name__ == "__main__":
    print(greet("北京人见面怎么打招呼？"))   #您现在还好吧？家里人都好吧？
    print(greet("老北京人见面怎么打招呼？")) #吃了吗？您呢。
```

### 提取表格
```python
from resounds import func_to_tool, predictor, GPT

def extract_markdown_table(table: list[list[str]]) -> dict:
    """Extract markdown table"""

@predictor(GPT(
    tools = [func_to_tool(extract_markdown_table)]
))
def chat(question: str) -> str | list:
    return ...

if __name__ == "__main__":
    results = chat("""
使用连字符和管道创建表可能很麻烦。为了加快该过程，请尝试使用Markdown Tables Generator。使用图形界面构建表，然后将生成的Markdown格式的文本复制到文件中。
# 对齐
您可以通过在标题行中的连字符的左侧，右侧或两侧添加冒号（:），将列中的文本对齐到左侧，右侧或中心。
| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |
呈现的输出如下所示：
""")
    if isinstance(results, list):
        for result in results:
            print(result["arguments"]["table"]) #[['Syntax', 'Description', 'Test Text'], [' :---', ' :----:', ' ---:'], ['Header', 'Title', "Here's this"], ['Paragraph', 'Text', 'And more']]
    else:
        print(results)
```

### 补全python代码
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
    print(div((-1, -2), (3, 1))) #(-0.5, -0.5)
```

## 优化器使用示例
以语义函数 `__main__.focus` 为例

- 编写测试工具 `# vi focus.py`
```
from resounds import MoonShot

request = MoonShot()

def verify(example) -> bool:
    return example['output']["return"] in ["无", "旅游", "美食", "编程", "英语"]
```
- 执行命令 `# resounds __main__.focus`
```
Menu:

1) Modify Function Description
2) Summarize Function Descriptions
3) Evaluate Semantic Functions

Press ^D to return.
Press ^C to abort.
I pick: 
```
1. `Modify Function Description`针对没有通过测试的样本，修改'函数描述'；
2. `Summarize Function Descriptions`所有通过测试的样本，可能有多个'函数描述'，要归纳为一个；
3. `Evaluate Semantic Functions`指定一个'函数描述'，用所有样本测试；

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
model = gpt-3.5-turbo-instruct

[GPT]
# 默认使用"gpt-3.5-turbo"
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

# Contact us
<may.xiaoya.zhang@gmail.com>
