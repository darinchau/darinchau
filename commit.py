## This file is run every time we perform a commit
## The main purpose of this file is to:
## 1. Manage the diagrams more clearly
## 2. Dynamically create the ReadMe
## 3. Redraw the pie chart

## This uses the markdown generator library on https://github.com/darinchau/markdown-generator

from MDgen import Image, ReadMe, Tagged, Point, Hyperlink, CurrentDate
from MDgen.profile import dev, GitPieChart, GitUser

linkedin = Image("https://linkedin.com/in/darinchauyf", "https://raw.githubusercontent.com/darinchau/darinchau/c2e538bb063a2b8077212ada96dead8d42fd3866/icons/linked%20in.svg", "LinkedIn")
instagram = Image("https://www.instagram.com/dc.darin/", "https://raw.githubusercontent.com/darinchau/darinchau/main/icons/instagram.svg", "Instagram @dc.darin")
leetcode = Image("https://leetcode.com/darinchau/", "https://raw.githubusercontent.com/darinchau/darinchau/main/icons/leetcode.svg", "LeetCode")

H1 = "h1"
CENTER = 'align="center"'
H3 = "h3"
LEFT = 'aligh="left"'

def generate():
    piepath = './icons/pie.svg'
    with open('./github.privatekey', 'r') as f:
        token = f.read() 
        user = GitUser(token)
    with open(piepath, 'w') as f:
        f.write(f"""\
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
<foreignObject width="100" height="100">
    <div xmlns="http://www.w3.org/1999/xhtml">
        {GitPieChart(user, use_columns=True).content}
    </div>
</foreignObject>
</svg>
""")
    
    readme = ReadMe().add(
        Tagged("Hi, I'm Darin Chau", H1, CENTER),
        Tagged("Undergraduate software developer from HKUST", H3, CENTER),
        ReadMe(),
        Point("🏫 I'm a student in Mathematics and Computer Science (Hong Kong University of Science and Technology)"),
        Point(f'📄 Know about ').add(
            Hyperlink("my experiences", "https://github.com/darinchau/darinchau/blob/main/latex/Resume.pdf")
        ),
        Point("🌱 I'm currently learning **SQL, Rust full-stack development**"),
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
            dev.seaborn,
            dev.tensorflow,
            dev.typescript,
            dev.unity,
            dev.vue
        ),
        ReadMe(),
        ReadMe("### My Github stats:").add(
            Hyperlink("Github stats:", "https://github.com/darinchau/markdown-generator")
        ),
        Image("https://github.com/darinchau/markdown-generator", piepath, "Github stats"),
        ReadMe("Last updated: ").add(
            CurrentDate()
        ),
        newline = True
    )
    
    readme.export("./README.md")
    
if __name__ == "__main__":
    generate()