import random
from src.models import Task

class GeneratorTaskSource:
    """Task source that creates random task objects"""

    def get_tasks(self) -> list[Task]:
        """Generate random tasks"""

        tasks = [Task(id=random.randint(1, 100), payload={"order_id": random.randint(1, 1000), "amount": random.randint(100, 1000)}, description='Task description', priority=random.randint(1, 5)) for i in range(random.randint(1, 5))]
        return tasks