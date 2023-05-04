## This file contains the base classes for read mes
## The main idea is that everything is inherited from the ReadMe class
## This class contains the "add" mutator method (which allows method chaining)
## and contains the "export" method. These two methods allow for customization of
## the markdown file like arranging subfiles

from __future__ import annotations
import os
import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Generator, Optional
from abc import ABC, abstractmethod as virtual
from datetime import datetime
from diagrams.util import rm

class ReadMe:
    """This wrapper class generates the read me file"""    
    def __init__(self, content = ""):
        self._content = content
    
    def add(self, *contents: ReadMe, newline: bool = False):
        """Add contents to read me. If the newline variable is set to true, then add a newline character between every readme content"""
        for c in contents:
            if isinstance(c, ReadMe):
                self._content += c.content
            if newline:
                self._content += "\n"
        return self
    
    @property
    def content(self) -> str:
        return self._content
    
    ## Overload for convenience in print statements
    def __repr__(self):
        return self.content    

    def export(self, path: str):
        # Delete the existing read me file
        rm(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.content)
            
    def __copy__(self) -> ReadMe:
        return ReadMe(self._content)

class Tagged(ReadMe):
    def __init__(self, content: str, tag: str, info: str):
        self._content = content
        self.tag = tag
        self.info = info 
        
    @property
    def content(self):
        return f'<{self.tag} {self.info}>{self._content}</{self.tag}>'
    
    def __copy__(self):
        return Tagged(self.content, self.tag, self.info)
   
class Point(ReadMe):
    @property
    def content(self):
        return f"- {self._content}"
    
class Hyperlink(ReadMe):
    def __init__(self, text: str, url: str):
        self.text = text
        self.url = url
    
    @property
    def content(self):
        return f"[{self.text}]({self.url})"
    
    def __copy__(self):
        return Hyperlink(self.text, self.url)
    
class Image(ReadMe):
    def __init__(self, linkurl: str, imageurl: str, alttext: Optional[str] = None):
        self.imageurl = imageurl
        self.linkurl = linkurl
        self.alttext = alttext if alttext else linkurl
    
    @property
    def content(self):
        return f'<a href="{self.linkurl}" target="blank"><img align="center" src="{self.imageurl}" alt="{self.alttext}" height="30" width="40" /></a>'

    def __copy__(self):
        return Image(self.linkurl, self.imageurl, self.alttext)

class CurrentDate(ReadMe):
    def __init__(self):
        pass
        
    @property
    def content(self) -> str:
        return datetime.now().strftime("%d/%m/%Y")

class CurrentTime(ReadMe):
    def __init__(self):
        pass
        
    @property
    def content(self) -> str:
        return datetime.now().strftime("%H:%M:%S")
