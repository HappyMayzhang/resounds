from pydantic import BaseModel, Field
from typing import Annotated
from resounds.tools import answer_correctness

class Context(BaseModel):
    relevant: Annotated[str, Field(description="相关知识")]

answer_correctness.setenv(Context(
    relevant = """
        各种语言都怎么打招呼？

        英语：'Hello'
        中文：'你好'
        法语：'Bonjour'
        日语：'こんにちは'
    """
))

if __name__ == '__main__':
    print(answer_correctness('Hello', '你好'))
    print(answer_correctness('Bonjour', 'こんにちは'))
