from __future__ import annotations
from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
from diagrams.base import ReadMe
from diagrams.infoclass import ChartInfo, ColorInfo
import json
from diagrams.git import GitUser, gen_github_info
from diagrams.leetcode import get_all_submission_details, SubmissionDetail

# This builds on the diagrams base thing and creates the chart
class Charts(ReadMe):
    def __init__(self, user: GitUser, hyperlink: str, relative_path: str, ignore_key: Callable[[ChartInfo, float], bool] | None = None):
        """Process all the repo information and creates the language pie chart for you
        This is the wrapper class to generate it"""

        pie_entries, pie_color, pie_labels = gen_github_info(user, ignore_key)
        submissions = get_all_submission_details()
        
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
        submit_languages = {}
        for detail in submissions:
            if (detail.language, detail.color) not in submit_languages:
                submit_languages[(detail.language, detail.color)] = []
            submit_languages[(detail.language, detail.color)].append((detail.memory_percentile, detail.runtime_percentile))

        for k, v in submit_languages.items():
            leet_ax.scatter([x[0] for x in v], [x[1] for x in v], label=k[0], color=k[1], alpha=0.7)
        
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
