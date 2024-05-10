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
