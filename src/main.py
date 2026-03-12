from typing import runtime_checkable, Protocol
from dataclasses import dataclass
import random, time, json, datetime
from src.constants import ALLOWED_STATUSES

# удалить description из payload


class IntegerRange:
    
    def __init__(self, min_value: int = 1, max_value: int = None):
        self.min_value = min_value
        self.max_value = max_value
    
    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name)
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError()
        if value < self.min_value:
            raise ValueError(f"Min value is {self.min_value}")
        if self.max_value and value > self.max_value:
            raise ValueError(f"Max value is {self.max_value}")
        
        setattr(instance, self.private_name, value)


class Task:
    """Unit of work with id and data payload"""

    __slots__ = ('_id', '_priority', '_status', '_created_at', 'payload')

    id = IntegerRange(min_value=1)
    priority = IntegerRange(min_value=1, max_value=5)
    payload: dict

    def __init__(self, id: int, description: str, priority: int, payload = None):
        self.payload = payload or {}
        self.id = id
        self.status = 'created'
        self.description = description
        self.priority = priority

        self._created_at = datetime.datetime.now()      

    def __repr__(self):
        return f"Task(id={self.id}, status='{self.status}', priority={self.priority}, description={self.description}, created_at={self.created_at})"  

    @classmethod
    def verify_status(cls, status):
        if not isinstance(status, str):
            raise TypeError('Status should be string')
        if status not in ALLOWED_STATUSES:
            raise ValueError('Unacceptable status')

    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, status):
        self.verify_status(status)
        self._status = status

    @classmethod
    def verify_description(cls, description):
        if not isinstance(description, str):
            raise TypeError('Description should be string')
        if len(description) <= 5:
            raise ValueError('Description must be at least 5 characters long')

    @property
    def description(self) -> str:
        return self.payload.get('description', '')
    
    @description.setter
    def description(self, description):
        self.verify_description(description)
        self.payload['description'] = description
    
    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at
    
    def __getattr__(self, name):
        if name in self.payload:
            return self.payload[name]
        
        raise AttributeError('No such attribute')
    
    @property
    def ready_to_start(self) -> bool:
        try:
            self.verify_description(self.description)
        
            return self._status == 'created'
        except (TypeError, ValueError):
            return False
    
    
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

        tasks = [Task(id=random.randint(1, 100), payload={"order_id": random.randint(1, 1000), "amount": random.randint(100, 1000)}, description='Task description', priority=random.randint(1, 5)) for i in range(random.randint(1, 5))]
        return tasks


class ApiTaskSource:
    """API stub that simulates an external task source"""

    def get_tasks(self) -> list[Task]:
        """Simulate API call to fetch tasks with a delay"""
        time.sleep(1)
        return [
            Task(id=101, payload={"order_id": random.randint(1001, 2000), "amount": random.randint(1000, 2000)}, description='Task description', priority=random.randint(1, 5)),
            Task(id=102, payload={"order_id": random.randint(1001, 2000), "amount": random.randint(1000, 2000)}, description='Task description', priority=random.randint(1, 5)),
            Task(id=103, payload={"order_id": random.randint(1001, 2000), "amount": random.randint(1000, 2000)}, description='Task description', priority=random.randint(1, 5)),
            Task(id=104, payload={"order_id": random.randint(1001, 2000), "amount": random.randint(1000, 2000)}, description='Task description', priority=random.randint(1, 5))
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
                tasks = [Task(id=item["id"], payload=item["payload"], description=item["payload"]["description"], priority=item["priority"]) for item in data]
            return tasks
        except Exception as e:
            raise ValueError(f"Error: {e}")


def run_tasks(source: TaskSource) -> list[Task]:
    """Validate the source implements TaskSource protocol and retrieve tasks from it"""

    if not isinstance(source, TaskSource):
        raise TypeError(f"{source} does not match contract TaskSource")
    
    return source.get_tasks()


