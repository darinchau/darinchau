## This file contains all the colors of github-supported languages
## Auto generated by ./make_colors.py ##
## YAML file obtained at https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml ##

import os
import re
from diagrams.infoclass import ColorInfo
from diagrams.util import copy, rm
import yaml
import re

class GitLanguageInfo(ColorInfo):
    def __init__(self, color: str, name: str, extension: list[str], language_type: str, language_id: int):
        self.color = color
        self.name = name
        self.lang_type = language_type
        self.id = language_id
        self.ext = copy(extension)

# Singleton object to hold all the git colors
class ColorContainer:
    instance = None
    def __new__(cls):
        if ColorContainer.instance is not None:
            return ColorContainer.instance
        
        self = super().__new__(cls)

        with open("./diagrams/languages.yml", 'r') as f:
            dic: dict[str, dict] = yaml.safe_load(f)
        
        colorinfos = {}
        
        for k, v in dic.items():
            try:
                colorinfos[k] = GitLanguageInfo(
                    color = v['color'],
                    language_type = v['type'],
                    language_id = v['language_id'],
                    name = k,
                    extension = v['extensions']
                )
            except KeyError:
                continue
        
        self.colorinfos = colorinfos
        ColorContainer.instance = self
        return self
    
    def get(self, x):
        return self.colorinfos[x]

COLORS = ColorContainer()