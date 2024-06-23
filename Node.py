# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

from Attribute import *

class Node:
    def __init__(self, attribute:Attribute=None, is_value_continuous:bool=False, value:str=None, branches:list=[], is_terminal:bool=False, result:str=None) -> None:
        self.attribute = attribute
        self.is_value_continuous = is_value_continuous
        self.value = value
        self.branches = branches
        self.is_terminal = is_terminal
        self.result = result

    def __str__(self, level=0):
        if self.is_terminal:
            return f'{"  " * level}Attribute: {self.attribute}, Value: {self.value}, Result: {self.result}\n'
        result = f'{"  " * level}Attribute: {self.attribute}, Value: {self.value}\n'
        for branch in self.branches:
            result += branch.__str__(level + 1)
        return result
    
    def __del__(self):
        del self.attribute, self.is_value_continuous, self.value, self.is_terminal, self.result, self.branches