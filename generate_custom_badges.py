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
    ("tesseract", "TESSERACT", "555555", "intel"), # Intel developed Tesseract
    ("mfc", "MFC", "00599C", "microsoft"), 
    ("unreal5", "UNREAL 5", "313131", "unrealengine"),

    # Python / Web
    ("python", "PYTHON", "3776AB", "python"),
    ("flask", "FLASK", "000000", "flask"),
    ("java", "JAVA", "007396", "coffeescript"), # Used as Coffee Cup proxy
    ("spring", "SPRING", "6DB33F", "spring"),

    # Mobile / Frontend
    ("dart", "DART", "0175C2", "dart"),
    ("flutter", "FLUTTER", "02569B", "flutter"),
    ("html5", "HTML5", "E34F26", "html5"),

    # DB
    ("mysql", "MYSQL", "4479A1", "mysql"),
    ("postgresql", "POSTGRESQL", "4169E1", "postgresql"),

    # Tools
    ("git", "GIT", "F05032", "git"),
    ("figma", "FIGMA", "F24E1E", "figma"),

    # Notes
    ("notion", "NOTION", "000000", "notion"),

    # Certificates
    ("qnet", "정보처리기사", "005696", "qnet"), # Custom Path
    ("sqld", "SQLD", "F29111", "sqld"), # Custom Path
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Hardcoded paths for icons that confuse the CDN
CUSTOM_PATHS = {
    # Microsoft 4-squares logo
    "microsoft": "M0 0h11.377v11.372H0zM12.623 0H24v11.372H12.623zM0 12.623h11.377V24H0zM12.623 12.623H24V24H12.623z",
    
    # Database Stack (SQLD Proxy) -> ViewBox 0 0 24 24
    "sqld": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8 8 8zM12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6z", # Simplified DB
    
    # Shield Check (Q-Net Proxy) -> ViewBox 0 0 24 24
    "qnet": "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"
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
