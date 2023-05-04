from abc import ABC, abstractmethod as virtual
from math import sin, cos
import random
from typing import Callable
from typing import Optional
from diagrams.git_colors import COLORS
from diagrams.user import GitUser
from diagrams.base import ReadMe
from diagrams.infoclass import ColorInfo, ChartInfo
from diagrams.util import copy

PI = 3.1415926

class PieChart(ReadMe):
    def __init__(self, chart_size: int, entries: list[ChartInfo], use_columns: bool = True, ignore_key: Callable[[ChartInfo, float], bool] | None = None): # type: ignore
        """Generates a pie chart in the markdown file. If use_columns is set to true, then legends are put in columns
        chart_size = Size of the chart on the html
        entries: List of Chart info entries to generate the chart
        use_columns: if set to true, then the legends are put on the side. Otherwise the legends are put at the bottom
        ignore_key: A callable function that ignore some entries and sweep them into the "Others" category. The lambda takes in
            the chart info c and the overall percentage f, returns a boolean on whether to make the entry represent in others. Default (None)
            is to not ignore any entries."""
        self.size = chart_size
        self.col = use_columns
        
        if ignore_key is None:
            ignore_key: Callable[[ChartInfo, float], bool] = lambda c, f: False
        
        self.sum_total = sum(v.amount for v in entries)
            
        self.entries = self.make_entries(entries, ignore_key)
        

    def make_entries(self, entries: list[ChartInfo], ignore_key: Callable[[ChartInfo, float], bool]):
        # We basically need to call ignore key here otherwise stuff down there will mess up
        ent: list[ChartInfo] = []
        other_sum = 0.
        for i, v in enumerate(entries):
            ratio = v.amount / self.sum_total
            if ignore_key(v, ratio):
                other_sum += v.amount
            else:
                ent.append(copy(v))
        
        ent.sort(key = lambda x: x.amount, reverse = True)
        ent.append(ChartInfo(other_sum, ColorInfo("#DEDEDE", "Others")))
        return ent
    
    def get_angles(self, a: float, mid_x: float, mid_y: float) -> tuple[float, float]:
        return mid_x + self.size//2 * sin(a), mid_y - self.size//2 * cos(a)
    
    def getPaths(self, mid_x: float, mid_y: float) -> tuple[list[str], int]:
        # Second loop to draw the chart
        paths = []
        
        last_angle = 0.
        
        # Keep track of the longest length to calculate the legend width
        longest_word_len = 0
        
        for i, v in enumerate(self.entries):
            ratio = v.amount / self.sum_total
            angle = 2 * PI * ratio
            
            # Calculate the new angles
            if i == len(self.entries) - 1:
                new_x, new_y = self.get_angles(0, mid_x, mid_y)
            else:
                new_x, new_y = self.get_angles(last_angle + angle, mid_x, mid_y)
            
            last_x, last_y = self.get_angles(last_angle, mid_x, mid_y)
            
            # There is a bug where if the ratio is larger than 0.5 in the pie chart
            # Then the path might be something unexpected.
            # To fix this we perform linear interpolation, to cover the distances:
            # 0 - 40%, 30 - 70%, 60 - 100%
            if ratio >= 0.49:
                f30_x, f30_y = self.get_angles(last_angle + 0.3 * angle, mid_x, mid_y)
                f40_x, f40_y = self.get_angles(last_angle + 0.4 * angle, mid_x, mid_y)
                f60_x, f60_y = self.get_angles(last_angle + 0.6 * angle, mid_x, mid_y)
                f70_x, f70_y = self.get_angles(last_angle + 0.7 * angle, mid_x, mid_y)
                paths += [
                    f'<path d="M{mid_x},{mid_y} L{last_x},{last_y} A{mid_x},{mid_y},0,0,1,{f40_x},{f40_y} Z" fill="{v.color.color}"></path>',
                    f'<path d="M{mid_x},{mid_y} L{f30_x},{f30_y} A{mid_x},{mid_y},0,0,1,{f70_x},{f70_y} Z" fill="{v.color.color}"></path>',
                    f'<path d="M{mid_x},{mid_y} L{f60_x},{f60_y} A{mid_x},{mid_y},0,0,1,{new_x},{new_y} Z" fill="{v.color.color}"></path>'
                ]
            else:
                paths.append(
                    f'<path d="M{mid_x},{mid_y} L{last_x},{last_y} A{mid_x},{mid_y},0,0,1,{new_x},{new_y} Z" fill="{v.color.color}"></path>'
                )
            
            # To minimize black borders for adjacent similar colors
            last_angle += angle - 0.005
            
            longest_word_len = max(longest_word_len, len(v.color.name))
        
        return paths, longest_word_len

    def getChart(self, paths: list[str]):
        # Use an HTML table to display the pie chart along with the legend
        chart = f'<div id="shape">\n\t<svg height="{self.size}" width="{self.size}">\n'
        chart += "\n".join([f"\t\t{p}" for p in paths])
        chart += '\n\t</svg>\n</div>'
        return chart
    
    def getVerticalLegend(self) -> list[str]:
        legends = [f'<p><span style="background-color: {v.color.color};">&nbsp; &nbsp;</span> {v.color.name}: {round(v.amount / self.sum_total * 100, 2)}%</p>' for v in self.entries]
        return legends
    
    def getSVGLegends(self) -> list[str]:
        legends = []
        for v in self.entries:
            bgColor = v.color.color
            textColor = "#ffffff" if v.color.isDark() else "#000000"
            l = f'<p><span style="background-color: {bgColor}; color: {textColor}">{v.color.name}</span>: {round(v.amount / self.sum_total * 100, 2)}%</p>'
            legends.append(l)
        return legends
    
    def getHorizontalLegend(self, entriesPerRow: int, padding: int) -> list[str]:
        legends = []
        currRow = ""
        for i, v in enumerate(self.entries):
            ratio = v.amount / self.sum_total
            mock_text = f"    {v.color.name}: {round(ratio * 100, 2)}%"
            currRow += f'<span style="background-color: {v.color.color};">&nbsp; &nbsp;</span> {v.color.name}: {round(ratio * 100, 2)}%'
            currRow += "&nbsp; " * (padding - len(mock_text))
            if i % entriesPerRow == entriesPerRow - 1 or i == len(self.entries) - 1:
                legends.append(f'<p>{currRow}</p>')
                currRow = ""
        return legends
    
    @property
    def content(self):
        """Content may not work on some SVG (for example GitHub ones). A compromise is to export the graph
        as an svg and then include the image in your Read Me. Use PieChart.exportAsSVG(filepath) for that."""
        paths, longest_word_length = self.getPaths(self.size // 2, self.size // 2)
        chart = self.getChart(paths)
        
        if self.col:
            legend = self.getVerticalLegend()
            
            # Finish the table in HTML format
            height = 18
            chart_width = 100
            legend_width = 20 * longest_word_length + 100
            
            table = f"""\
<table style="height: {height}px; width: {chart_width + legend_width}px; border-collapse: collapse; border-style: hidden;" border="1">
<tbody>
<tr style="height: {height}px;">
    <td style="width: {chart_width}px; height: {height}px;">
{chart}
    </td>
    <td style="width: {legend_width}px; height: {height}px;">
{legend}
    </td>
</tr>
</tbody>
</table>"""
        else:
            legend = self.getHorizontalLegend(3, longest_word_length + 10)
            table = f"{chart}\n{legend}"""
        
        return table
    
    def exportAsSVG(self, relativePath: str, hyperlink: str = "") -> ReadMe:
        class SVGReadMe(ReadMe):
            pass
        svgReadMe = SVGReadMe(f"![{hyperlink}]({relativePath})")
        
        # Create the svg object
        paths, longest_word = self.getPaths(self.size//2, self.size//2)
        path = "\n".join(f"\t{p}" for p in paths)
        
        legends = self.getSVGLegends()
        legend = "\n".join(f"\t\t{p}" for p in legends)
        
        width = self.size + 25 * longest_word
        height = max(35 * len(self.entries), self.size)
        svgHeightOffset = max((height - self.size) / 2, 0)
        
        svg = f"""\
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<svg x="0" y="{svgHeightOffset}" height="{self.size}" width="{self.size}">
{path}
</svg>
<foreignObject x="{self.size + 30}" y="0" width="{width - self.size}" height="{height}">
    <div xmlns="http://www.w3.org/1999/xhtml">
{legend}
    </div>
</foreignObject>
</svg>
"""
        with open(relativePath, 'w') as f:
            f.write(svg)
        
        return svgReadMe

class GitPieChart(PieChart):
    def __init__(self, user: GitUser, chart_size: int = 150, use_columns: bool = False, ignore_key: Callable[[ChartInfo, float], bool] | None = None):
        """Process all the repo information and creates the language pie chart for you
        This is the wrapper class to generate it"""
        entries: list[ChartInfo] = []
        for language, num_bytes in user.total_languages.items():
            color = COLORS.get(language)
            if color:
                entries.append(ChartInfo(num_bytes, color))
        return super().__init__(chart_size, entries, use_columns, ignore_key)
