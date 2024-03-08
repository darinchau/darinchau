## This file is run every time we perform a commit
## The main purpose of this file is to:
## 1. Manage the diagrams more clearly
## 2. Dynamically create the ReadMe
## 3. Redraw the pie chart

from __future__ import annotations
from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
from diagrams.base import Image, ReadMe, Tagged, Point, Hyperlink, CurrentDate
from diagrams.images import dev
from diagrams.git import GitUser
from diagrams.infoclass import ChartInfo, ColorInfo
from diagrams.charts import Charts
import json
import subprocess

linkedin = Image("https://linkedin.com/in/darinchauyf", "https://raw.githubusercontent.com/darinchau/darinchau/c2e538bb063a2b8077212ada96dead8d42fd3866/icons/linked%20in.svg", "LinkedIn")
instagram = Image("https://www.instagram.com/dc.darin/", "https://raw.githubusercontent.com/darinchau/darinchau/main/icons/instagram.svg", "Instagram @dc.darin")
leetcode = Image("https://leetcode.com/darinchau/", "https://raw.githubusercontent.com/darinchau/darinchau/main/icons/leetcode.svg", "LeetCode")

H1 = "h1"
CENTER = 'align="center"'
H3 = "h3"
LEFT = 'aligh="left"'

def generate():
    # Get the user
    piepath = './icons/pie.svg'
    with open('./github.privatekey', 'r') as f:
        token = f.read() 
        user = GitUser(token)
    
    # Languages to ignore (stash into "Other")
    def ignore(c: ChartInfo, f: float):
        if c.color.name in ["ShaderLab", "HLSL", "Mathematica", "Batchfile", "Ruby"]:
            return True
        if f < 0.01:
            return True
        return False

    readme = ReadMe().add(
        Tagged("Hi, I'm Darin Chau", H1, CENTER),
        Tagged("Undergraduate software developer from HKUST", H3, CENTER),
        ReadMe(),
        Point("🏫 I'm a student in Mathematics and Computer Science (Hong Kong University of Science and Technology)"),
        Point("🌱 I'm currently learning **Hugging Face Libraries**, **NoSQL databases**"),
        Point("🔎 I have conducted research work in Mathematics (Cluster algebra) and Computer Science (CNN Crowd Counting)"),
        Point("🎹 I am proficient at piano performance **(DipABRSM)**"),
        ReadMe(),
        Tagged("Connect with me:", H3, LEFT),
        Tagged("", "p", LEFT).add(
            linkedin,
            instagram,
            leetcode
        ),
        ReadMe(),
        Tagged("Languages and tools:", H3, LEFT),
        Tagged("", "p", LEFT).add(
            dev.angular,
            dev.c,
            dev.cpp,
            dev.html,
            dev.css,
            dev.javascript,
            dev.nodejs,
            dev.opencv,
            dev.pandas,
            dev.python,
            dev.react,
            dev.reactnative,
            dev.rust,
            dev.scala,
            dev.seaborn,
            dev.tensorflow,
            dev.unity,
        ),
        ReadMe(),
        ReadMe("### My Stats:"),
        Charts(user, "https://github.com/darinchau/markdown-generator", piepath, ignore_key=ignore),
        ReadMe(),
        ReadMe("Last updated: ").add(
            CurrentDate()
        ),
        newline = True
    )
    
    readme.export("./README.md")
    
def github() -> None:
    print("Doing github commit")
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "update pie"])
    subprocess.call(["git", "push", "origin", "main"])
    return

if __name__ == "__main__":
    generate()
    # github()
