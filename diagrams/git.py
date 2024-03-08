## This file is responsible for retreiving information from github and generating the Github pie chart

from github import Github
from github.Repository import Repository
import threading
from queue import Queue
import os
import re
from diagrams.infoclass import ColorInfo
from diagrams.util import copy, rm
import yaml
from typing import Callable
from diagrams.infoclass import ChartInfo, ColorInfo
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

class GitUser:
    def __init__(self, auth_token: str):
        """A git user is responsible for getting all the repos and languages of the user"""
        self.g = Github(auth_token)
        usr = self.g.get_user()
        self.repos = list(usr.get_repos())

        # Create the language information here
        result_queue = Queue()
        threads = []

        with open("diagrams/forks.txt", 'r') as f:
            forks = f.readlines()
        forks = [f.strip() for f in forks]

        def process_repo(repo: Repository):
            if repo.owner.name != usr.name:
                return
            if repo.name in forks:
                return
            print("    " + repo.name)
            # stats = repo.get_stats_contributors()
            # if stats is not None:
            #     first_author = stats[0].author
            #     if first_author.name != usr.name:
            #         return
            for k, v in repo.get_languages().items():
                # Artificially cut off Jupyter because it is just python and it tends to be THICC
                if k == "Jupyter Notebook":
                    k = "Python"
                    v *= .5
                result_queue.put((k, v))

        # Use multithreading because we make soooo many request calls inside process repo
        print("The following repos will be counted:")
        for repo in self.repos:
            thread = threading.Thread(target=process_repo, args=(repo,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # Process the language info to expose to other modules
        self._total_languages: dict[str, int] = {}
        self._total_bytes = 0

        while not result_queue.empty():
            k, v = result_queue.get()
            self._total_languages[k] = self._total_languages.get(k, 0) + v
            self._total_bytes += v

    @property
    def total_bytes(self):
        """Total number of bytes of code in the repo"""
        return self._total_bytes
    
    def __getitem__(self, k):
        """Total number of languages"""
        return self._total_languages.get(k, 0)
    
    def languages(self):
        return sorted(self._total_languages.items(), key=lambda x: x[1], reverse=True)
    
def gen_github_info(user: GitUser, ignore_key: Callable[[ChartInfo, float], bool]):
    """This takes a git user object and a boolean function that takes in a ChartInfo and a percentage to determine whether the language should be included in "Others"
    This will return
        entry: list[float] - the amount of bytes for each language
        color: list[str] - the color of each language
        label: list[str] - the label for each language"""
    # Set keys to ignore
    if ignore_key is None:
        ignore_key = lambda c, f: False
    
    # Get all the language infos
    entries: list[tuple[ChartInfo, float]] = []
    other_bytes = 0
    print("There are these languages:")
    for language, num_bytes in user.languages():
        percentage_in_repo = num_bytes / user.total_bytes
        print(f"    {language}: {round(percentage_in_repo*100, 2)}%")

        color = COLORS.get(language)
        if color is None:
            other_bytes += num_bytes
            continue

        info = ChartInfo(num_bytes, color)
        if ignore_key(info, percentage_in_repo):
            other_bytes += num_bytes
            continue

        entries.append((info, percentage_in_repo))
    
    # Finalize entries and sort them
    # Reverse the entries because we want a clockwise pie chart
    entries.sort(key = lambda x: x[0].amount, reverse = True)
    entries.append((ChartInfo(other_bytes, ColorInfo("#AAAAAA", "Others")), other_bytes/user.total_bytes))

    # Artificially cut the number of entries to 8
    while len(entries) > 8:
        last = entries.pop(-2)
        entries[-1] = (ChartInfo(entries[-1][0].amount + last[0].amount, entries[-1][0].color), entries[-1][1] + last[1])
    
    entry = [x.amount for x, _ in entries]
    label = [f"{x.color.name}: {percentage * 100:.2f}%" for x, percentage in entries]
    color = [x.color.color for x, _ in entries]
    return entry, color, label
