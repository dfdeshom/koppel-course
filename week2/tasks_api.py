import typing

class ToDoTask:
    name: str
    is_done: bool = False
    id: int 
            
class ToDoTaskManager:
    tasks: typing.Dict[int, ToDoTask]
    
    def create_task(name: str) -> ToDoTask:
        pass
    def delete_task(task_id: int) -> None:
        pass
    def list_tasks() -> typing.List[ToDoTask]:
        pass
    def mark_task_as_done(task_id: int) -> None:
        pass
