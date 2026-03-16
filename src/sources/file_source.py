import json
from src.models import Task

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