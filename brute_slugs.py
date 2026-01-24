import requests
import os

SRC_DIR = "icons_src"

missing_ones = {
    "winmerge": ["winmerge", "win-merge"],
    "tesseract": ["tesseract", "tesseractocr", "tesseract-ocr"],
    "excel": ["microsoftexcel", "microsoft-excel", "excel"],
    "visualbasic": ["visualbasic", "visual-basic", "vb"],
    "cinema4d": ["cinema4d", "cinema-4d", "c4d"],
    "rhino": ["rhinoceros", "rhino"],
    "lightroom": ["adobelightroom", "adobe-lightroom", "lightroom"],
    "keyshot": ["keyshot", "luxion"],
    "qnet": ["qualcomm", "qualcom", "qcom"],
    "sequentialthinking": ["steps", "rocket", "workflow"],
    "windbg": ["microsoft", "windbg", "win-dbg"]
}

for name, variations in missing_ones.items():
    found = False
    for slug in variations:
        url = f"https://cdn.simpleicons.org/{slug}/white"
        print(f"Trying {name} -> {slug}...")
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                with open(os.path.join(SRC_DIR, f"{name}.svg"), "wb") as f:
                    f.write(r.content)
                print(f"  FOUND: {slug} saved as {name}.svg")
                found = True
                break
            else:
                print(f"  Fail {r.status_code}")
        except:
            pass
    if not found:
        print(f"  Could not find {name}")

print("Done.")
