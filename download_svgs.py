import requests
import os

SRC_DIR = "icons_src"
if not os.path.exists(SRC_DIR):
    os.makedirs(SRC_DIR)

targets = [
    ("c", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/c/c-original.svg"),
    ("cpp", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg"),
    ("boost", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/boost/boost-original.svg"),
    ("opencv", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/opencv/opencv-original.svg"),
    ("unreal5", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/unrealengine/unrealengine-original.svg"),
    ("python", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg"),
    ("flask", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original.svg"),
    ("java", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg"),
    ("spring", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/spring/spring-original.svg"),
    ("dart", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/dart/dart-original.svg"),
    ("flutter", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flutter/flutter-original.svg"),
    ("html5", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg"),
    ("mysql", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg"),
    ("postgresql", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg"),
    ("git", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original.svg"),
    ("github", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original.svg"),
    ("figma", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/figma/figma-original.svg"),
    ("visualstudio", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/visualstudio/visualstudio-original.svg"),
    ("vscode", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vscode/vscode-original.svg"),
    ("rider", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jetbrains/jetbrains-original.svg"),
    ("androidstudio", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/androidstudio/androidstudio-original.svg"),
    ("photoshop", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/photoshop/photoshop-original.svg"),
    ("illustrator", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/illustrator/illustrator-original.svg"),
    ("premiere", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/premierepro/premierepro-original.svg"),
    ("aftereffects", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/aftereffects/aftereffects-original.svg"),
    ("blender", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/blender/blender-original.svg"),
    ("notion", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/notion/notion-original.svg"),
    # Simple Icons fallbacks
    ("tesseract", "https://cdn.simpleicons.org/tesseract/white"),
    ("synology", "https://cdn.simpleicons.org/synology/white"),
    ("winmerge", "https://cdn.simpleicons.org/winmerge/white"),
    ("drawio", "https://cdn.simpleicons.org/diagramsdotnet/white"),
    ("visualbasic", "https://cdn.simpleicons.org/visual-basic/white"),
    ("excel", "https://cdn.simpleicons.org/microsoft-excel/white"),
    ("paddle-ocr", "https://cdn.simpleicons.org/paddlepaddle/white"),
    ("windbg", "https://cdn.simpleicons.org/microsoft/white"),
    ("qnet", "https://cdn.simpleicons.org/googlefit/white"),
    ("sqld", "https://cdn.simpleicons.org/sqlite/white"),
    ("antigravity", "https://cdn.simpleicons.org/rocket/white"), 
    ("context7", "https://cdn.simpleicons.org/googledocs/white"),
    ("sequentialthinking", "https://cdn.simpleicons.org/steps/white"),
    ("lightroom", "https://cdn.simpleicons.org/adobe-lightroom/white"),
    ("c4d", "https://cdn.simpleicons.org/cinema4d/white"),
    ("rhino", "https://cdn.simpleicons.org/rhinoceros/white"),
    ("keyshot", "https://cdn.simpleicons.org/luxion/white"),
    ("tesseract", "https://cdn.simpleicons.org/tesseract/white"),
    ("playwright", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/playwright/playwright-original.svg"),
]

for slug, url in targets:
    try:
        print(f"Downloading {slug} from {url}...")
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            ext = ".svg"
            with open(os.path.join(SRC_DIR, f"{slug}{ext}"), "wb") as f:
                f.write(r.content)
            print(f"  Successfully saved {slug}{ext}")
        else:
            print(f"  Failed with status code {r.status_code}")
    except Exception as e:
        print(f"  Error: {e}")

print("Done.")
