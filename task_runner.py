import asyncio
from config import logger

class TaskRunner:
    @classmethod
    @logger.catch()
    async def run_tasks(cls, func, tasks):
        sem = asyncio.Semaphore(4)
        async_tasks = []
        @logger.catch()
        async def task_wrapper(t):
            async with sem:
                try:
                    await func(t)
                except Exception as e:
                    raise e

        for task in tasks:
            t = asyncio.create_task(task_wrapper(task))
            async_tasks.append(t)
        await asyncio.gather(*async_tasks)
