from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status

from repository import TaskRepository
from schemas import TaskAdd, TaskId

router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.get("/")
async def get_tasks() -> List[TaskAdd]:
    task_dicts = await TaskRepository.find_all()
    tasks = [TaskAdd(**task_dict) for task_dict in task_dicts]
    return tasks


@router.post("/")
async def add_task(task: TaskAdd) -> TaskId:
    try:
        task_id = await TaskRepository.add_one(task)  # все ф-ии внутри репо асинхронные
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'{e}'
        )
    else:
        return {"ok": True, 'task_id': task_id}  # Pycharm ругает на возврат dict, но на самом деле все ок, т.к соответсвие схеме TaskId
