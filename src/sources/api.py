import time
import random
from src.models import Task

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