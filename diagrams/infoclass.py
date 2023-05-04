from __future__ import annotations
import random
from collections import namedtuple
from diagrams.util import copy

class ChartInfo:
    __slots__ = ("amount", "color")
    def __init__(self, amount: float, color: ColorInfo) -> None:
        self.amount = amount
        self.color = color
        
    def __copy__(self):
        return ChartInfo(self.amount, copy(self.color))

class ColorInfo:
    """Color is the hex code of the color, name is the entry in the chart with said color
    For example, ColorInfo("#FF0000", "Hiya!") will give you an entry in the chart, with red plots and name 'Hiya!'"""
    def __init__(self, color: str, name: str):
        self.color = color
        self.name = name
    
    @classmethod
    def random(cls, name: str, *, lower_bound: int = 0, upper_bound: int = 255) -> ColorInfo:
        """Generate a random color for testing purposes
        lower bound and upper bound are bounds for the color values to prevent generating colors that are too bright or too dim"""
        r = str(hex(random.randint(lower_bound, upper_bound)))[2:]
        g = str(hex(random.randint(lower_bound, upper_bound)))[2:]
        b = str(hex(random.randint(lower_bound, upper_bound)))[2:]
        color = f"#{r}{g}{b}"
        return cls(color, name)
    
    def isDark(self, threshold: float = 0.65):
        r = int(self.color[1:3], base = 16)
        g = int(self.color[3:5], base = 16)
        b = int(self.color[5:7], base = 16)
        return 0.299 * r + 0.587 * g + 0.114 * b <= threshold * 255
    
    def __copy__(self):
        return ColorInfo(self.color, self.name)
