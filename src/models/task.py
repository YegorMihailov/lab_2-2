import datetime
from ..descriptors import IntegerRange
from ..constants import ALLOWED_STATUSES


class Task:
    """Unit of work with id, data payload, status, priority, and time created at"""

    __slots__ = ('_id', '_priority', '_status', '_created_at', 'payload')

    id = IntegerRange(min_value=1)
    priority = IntegerRange(min_value=1, max_value=5)
    payload: dict

    def __init__(self, id: int, description: str, priority: int, payload = None):
        """Initialize Task instance and validate its attributes"""

        self.payload = payload or {}
        self.id = id
        self.status = 'created'
        self.description = description
        self.priority = priority

        self._created_at = datetime.datetime.now()      

    def __repr__(self):
        """Return a string representation of the Task"""

        return f"Task(id={self.id}, status='{self.status}', priority={self.priority}, description={self.description}, created_at={self.created_at})"  

    @classmethod
    def verify_status(cls, status):
        """Validate the provided status"""

        if not isinstance(status, str):
            raise TypeError('Status should be string')
        if status not in ALLOWED_STATUSES:
            raise ValueError('Unacceptable status')

    @property
    def status(self) -> str:
        """Get the current status of the task"""

        return self._status
    
    @status.setter
    def status(self, status: str):
        """Set the task status after validation"""

        self.verify_status(status)
        self._status = status

    @classmethod
    def verify_description(cls, description):
        """Validate the description of the task"""

        if not isinstance(description, str):
            raise TypeError('Description should be string')
        if len(description) <= 5:
            raise ValueError('Description must be at least 5 characters long')

    @property
    def description(self) -> str:
        """Retrieve the description from payload"""

        return self.payload.get('description', '')
    
    @description.setter
    def description(self, description: str):
        """Validate the description and store it in payload"""

        self.verify_description(description)
        self.payload['description'] = description
    
    @property
    def created_at(self) -> datetime.datetime:
        """Get the task timestamp"""

        return self._created_at
    
    def __getattr__(self, name):
        """Provide dynamic access to keys stored in payload"""

        if name in self.payload:
            return self.payload[name]
        
        raise AttributeError('No such attribute')
    
    @property
    def ready_to_start(self) -> bool:
        """Determine if the task is ready to be start"""

        try:
            self.verify_description(self.description)
        
            return self._status == 'created'
        except (TypeError, ValueError):
            return False