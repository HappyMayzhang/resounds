from typing import Annotated
from pydantic import Field
from resounds.tools import china_weather_15

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
    data = china_weather_15(province, city)['data']
    return data['yesterday'] if day < 0 else data['forecast'][day]

def other(
    question: Annotated[str, "question"]
) -> None:
    """抽取任何信息或查询任何资料"""

#####

from resounds import func_to_tool, function_calling
from time import sleep

tools = [
    func_to_tool(extract_student_info),
    func_to_tool(extract_school_info),
    func_to_tool(query_weather),
    func_to_tool(other)
]
print(tools)

student_1_description = "David Nguyen is a sophomore majoring in computer science at Stanford University. He is Asian American and has a 3.8 GPA. David is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after graduating."
student_2_description="Ravi Patel is a sophomore majoring in computer science at the University of Michigan. He is South Asian Indian American and has a 3.7 GPA. Ravi is an active member of the university's Chess Club and the South Asian Student Association. He hopes to pursue a career in software engineering after graduating."
school_1_description = "Stanford University is a private research university located in Stanford, California, United States. It was founded in 1885 by Leland Stanford and his wife, Jane Stanford, in memory of their only child, Leland Stanford Jr. The university is ranked #5 in the world by QS World University Rankings. It has over 17,000 students, including about 7,600 undergraduates and 9,500 graduates23. "

for a in [
    student_2_description,
    school_1_description,
    "LLM根据函数描述，参数描述以及用户的输入，来决定是不是要调用这个函数。",
    '明天北京海淀的天气怎么样？',
    student_1_description
]:
    kwargs = function_calling(a, tools)
    print(kwargs)
    match kwargs['name']:
        case '__main__.query_weather':
            print(query_weather(**kwargs['arguments']))
        case '__main__.other':
            print("------")
    sleep(21)
