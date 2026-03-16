from src.sources import TaskSource
from src.models import Task

def run_tasks(source: TaskSource) -> list[Task]:
    """Validate the source implements TaskSource protocol and retrieve tasks from it"""

    if not isinstance(source, TaskSource):
        raise TypeError(f"{source} does not match contract TaskSource")
    
    return source.get_tasks()


