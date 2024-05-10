from resounds import predictor, FastAPI

@predictor(FastAPI(
    url = 'https://www.runoob.com/try/ajax/json_demo.json',
    method = 'GET'
))
def test_fastapi() -> dict:
    return ...

print(test_fastapi())
