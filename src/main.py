from typing import runtime_checkable, Protocol
from dataclasses import dataclass
import random, time, json


@dataclass
class Task:
    """Unit of work with id and data payload"""

    id: int
    payload: dict


@runtime_checkable
class TaskSource(Protocol):
    """Structural protocol defining the interface"""

    def get_tasks(self) -> list[Task]:
        """Retrieve a list of tasks from the source"""
        pass


class GeneratorTaskSource:
    """Task source that creates random task objects"""

    def get_tasks(self) -> list[Task]:
        """Generate random tasks"""

        tasks = [Task(id=random.randint(1, 100), payload={"order_id": random.randint(1, 1000), "amount": random.randint(100, 1000)}) for i in range(random.randint(1, 5))]
        return tasks


class ApiTaskSource:
    """API stub that simulates an external task source"""

    def get_tasks(self) -> list[Task]:
        """Simulate API call to fetch tasks with a delay"""
        time.sleep(1)
        return [
            Task(id=101, payload={"order_id": random.randint(1001, 2000), "amount": random.randint(1000, 2000)}),
            Task(id=102, payload={"order_id": random.randint(1001, 2000), "amount": random.randint(1000, 2000)}),
            Task(id=103, payload={"order_id": random.randint(1001, 2000), "amount": random.randint(1000, 2000)}),
            Task(id=104, payload={"order_id": random.randint(1001, 2000), "amount": random.randint(1000, 2000)})
        ]
    

class FileTaskSource:
    """Task source that reads and parses task data from JSON file"""

    def __init__(self, filename: str):
        self.filename = filename


    def get_tasks(self) -> list[Task]:
        """Read and parse tasks from the JSON file"""
        
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                tasks = [Task(id=item["id"], payload=item["payload"]) for item in data]
            return tasks
        except Exception as e:
            raise ValueError(f"Error: {e}")


def run_tasks(source: TaskSource) -> list[Task]:
    """Validate the source implements TaskSource protocol and retrieve tasks from it"""

    if not isinstance(source, TaskSource):
        raise TypeError(f"{source} does not match contract TaskSource")
    
    return source.get_tasks()


