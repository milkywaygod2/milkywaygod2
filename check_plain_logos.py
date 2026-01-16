import requests

def check_url(name, base_slug, variant):
    url = f"https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/{base_slug}/{base_slug}-{variant}.svg"
    try:
        r = requests.head(url, timeout=2)
        if r.status_code == 200:
            print(f"[FOUND] {name} ({variant}): {url}")
            return True
        else:
            print(f"[MISSING] {name} ({variant})")
            return False
    except:
        return False

# Suspects for "Dark on Dark" issues
suspects = [
    ("photoshop", "photoshop"),
    ("illustrator", "illustrator"),
    ("premiere", "premierepro"),
    ("aftereffects", "aftereffects"),
    ("visualstudio", "visualstudio"), # Ribbon is purple
    ("c", "c"), # Light blue?
    ("python", "python"), # Blue/Yellow
    ("blender", "blender"),
]

for name, slug in suspects:
    check_url(name, slug, "plain")
    check_url(name, slug, "original")
