import os
import numpy as np
from typing import TypeVar

# Remove a file if it exists
def rm(filename: str):
    if os.path.exists(filename):
        os.remove(filename)    

_copyable = TypeVar("_copyable")
def copy(obj: _copyable) -> _copyable:
    """Makes a deep copy via the dunder copy method in a class. If the parameter is a list, returns the recursive deep copy"""
    if isinstance(obj, int | float | str):
        return obj
    
    if isinstance(obj, list):
        return [copy(x) for x in obj] #type: ignore
    
    if isinstance(obj, tuple):
        return tuple(copy(x) for x in obj) #type: ignore
    
    if isinstance(obj, dict):
        return {copy(k): copy(v) for k, v in obj.items()} #type: ignore
    
    if isinstance(obj, np.ndarray):
        return np.array(obj, dtype = obj.dtype)
    
    if "__copy__" in dir(obj):
        return obj.__copy__() #type: ignore
    
    raise TypeError(f"Object of type {type(obj).__name__} is not copyable!")
