# модуль для реализации паттерна репозиторий. Он позволяет работать с БД как с коллекцией объектов
# добавлять объекты через add() например, редактирвоать, читать и т.д
from sqlalchemy import select

from database import new_session, TaskTable
from schemas import TaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls,
                      data: TaskAdd) -> int:  # для добавления новой таски указываем тип принимаемых данных - TaskAdd
        async with new_session() as session:  # говорим что открытый контекстный менеджер отдает объект сессии
            task_dict = data.model_dump()  # преобразуем объект TaskAdd в словарь

            task = TaskTable(**task_dict)  # новая таска - объект, новая строка в таблице с полями. id сами не задаем
            session.add(task)  # запрос на добавление объекта в сессию. session - объект для работы с транзакцией.

            await session.flush()  # чтобы первичный ключ в объекте Task отобразился, делаем flush.
            # flush не завершает транзакцию, но только отправляет изменение в БД и получит id таски
            await session.commit()  # исполнение запроса. Все добавленные через add изменения окажутся в БД

            return task.id

    @classmethod
    async def find_all(cls) -> list[TaskAdd]:
        async with new_session() as session:
            query = select(TaskTable)
            res = await session.execute(query)
            task_models = res.scalars().all()

            # чтобы эндпоинт get_tasks() вернул TaskAdd, нужно объекты бд конвертировать в pydantic-схемы:
            tasks = [
                {"name": task_model.name, "description": task_model.description, "created": task_model.created}
                for task_model in task_models
            ]
            # return task_models
            return tasks
    # здесь будет использована фабрика сессий, позволяющая работать с объектами БД как с реальными моделями, с экз-ми
    # класса TaskTable
