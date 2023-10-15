## This file contains all the colors of github-supported languages

import os
import re
from diagrams.infoclass import ColorInfo
from diagrams.util import copy, rm
import yaml
import re
import requests

URL = "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml"

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
    colorinfos: dict[str, GitLanguageInfo]
    def __new__(cls):
        if ColorContainer.instance is not None:
            return ColorContainer.instance
        
        self = super().__new__(cls)

        # Gets content from the language thing database from github themselves
        response = requests.get(URL)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to retrieve YAML content. Status code: {response.status_code}")
        
        yml_content = response.text
        dic: dict[str, dict] = yaml.safe_load(yml_content)
        
        colorinfos: dict[str, GitLanguageInfo] = {}
        
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

    def get(self, x) -> GitLanguageInfo:
        return self.colorinfos[x]

COLORS = ColorContainer()
