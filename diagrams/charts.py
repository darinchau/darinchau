from __future__ import annotations
from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
from diagrams.base import ReadMe
from diagrams.user import GitUser
from diagrams.infoclass import ChartInfo, ColorInfo
from diagrams.git_colors import COLORS
import json

def gen_github_info(user: GitUser, ignore_key: Callable[[ChartInfo, float], bool]):
    # Set keys to ignore
    if ignore_key is None:
        ignore_key = lambda c, f: False
    
    # Get all the language infos
    entries: list[tuple[ChartInfo, float]] = []
    other_bytes = 0
    for language, num_bytes in user.total_languages.items():
        color = COLORS.get(language)
        if color is None:
            other_bytes += num_bytes
            continue

        info = ChartInfo(num_bytes, color)
        percentage_in_repo = num_bytes / user.total_bytes
        if ignore_key(info, percentage_in_repo):
            other_bytes += num_bytes
            continue

        entries.append((info, percentage_in_repo))
    
    # Finalize entries and sort them
    # Reverse the entries because we want a clockwise pie chart
    entries.sort(key = lambda x: x[0].amount, reverse = True)
    entries.append((ChartInfo(other_bytes, ColorInfo("#AAAAAA", "Others")), other_bytes/user.total_bytes))
    entry = [x.amount for x, _ in entries]
    label = [f"{x.color.name}: {percentage * 100:.2f}%" for x, percentage in entries]
    color = [x.color.color for x, _ in entries]
    return entry, color, label


def gen_leetcode_info(user: GitUser):
    # Load leetcode repo
    leetcode = None
    for repo in user.repos:
        if repo.full_name == "darinchau/my-leet-code-submissions":
            leetcode = repo
            break
    if leetcode is None:
        raise AssertionError("Cannot find leet code repository")
    x = leetcode.get_contents("stats.json").decoded_content
    js = json.loads(x.decode())
    
    # Sort the submissions according to language
    submissions: dict[str, tuple[ColorInfo, list[tuple[float, float]]]] = {}
    for entries in js['submissions']:
        language: str = entries['language']
        color = COLORS.get(language)
        if color is None:
            color = ColorInfo("#AAAAAA", "Others")
            language = "Others"
        try:
            submissions[language][1].append((entries['runtime'], entries['memory']))
        except KeyError:
            submissions[language] = (color, [(entries['runtime'], entries['memory'])])
            
    return submissions

# This builds on the diagrams base thing and creates the chart
class Charts(ReadMe):
    def __init__(self, user: GitUser, hyperlink: str, relative_path: str, ignore_key: Callable[[ChartInfo, float], bool] | None = None):
        """Process all the repo information and creates the language pie chart for you
        This is the wrapper class to generate it"""

        pie_entries, pie_color, pie_labels = gen_github_info(user, ignore_key)
        submissions = gen_leetcode_info(user)

        
        # Here is the pie chart
        pie_ax: plt.Axes
        leet_ax: plt.Axes
        fig, (pie_ax, leet_ax) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 4]})
        pie_ax.pie(pie_entries, colors = pie_color, startangle = 90, counterclock=False)
        pie_ax.set_axis_off()
        pie_ax.set_title("My Github stats")
        # box = pie_ax.get_position()
        # pie_ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
        # pie_ax.legend(pie_labels, loc='center left', bbox_to_anchor=(1, 0.5))
        pie_ax.legend(pie_labels, bbox_to_anchor=(1,0), loc="lower left")

        # Here is the leet code scatter
        for lang, (color, subs) in submissions.items():
            x = [s[0] for s in subs]
            y = [s[1] for s in subs]
            leet_ax.scatter(x, y, c=color.color, alpha=0.7, label = lang)
        leet_ax.set_ylabel("Memory")
        leet_ax.set_xlabel("Runtime")
        leet_ax.set_ylim(0, 110)
        leet_ax.set_xlim(0, 110)
        leet_ax.set_xticks([0, 20, 40, 60, 80, 100])
        leet_ax.set_yticks([0, 20, 40, 60, 80, 100])
        leet_ax.legend(loc='lower left', fontsize=9)
        leet_ax.set_aspect('equal', adjustable='box')
        leet_ax.set_title('LeetCode Submission')

        fig.tight_layout()

        fig.savefig(relative_path, bbox_inches='tight')
        self._content = f"![{hyperlink}]({relative_path})"