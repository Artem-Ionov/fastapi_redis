from fastapi import FastAPI

app = FastAPI(title="Данные о торгах")

@app.get("/")
async def root():
    """Корневой маршрут для проверки работоспособности"""
    return {"message": "Добро пожаловать!"}