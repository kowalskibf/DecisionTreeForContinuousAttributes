# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

class Attribute:
    def __init__(self, name: str, continuous:bool=False, values:list=[]) -> None:
        self.name = name
        self.continuous = continuous
        self.values = values

    def value_included(self, value) -> bool:
        return value in self.values
    
    def __str__(self) -> str:
        if self.continuous:
            return f'Name: {self.name}, type: continuous'
        return f'Name: {self.name}, type: discrete, values: {" ".join(value for value in self.values)}'

class Record:
    def __init__(self, **kwargs) -> None:
        self.data = kwargs