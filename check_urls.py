import requests

urls_to_check = [
    ("Intel (for Tesseract)", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/intel/intel-original.svg"),
    ("PaddlePaddle", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/paddlepaddle/paddlepaddle-original.svg"),
    ("WinMerge", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/winmerge/winmerge-original.svg"), # Guess
    ("Draw.io", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/drawio/drawio-original.svg"), # Guess
    ("Lightroom", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/lightroom/lightroom-original.svg"), # Guess
    ("Cinema 4D", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cinema4d/cinema4d-original.svg"), # Guess
    ("Unity", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/unity/unity-original.svg"),
    ("Rhinoceros", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rhinoceros/rhinoceros-original.svg"), # Guess
    ("Blender", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/blender/blender-original.svg"),
     ("Matlab", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/matlab/matlab-original.svg"),
]

for name, url in urls_to_check:
    try:
        r = requests.head(url, timeout=2)
        if r.status_code == 200:
            print(f"[FOUND] {name}: {url}")
        else:
            print(f"[MISSING] {name} ({r.status_code})")
    except Exception as e:
        print(f"[ERROR] {name}: {e}")
