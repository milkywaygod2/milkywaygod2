import os
import requests
import xml.etree.ElementTree as ET

# Configuration
OUTPUT_DIR = "icons"
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
    ("c", "C", "A8B9CC", "c"),
    ("cpp11", "C++11", "00599C", "cplusplus"),
    ("cpp14", "C++14", "00599C", "cplusplus"),
    ("cpp17", "C++17", "00599C", "cplusplus"),
    ("cpp20", "C++20", "00599C", "cplusplus"),
    
    # C++ Extended
    ("boost", "BOOST", "DE5E11", "boost"),
    ("opencv", "OPENCV", "5C3EE8", "opencv"),
    ("tesseract", "TESSERACT", "555555", "intel"), 
    ("paddle-ocr", "PADDLE-OCR", "000000", "paddle-ocr"), # Custom
    ("mfc", "MFC", "00599C", "microsoft"), 
    ("unreal5", "UNREAL 5", "313131", "unrealengine"),

    # Python / Web
    ("python", "PYTHON", "3776AB", "python"),
    ("flask", "FLASK", "000000", "flask"),
    ("ollama", "OLLAMA", "000000", "ollama"),
    ("deepseek-ocr", "DEEPSEEK-OCR", "4D6BFE", "deepseek-ocr"), # Custom
    ("java", "JAVA", "007396", "coffeescript"), 
    ("spring", "SPRING", "6DB33F", "spring"),

    # Mobile / Frontend
    ("dart", "DART", "0175C2", "dart"),
    ("flutter", "FLUTTER", "02569B", "flutter"),
    ("html5", "HTML5", "E34F26", "html5"),

    # DB
    ("mysql", "MYSQL", "4479A1", "mysql"),
    ("postgresql", "POSTGRESQL", "4169E1", "postgresql"),
    ("synology", "SYNOLOGY", "B5111B", "synology"),

    # Tools: Git/Github, GitExtension, Winmerge, WinDbg, Figma, Draw.io
    ("git", "GIT", "F05032", "git"),
    ("github", "GITHUB", "181717", "github"),
    ("gitextensions", "GITEXTENSIONS", "2D2D2D", "gitextensions"),
    ("winmerge", "WINMERGE", "86B404", "winmerge"), # Custom
    ("windbg", "WINDBG", "0078D7", "windbg"), # Custom
    ("figma", "FIGMA", "F24E1E", "figma"),
    ("drawio", "DRAW.IO", "F08705", "drawdotio"),

    # IDEs: VS, VSCode, Rider, AndroidStudio
    ("visualstudio", "VISUAL STUDIO", "5C2D91", "visualstudio"),
    ("vscode", "VS CODE", "007ACC", "visualstudiocode"),
    ("rider", "RIDER", "000000", "rider"),
    ("androidstudio", "ANDROID STUDIO", "3DDC84", "androidstudio"),

    # Internal / Custom
    ("antigravity", "ANTIGRAVITY", "FF0000", "antigravity"), # Rocket
    ("context7", "CONTEXT7", "005BBB", "context7"), # Custom
    ("sequentialthinking", "SEQUENTIALTHINKING", "FF9900", "sequentialthinking"), # Brain
    ("flywright", "FLYWRIGHT", "2EAD33", "playwright"), # Used Playwright slug

    # Design / 3D
    ("photoshop", "PHOTOSHOP", "31A8FF", "adobephotoshop"),
    ("illustrator", "ILLUSTRATOR", "FF9A00", "adobeillustrator"),
    ("lightroom", "LIGHTROOM", "31A8FF", "adobelightroom"),
    ("premiere", "PREMIERE", "9999FF", "adobepremierepro"),
    ("aftereffects", "AFTER EFFECTS", "9999FF", "adobeaftereffects"),
    ("c4d", "CINEMA 4D", "004899", "cinema4d"),
    ("rhino", "RHINO", "8C8C8C", "rhinoceros"),
    ("blender", "BLENDER", "E87D0D", "blender"),
    ("keyshot", "KEYSHOT", "000000", "keyshot"), # Custom

    # Other
    ("visualbasic", "VISUAL BASIC", "005476", "visualbasic"), # VB.NET often generic .NET or custom? Checking slug later. Using custom slug if needed, but visualbasic likely distinct or generic. SimpleIcons has visualbasic.
    ("excel-xlsm", "EXCEL XLSM", "217346", "microsoftexcel"),

    # Notes
    ("notion", "NOTION", "000000", "notion"),

    # Certificates
    ("qnet", "정보처리기사", "005696", "qnet"), # Custom Path
    ("sqld", "SQLD", "F29111", "sqld"), # Custom Path
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
    # Rough estimate for Verdana 11 bold-ish
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

def generate_badge(filename, label, color_hex, icon_slug):
    print(f"Generating {filename}...")
    
    path_d = ""
    viewbox_size = 24 # Standard
    
    # 1. Fetch Icon or Use Custom
    if icon_slug in CUSTOM_PATHS:
        path_d = CUSTOM_PATHS[icon_slug]
        # Custom paths assumed on 24x24 scale
    else:
        icon_url = f"https://cdn.simpleicons.org/{icon_slug}/white" 
        
        try:
            r = requests.get(icon_url, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                # Parse SVG to get path and viewBox
                # SimpleIcons usually standardizes to 24x24 viewBox
                icon_svg = ET.fromstring(r.content)
                path_elem = icon_svg.find(".//{http://www.w3.org/2000/svg}path")
                if path_elem is None:
                    # Try without namespace
                    path_elem = icon_svg.find("path")
                path_d = path_elem.attrib['d'] if path_elem is not None else ""
            else:
                print(f"  Error fetching icon {icon_slug}: {r.status_code}")
                return
            
        except Exception as e:
            print(f"  Exception fetching/parsing {icon_slug}: {e}")
            return

    # 2. Calculate Layout
    text_w = get_text_width(label)
    
    # Scale calculation
    # Base scale
    scale_factor = ICON_HEIGHT / float(viewbox_size)
    
    # Custom Scaling for specific logos
    if filename == 'mysql':
        scale_factor *= 1.4  # Boost MySQL by 40%
    if filename == 'tesseract':
        scale_factor *= 1.1 # Boost Intel logo slightly
        
    # Total Width
    full_width = PADDING_X + ICON_HEIGHT + ICON_TEXT_GAP + text_w + PADDING_X
    
    # Center Y adjustment mainly matters if base size differs, but with transform scale it's distinct.
    # We maintain top-left corner at (PADDING_X, (BADGE - ICON)/2) and just scale.
    # However, if we scale UP MySQL, it might overflow. We should adjust translate.
    
    trans_x = PADDING_X
    trans_y = (BADGE_HEIGHT - (viewbox_size * scale_factor))/2
    
    # 3. Build SVG
    # We use a simple template
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{full_width}" height="{BADGE_HEIGHT}" role="img" aria-label="{label}">
  <title>{label}</title>
  <rect width="{full_width}" height="{BADGE_HEIGHT}" fill="#{color_hex}"/>
  <g transform="translate({trans_x}, {trans_y}) scale({scale_factor})">
    <path fill="white" d="{path_d}"/>
  </g>
  <text x="{PADDING_X + ICON_HEIGHT + ICON_TEXT_GAP + text_w/2}" y="{BADGE_HEIGHT/2 + 4}" 
        font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" font-weight="bold" fill="white" 
        text-anchor="middle">{label}</text>
</svg>"""

    with open(os.path.join(OUTPUT_DIR, f"{filename}.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)

print(f"Starting Badge Generation for {len(badges)} badges...")
for b in badges:
    generate_badge(*b)
print("Done.")
