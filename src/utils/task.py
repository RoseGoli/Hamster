import asyncio
from src.utils.logger import logger

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.stop_event = asyncio.Event()

    async def task_wrapper(self, coro_func, *args, **kwargs):
        print(f"Task {args[0]} starting")
        while not self.stop_event.is_set():
            await coro_func(*args, **kwargs)
        print(f"Task {args[0]} stopping")

    def start_tasks(self, task_funcs):
        self.stop_event.clear()
        self.tasks = [
            asyncio.create_task(self.task_wrapper(task_func, i))
            for i, task_func in enumerate(task_funcs)
        ]

    async def stop_tasks(self):
        self.stop_event.set()
        await asyncio.gather(*self.tasks)
        self.tasks = []