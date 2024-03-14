from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import delete_tables, create_tables
from router import router as tasks_router


@asynccontextmanager  # декоратор для создания контекстных менеджеров
async def lifespan(app: FastAPI):
    print('Включение приложения')
    # await delete_tables()
    # print('БД очищена')
    await create_tables()
    print('БД готова к работе. Таблицы созданы')
    yield
    print('Выключение приложения')


app = FastAPI(lifespan=lifespan)
app.include_router(router=tasks_router)


@app.get("/", name='Root')
def root():
    return {"msg": "Welcome to the simple_tasks API. U can go to the docs by link: http://127.0.0.1:8000/docs"}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
