import os
import requests
import base64
from io import BytesIO

# Configuration
OUTPUT_DIR = "icons"
SRC_DIR = "icons_src"
BADGE_HEIGHT = 28
ICON_HEIGHT = 22  # Increased for larger logos (Standard was 20)
FONT_SIZE = 11
PADDING_X = 8
ICON_TEXT_GAP = 6
FONT_FAMILY = "Verdana, Geneva, sans-serif"

# Badge Definitions: (Filename, Label, HexColor, SimpleIconsSlug)
# Note: Text color will be white.
badges = [
    # C / C++ Group
    ("c", "C", "2D2D2D", "c", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/c/c-original.svg"),
    ("cpp11", "C++11", "2D2D2D", "cplusplus", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg"),
    ("cpp14", "C++14", "2D2D2D", "cplusplus", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg"),
    ("cpp17", "C++17", "2D2D2D", "cplusplus", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg"),
    ("cpp20", "C++20", "2D2D2D", "cplusplus", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg"),
    ("boost", "Boost", "2D2D2D", "boost", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/boost/boost-original.svg"),
    ("opencv", "OpenCV", "2D2D2D", "opencv", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/opencv/opencv-original.svg"),
    ("tesseract", "Tesseract", "2D2D2D", "tesseract", None), # Custom/Fallback
    ("paddle-ocr", "PaddleOCR", "2D2D2D", "paddle-ocr", None), # Custom/Fallback
    ("mfc", "MFC", "2D2D2D", "microsoft", None), # Fallback to MS squares or find MFC logo?
    ("unreal5", "Unreal Engine 5", "2D2D2D", "unrealengine", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/unrealengine/unrealengine-original.svg"),

    # Python / Web
    ("python", "Python", "2D2D2D", "python", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg"),
    ("flask", "Flask", "2D2D2D", "flask", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original.svg"),
    ("ollama", "Ollama", "2D2D2D", "ollama", "https://ollama.com/public/ollama.png"), # Try official PNG
    ("deepseek-ocr", "DeepSeek", "2D2D2D", "deepseek-ocr", None), # Custom/Fallback (Need to find)

    # Java
    ("java", "Java", "2D2D2D", "java", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg"),
    ("spring", "Spring", "2D2D2D", "spring", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/spring/spring-original.svg"),

    # Mobile / Front
    ("dart", "Dart", "2D2D2D", "dart", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/dart/dart-original.svg"),
    ("flutter", "Flutter", "2D2D2D", "flutter", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flutter/flutter-original.svg"),
    ("html5", "HTML5", "2D2D2D", "html5", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg"),

    # DB / NAS
    ("mysql", "MySQL", "2D2D2D", "mysql", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg"),
    ("postgresql", "PostgreSQL", "2D2D2D", "postgresql", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg"),
    ("synology", "Synology", "2D2D2D", "synology", None), # Custom

    # Tools
    ("git", "Git", "2D2D2D", "git", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original.svg"),
    ("github", "GitHub", "2D2D2D", "github", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original.svg"),
    ("gitextensions", "GitExt", "2D2D2D", "gitextensions", "https://gitextensions.github.io/images/gitextensions-logo.png"), # Tricky, try png
    ("winmerge", "WinMerge", "2D2D2D", "winmerge", None), # Custom
    ("windbg", "WinDbg", "2D2D2D", "windbg", None), # Custom
    ("figma", "Figma", "2D2D2D", "figma", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/figma/figma-original.svg"),
    ("drawio", "Draw.io", "2D2D2D", "drawdotio", None), # Custom

    # IDEs
    ("visualstudio", "Visual Studio", "2D2D2D", "visualstudio", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/visualstudio/visualstudio-original.svg"),
    ("vscode", "VS Code", "2D2D2D", "visualstudiocode", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vscode/vscode-original.svg"),
    ("rider", "Rider", "2D2D2D", "rider", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jetbrains/jetbrains-original.svg"), # JetBrains logo as fallback or Rider if exists?
    ("androidstudio", "Android Studio", "2D2D2D", "androidstudio", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/androidstudio/androidstudio-original.svg"),

    # Internal / Custom Agentic
    ("antigravity", "Antigravity", "2D2D2D", "antigravity", None),
    ("context7", "Context7", "2D2D2D", "context7", None),
    ("sequentialthinking", "Sequential", "2D2D2D", "sequentialthinking", None),
    ("flywright", "Flywright", "2D2D2D", "playwright", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/playwright/playwright-original.svg"),

    # Design / 3D
    ("photoshop", "Photoshop", "2D2D2D", "adobephotoshop", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/photoshop/photoshop-original.svg"),
    ("illustrator", "Illustrator", "2D2D2D", "adobeillustrator", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/illustrator/illustrator-original.svg"),
    ("lightroom", "Lightroom", "2D2D2D", "adobelightroom", None), # Not in devicon?
    ("premiere", "Premiere", "2D2D2D", "adobepremierepro", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/premierepro/premierepro-original.svg"),
    ("aftereffects", "After Effects", "2D2D2D", "adobeaftereffects", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/aftereffects/aftereffects-original.svg"),
    ("c4d", "Cinema 4D", "2D2D2D", "c4d", None),
    ("rhino", "Rhino", "2D2D2D", "rhino", None),
    ("blender", "Blender", "2D2D2D", "blender", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/blender/blender-original.svg"),
    ("keyshot", "KeyShot", "2D2D2D", "keyshot", None),

    # Other
    ("visualbasic", "VB.NET", "2D2D2D", "visualbasic", None), # maybe dot-net logo?
    ("excel-xlsm", "Excel", "2D2D2D", "microsoftexcel", None),

    # Certs (Proxies)
    ("sqld", "SQLD", "2D2D2D", "sqld", None),
    ("qnet", "Q-Net", "2D2D2D", "qnet", None),
    ("notion", "Notion", "2D2D2D", "notion", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/notion/notion-original.svg"),
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Hardcoded paths for icons that confuse the CDN or need custom paths
CUSTOM_PATHS = {
    # C++ Extended Groups
    "paddle-ocr": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z", # Text Document
    "microsoft": "M0 0h11.377v11.372H0zM12.623 0H24v11.372H12.623zM0 12.623h11.377V24H0zM12.623 12.623H24V24H12.623z",
    
    # Python / Web
    "deepseek-ocr": "M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z", # Search

    # Tools
    "visualstudio": "M17 0c-.5 0-1 .2-1.4.6L9 6.2 2.6 3a1 1 0 0 0-1.4 1v16a1 1 0 0 0 1.4 1L9 17.8l6.6 5.6c.4.4.9.6 1.4.6 1.1 0 2-.9 2-2V2c0-1.1-.9-2-2-2z m0 18.2L11.5 12 17 5.8v12.4z M9.8 13.7L5 16.1V7.9l4.8 2.4 1.7-1.7-6.9-3.4a.99.99 0 0 0-1-.1c-.4.2-.6.5-.6.9v12c0 .4.2.7.6.9.3.2.7.2 1 0l6.9-3.4-1.7-1.8z",
    "visualstudiocode": "M23.15 2.587L18.21.21a.71.71 0 00-1 .492l-1.66 6.6L2.2 1.39a.77.77 0 00-1.2.56v20a.77.77 0 001.2.57L15.5 16.7l1.66 6.6a.71.71 0 001 .5l4.94-2.38a.72.72 0 00.3-.64V3.22a.72.72 0 00-.25-.633z",
    "winmerge": "M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z", # Branch/Nodes
    "windbg": "M19 8h-2.81a5.985 5.985 0 0 0-1.82-1.96l.93-.93a.996.996 0 1 0-1.41-1.41l-1.47 1.47C11.96 5.06 11.49 5 11 5s-.96.06-1.41.17l-1.48-1.48a.996.996 0 1 0-1.41 1.41l.93.93A5.985 5.985 0 0 0 5.81 8H3v2h2.29c-.11.64-.18 1.31-.18 2s.07 1.36.18 2H3v2h2.81c.71 1.12 1.69 2.05 2.87 2.66l-.91.91a.996.996 0 1 0 1.41 1.41l1.46-1.46C10.51 19.94 10.98 20 11.45 20s.95-.06 1.4-.17l1.46 1.46a.996.996 0 1 0 1.41-1.41l-.9-1.9-.9c1.18-.61 2.16-1.54 2.87-2.66H21v-2h-2.29c.11-.64.18-1.31.18-2s-.07-1.36-.18-2H21V8zM11.45 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z", # Bug
    "drawdotio": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 16.5V12H6v-2h3V7.5l4.5 4.5-4.5 4.5z", # Simple block diagram

    # Internal / Custom
    "antigravity": "M7.5 7.5L4 11v4l3.5 3.5L11 15v-4L7.5 7.5zm9 0L13 11v4l3.5 3.5L20 15v-4l-3.5-3.5zM12 2L9 5v4l3 3 3-3V5l-3-3z", # Rocket
    "context7": "M5 5v14h14V5H5zm2 2h10v2H7V7zm0 4h7v2H7v-2zm0 4h10v2H7v-2z", # Document text
    "sequentialthinking": "M4 18h16v2H4v-2zm0-5h16v2H4v-2zm0-5h16v2H4V8zm0-5h16v2H4V3z", # Stack/Steps
    "playwright": "M2.8 19.45L21.2 12 2.8 4.55v14.9z", # Play/Flight (Triangle)

    # Design / 3D
    "adobephotoshop": "M0 0v24h24V0H0zm19.5 16h-2.5v-2.5c0-.83-.67-1.5-1.5-1.5h-1v4h-2.5v-7h3.5c2.21 0 4 1.79 4 4v.5c0 1.38-1.12 2.5-2.5 2.5zM4.5 16h3.5v-2h2v-2h-2v-1h2.5v-2H4.5v7z",
    "adobeillustrator": "M0 0v24h24V0H0zm9.5 16h-5v-1l2-5h1l2 5v1zm-3-2h3v-.5l-1-2.5h-.5l-1 2.5v.5zm9 2h-2v-7h2v7zm1.5-6h2v-1h-2v1z",
    "adobelightroom": "M0 0v24h24V0H0zm6.5 16v-7h2.5v5h3v2h-5.5zm7 0v-5h3v-2h-3v-1h3v-1.5h-3.5c-1.1 0-2 .9-2 2v5.5h2.5z",
    "adobepremierepro": "M0 0v24h24V0H0zm6 16v-7h3.5c1.1 0 2 .9 2 2v1c0 1.1-.9 2-2 2H8.5v2H6zm2.5-4h1c.28 0 .5-.22.5-.5v-1c0-.28-.22-.5-.5-.5h-1v2zm7 4v-5h2v-2h-2v-1h2v-1.5h-2.5c-1.1 0-2 .9-2 2v5.5h2.5z",
    "adobeaftereffects": "M0 0v24h24V0H0zm7 16l-1-2h-3l-1 2H.5l3.5-7h2l3.5 7H7zm-1.5-3l-1-2.5L3.5 13h2zm10 3v-1h3v-1.5h-3v-1h3V8h-3c-1.1 0-2 .9-2 2v4c0 1.1.9 2 2 2h3.5V16h-3.5z",
    "keyshot": "M12.65 10A5.98 5.98 0 0 0 7 6c-3.31 0-6 2.69-6 6s2.69 6 6 6a5.98 5.98 0 0 0 5.65-4H17v4h4v-4h2v-4H12.65zM7 14c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z",

    # Other
    "visualbasic": "M2 4v16h20V4H2zm4 12l-2.5-7h2L7 13l1.5-4h2L8 16H6zm10 0h-2l-1-2h-1v2h-2V8h3.5c1.93 0 3.5 1.57 3.5 3.5 0 1.1-.55 2.05-1.39 2.66C15.9 14.54 16 15.02 16 16z",
    "microsoftexcel": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14l-2.5-3.5L6 16h2.5l1.25-2 1.25 2H13l-2.5-3.5L13 8h-2.5l-1.25 2L8 8H5.5l2.5 3.5L5.5 15h2.5z",

    # Certificates (Proxies)
    "sqld": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8 8 8zM12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6z", 
    "qnet": "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z",
}


def get_text_width(text):
    # Rough estimate for text width (verdana 11px)
    return max(len(text) * 7.5 + 10, 20)
    # Uppercase chars are wider ~8-9px, Lower ~6-7px.
    # We'll use a simple multiplier.
    width = 0
    for char in text:
        if '\u3131' <= char <= '\u318E' or '\uAC00' <= char <= '\uD7A3': # Korean
            width += 13
        elif char.isupper():
            width += 9
        else:
            width += 7.5
    return int(width)

def fetch_local_or_url(slug, forced_url=None):
    # 1. Try local overrides first
    local_svg = os.path.join(SRC_DIR, f"{slug}.svg")
    local_png = os.path.join(SRC_DIR, f"{slug}.png")
    
    if os.path.exists(local_svg):
        with open(local_svg, "r", encoding="utf-8") as f:
            return f.read(), True # content, is_svg
            
    if os.path.exists(local_png):
        with open(local_png, "rb") as f:
            enc = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{enc}", False # content as href, is_svg=False

    # 2. Try forced URL if provided
    if forced_url:
        try:
            r = requests.get(forced_url)
            if r.status_code == 200:
                if forced_url.endswith(".svg"):
                     return r.text, True
                else: # Assume PNG/Image
                     enc = base64.b64encode(r.content).decode()
                     return f"data:image/png;base64,{enc}", False
        except Exception as e:
            print(f"Failed to fetch {forced_url}: {e}")

    # 3. Try Devicon (Standard)
    # Convention: https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/{slug}/{slug}-original.svg
    devicon_url = f"https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/{slug}/{slug}-original.svg"
    try:
        r = requests.get(devicon_url, timeout=2)
        if r.status_code == 200:
            return r.text, True
    except:
        pass

    return None, False


def generate_badge(filename, label, color_hex, icon_slug, forced_url=None):
    print(f"Generating {filename}...")
    
    # Text Layout Calculation
    label_width = get_text_width(label)
    total_width = label_width + 35 # 30px icon + padding
    
    # Try to get colored logo
    logo_content, is_svg = fetch_local_or_url(icon_slug, forced_url)
    
    logo_svg_element = ""
    
    if logo_content:
        # If it's an SVG, we try to strip the XML/DOCTYPE header and inject it
        if is_svg:
            # Simple strip of headers to embed as inner content
            # This is a bit hacky but works for most clean SVGs
            start_svg = logo_content.find("<svg")
            if start_svg != -1:
                # Extract attributes from the root svg tag to maybe respect viewbox?
                # For now, let's wrap it in an group or symbol to allow sizing
                # But easiest way to size separate SVG is <image href="data:image/svg+xml;base64,...">
                # Let's use base64 for SVG too to ensure isolation
                enc = base64.b64encode(logo_content.encode("utf-8")).decode()
                logo_svg_element = f'<image x="7" y="7" width="26" height="26" href="data:image/svg+xml;base64,{enc}"/>'
            else:
                 # Fallback if no svg tag found?
                 pass
        else:
            # It's a base64 encoded image string (e.g. PNG)
            logo_svg_element = f'<image x="7" y="7" width="26" height="26" href="{logo_content}"/>'
    
    # Fallback to Monochrome Custom Path or Simple Icons
    if not logo_svg_element:
        path_d = ""
        if icon_slug in CUSTOM_PATHS:
            path_d = CUSTOM_PATHS[icon_slug]
            # Use white fill for monochrome
            logo_svg_element = f'<path fill="#fff" d="{path_d}"/>'
        else:
            # Try Simple Icons
            try:
                icon_url = f"https://cdn.simpleicons.org/{icon_slug}/white"
                r = requests.get(icon_url)
                if r.status_code == 200:
                    # Extract path d
                    start_d = r.text.find('d="')
                    if start_d != -1:
                        end_d = r.text.find('"', start_d + 3)
                        path_d = r.text[start_d+3:end_d]
                        logo_svg_element = f'<path fill="#fff" d="{path_d}"/>'
            except:
                pass
                
        # Scale adjustment for monochrome paths (viewbox 24->26?)
        # For simplicity, we keep the original logic for paths if fallback
        if not logo_svg_element:
             print(f"  [Warning] No logo found for {filename}")
             
        # If using path, we usually wrap it in a transform for size. 
        # But wait, original code was 24x24 viewbox.
        # If we successfully created a path element, it expects a parent scaling 
        # or we assume the path is 24x24.
        # Let's wrap path-based logos in a standard 24->26 scaling group if needed
        # Or just place it.
        # To maintain consistency, if it is a path, we wrap:
        if "<path" in logo_svg_element:
             logo_svg_element = f'<svg x="7" y="7" width="26" height="26" viewBox="0 0 24 24">{logo_svg_element}</svg>'


    # Badge Template (For the Badge) - Dark Grey Background #2D2D2D
    # Using 'for-the-badge' style look
    badge_height = 40
    
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{badge_height}" viewBox="0 0 {total_width} {badge_height}">
        <rect width="{total_width}" height="{badge_height}" rx="4" fill="#2D2D2D"/>
        {logo_svg_element}
        <text x="{35 + label_width/2}" y="25" text-anchor="middle" font-family="Verdana, Geneva, sans-serif" font-size="16" fill="#fff" font-weight="bold">{label}</text>
    </svg>'''

    with open(os.path.join(OUTPUT_DIR, f"{filename}.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    print(f"Starting Badge Generation for {len(badges)} badges...")
    for badge in badges:
        # Handle optional URL
        if len(badge) == 5:
            generate_badge(badge[0], badge[1], badge[2], badge[3], badge[4])
        else:
            generate_badge(badge[0], badge[1], badge[2], badge[3])
    print("Done.")
