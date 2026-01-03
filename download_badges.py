import os
import requests
import urllib.parse

# Define the badges to download
# Format: (filename, label, message, color, logo, logoColor)
# We will construct the shields.io URL manually to ensure consistent style
# URL format: https://img.shields.io/badge/<LABEL>-<MESSAGE>-<COLOR>?style=for-the-badge&logo=<LOGO>&logoColor=<LOGOCOLOR>
# However, for simple stack badges, it's usually: https://img.shields.io/badge/<TEXT>-<COLOR>?style=for-the-badge&logo=<LOGO>&logoColor=white

badges = [
    # C / C++
    ("c", "c-A8B9CC", "c"),
    ("cpp11", "c++11-00599C", "c%2B%2B"),
    ("cpp14", "c++14-00599C", "c%2B%2B"),
    ("cpp17", "c++17-00599C", "c%2B%2B"),
    ("cpp20", "c++20-00599C", "c%2B%2B"),
    # C++ Libraries & Frameworks
    ("boost", "boost-DE5E11", "boost"),
    ("opencv", "opencv-5C3EE8", "opencv"),
    ("tesseract", "tesseract_ocr-000000", "tesseract"), # Attempting specific, if fails will fall back in browser, script just downloads svg
    ("mfc", "mfc-00599C", "windows"),
    ("unreal5", "unreal_engine_5-313131", "unrealengine"),
    
    # Python / Java / Web
    ("python", "python-3776AB", "python"),
    ("flask", "flask-000000", "flask"),
    ("java", "java-007396", "java"),
    ("spring", "spring-6DB33F", "spring"),
    
    # Mobile / Frontend
    ("dart", "dart-0175C2", "dart"),
    ("flutter", "flutter-02569B", "flutter"),
    ("html5", "html5-E34F26", "html5"),
    
    # DB
    ("mysql", "mysql-4479A1", "mysql"),
    ("postgresql", "postgresql-4169E1", "postgresql"),
    
    # Tools
    ("git", "git-F05032", "git"),
    ("figma", "figma-F24E1E", "figma"),

    # Note
    ("notion", "Notion-000000", "Notion"),
    
    # Certificates
    ("qnet", "정보처리기사-005696", "southkorea"), # Using generic if specific not found, maybe no logo? Let's use a generic 'certificate' look if possible or just text-heavy.
    ("sqld", "SQLD-F29111", "mysql"), # Using DB icon for SQLD
]

style = "for-the-badge"
output_dir = "icons"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Downloading {len(badges)} badges to '{output_dir}/'...")

for filename, text_color, logo in badges:
    url = f"https://img.shields.io/badge/{text_color}?style={style}&logo={logo}&logoColor=white"
    
    # Special case for Notion link if needed, but we just want the image
    # Note: User wanted the badge image itself saved.
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        file_path = os.path.join(output_dir, f"{filename}.svg")
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Saved: {file_path}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

print("Download complete.")
