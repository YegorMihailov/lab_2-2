class IntegerRange:
    """Data descriptor that validates if integer falls within a specified range"""
    
    def __init__(self, min_value: int = 1, max_value: int = None):
        """Initialize the descriptor with minimum and optional maximum values"""

        self.min_value = min_value
        self.max_value = max_value
    
    def __set_name__(self, owner, name):
        """Set the private attribute name"""

        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        """Retrieve value from instance or return the descriptor if accessed via class"""

        if instance is None:
            return self
        return getattr(instance, self.private_name)
    
    def __set__(self, instance, value):
        """Сheck the value within the range and set the value"""

        if not isinstance(value, int):
            raise TypeError()
        if value < self.min_value:
            raise ValueError(f"Min value is {self.min_value}")
        if self.max_value and value > self.max_value:
            raise ValueError(f"Max value is {self.max_value}")
        
        setattr(instance, self.private_name, value)


