from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# создаем асинхронный движок котоырй будет отправлять запросы в БД
engine = create_async_engine(
    'sqlite+aiosqlite:///tasks.db'
)

# фабрика создания сессии (открытие транзакции для работы с БД)
new_session = async_sessionmaker(engine, expire_on_commit=False)


# Мы должны отключить поведение "expire on commit (завершить при фиксации)" для сессий с expire_on_commit=False.
# Это связано с тем, что в настройках async мы не хотим, чтобы SQLAlchemy выдавал новые SQL-запросы к базе данных при
# обращении к уже закоммиченным объектам.


class Model(DeclarativeBase):
    pass


# описываем таблицу
# class TaskTable(DeclarativeBase):  # получим ошибку sqlalchemy.exc.InvalidRequestError: Cannot use 'DeclarativeBase'
# directly as a declarative base class. Create a Base by creating a subclass of it.
class TaskTable(Model):  # а вот так не получим ошибку
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str | None]]
    created: Mapped[str]


# асинхронная ф-ия для создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


# асинхронная ф-ия для создания таблиц
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
