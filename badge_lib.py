import os
import io
import base64
import re
import requests
from pathlib import Path
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from jcore.l3_diagnostics.jlogger import JLogger
from xml.etree import ElementTree as ET

# Configuration
OUTPUT_DIR = Path("icons")
SRC_DIR = Path("icons_src")
BADGE_HEIGHT = 28
ICON_SIZE = 20  # Icon size (square)
ICON_PADDING = 4  # Padding around icon
FONT_SIZE = 11
PADDING_X = 8
ICON_TEXT_GAP = 6
FONT_FAMILY = "Verdana, Geneva, sans-serif"

CUSTOM_PATHS = {
    # C++ Extended Groups
    "paddle-ocr": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z", # Fallback
    "microsoft": "M0 0h11.377v11.372H0zM12.623 0H24v11.372H12.623H0zM0 12.623h11.377V24H0zM12.623 12.623H24V24H12.623z",
    
    # Python / Web
    "deepseek-ocr": "M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z", # Search

    # Tools
    "visualstudio": "M17 0c-.5 0-1 .2-1.4.6L9 6.2 2.6 3a1 1 0 0 0-1.4 1v16a1 1 0 0 0 1.4 1L9 17.8l6.6 5.6c.4.4.9.6 1.4.6 1.1 0 2-.9 2-2V2c0-1.1-.9-2-2-2z m0 18.2L11.5 12 17 5.8v12.4z M9.8 13.7L5 16.1V7.9l4.8 2.4 1.7-1.7-6.9-3.4a.99.99 0 0 0-1-.1c-.4.2-.6.5-.6.9v12c0 .4.2.7.6.9.3.2.7.2 1 0l6.9-3.4-1.7-1.8z",
    "visualstudiocode": "M23.15 2.587L18.21.21a.71.71 0 00-1 .492l-1.66 6.6L2.2 1.39a.77.77 0 00-1.2.56v20a.77.77 0 001.2.57L15.5 16.7l1.66 6.6a.71.71 0 001 .5l4.94-2.38a.72.72 0 00.3-.64V3.22a.72.72 0 00-.25-.633z",
    "winmerge": "M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z", # Branch/Nodes
    "windbg": "M0 0h11.377v11.372H0zM12.623 0H24v11.372H12.623H0zM0 12.623h11.377V24H0zM12.623 12.623H24V24H12.623z", # Microsoft Logo (Fallback for broken bug path)
    "drawdotio": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 16.5V12H6v-2h3V7.5l4.5 4.5-4.5 4.5z", # Simple block diagram
    "gitextensions": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8 8 8z", # Fallback Circle

    # Internal / Custom
    "antigravity": "M12 2.5l-2.5 4h5l-2.5-4zm-4 5l-3 5h5.5l-2.5-5zm8 0l-2.5 5H19l-3-5z", # Rocket
    "context7": "M4 4h16v16H4V4zm2 2v12h12V6H6zm2 2h8v2H8V8zm0 4h8v2H8v-2z", # Document
    "sequentialthinking": "M4 18h16v2H4v-2zm0-4h12v2H4v-2zm0-4h8v2H4v-2zm0-4h4v2H4V6z", # Steps
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

def ensure_dirs():
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not SRC_DIR.exists():
        SRC_DIR.mkdir(parents=True, exist_ok=True)

def get_text_width(text):
    # Rough estimate for text width (verdana 11px)
    return max(len(text) * 7.5 + 10, 20)

def get_svg_bounds(svg_content):
    """Extract viewBox and calculate centered positioning for SVG content"""
    try:
        # Parse SVG to get viewBox
        root = ET.fromstring(svg_content)
        viewbox = root.get('viewBox', '0 0 24 24')
        vb_parts = [float(x) for x in viewbox.split()]

        if len(vb_parts) == 4:
            vb_x, vb_y, vb_w, vb_h = vb_parts
            # Return viewBox dimensions for proper centering
            return viewbox, vb_w, vb_h
    except:
        pass

    return "0 0 24 24", 24, 24

def fetch_local_or_url(slug, forced_url=None):
    ensure_dirs()
    local_svg = SRC_DIR / f"{slug}.svg"
    if local_svg.exists():
        with open(local_svg, "r", encoding="utf-8") as f:
            return f.read(), True

    local_png = SRC_DIR / f"{slug}.png"
    if local_png.exists():
        with open(local_png, "rb") as f:
            enc = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{enc}", False

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
            JLogger().log_warning(f"Failed to fetch {forced_url}: {e}")

    # Try Devicon (Standard)
    devicon_url = f"https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/{slug}/{slug}-original.svg"
    try:
        r = requests.get(devicon_url, timeout=2)
        if r.status_code == 200:
            return r.text, True
    except:
        pass

    return None, False

def generate_badge(filename, label, color_hex, icon_slug, forced_url=None):
    JLogger().log_info(f"Generating badge: {filename}...")
    # Use white background with light gray border
    char_width = 8.5 if FONT_SIZE > 10 else 7.5
    text_width_approx = len(label) * char_width
    total_width = int(30 + text_width_approx + 10)

    bg_rect = f'<rect width="{total_width}" height="{BADGE_HEIGHT}" rx="4" fill="#FFFFFF" stroke="#E1E4E8" stroke-width="1"/>'

    logo_content, is_svg = fetch_local_or_url(icon_slug, forced_url)
    logo_svg_element = ""
    
    if logo_content:
        if is_svg:
            start_svg = logo_content.find("<svg")
            if start_svg != -1:
                end_opening_tag = logo_content.find(">", start_svg)
                end_svg = logo_content.rfind("</svg>")
                
                if end_opening_tag != -1 and end_svg != -1:
                    inner_content = logo_content[end_opening_tag+1:end_svg]
                    viewbox_match = re.search(r'viewBox="([^"]+)"', logo_content)
                    viewbox_attr = f'viewBox="{viewbox_match.group(1)}"' if viewbox_match else 'viewBox="0 0 128 128"'

                    # Keep original icon colors for white background
                    icon_x = ICON_PADDING
                    icon_y = (BADGE_HEIGHT - ICON_SIZE) / 2  # Vertically center the icon
                    # Use preserveAspectRatio for automatic centering within viewBox
                    logo_svg_element = f'<svg x="{icon_x}" y="{icon_y}" width="{ICON_SIZE}" height="{ICON_SIZE}" {viewbox_attr} preserveAspectRatio="xMidYMid meet">{inner_content}</svg>'
                else:
                    # Fallback to base64 if parsing fails
                    enc = base64.b64encode(logo_content.encode("utf-8")).decode()
                    logo_svg_element = f'<image x="7" y="7" width="{ICON_HEIGHT + 4}" height="{ICON_HEIGHT + 4}" href="data:image/svg+xml;base64,{enc}"/>'
            else:
                 pass
        else:
            # It's a base64 encoded image string (e.g. PNG)
            icon_x = ICON_PADDING
            icon_y = (BADGE_HEIGHT - ICON_SIZE) / 2  # Vertically center the icon
            logo_svg_element = f'<image x="{icon_x}" y="{icon_y}" width="{ICON_SIZE}" height="{ICON_SIZE}" href="{logo_content}"/>'
    
    # Fallback to Simple Icons (colored) or Custom Path
    if not logo_svg_element:
        # Try Simple Icons (colored version first)
        try:
            icon_url = f"https://cdn.simpleicons.org/{icon_slug}"
            r = requests.get(icon_url, timeout=2)
            if r.status_code == 200:
                # Extract path and color from SimpleIcons SVG
                svg_content = r.text
                fill_match = re.search(r'fill="([^"]+)"', svg_content)
                path_match = re.search(r'<path[^>]*d="([^"]+)"', svg_content)
                viewbox_match = re.search(r'viewBox="([^"]+)"', svg_content)

                if path_match:
                    fill_color = fill_match.group(1) if fill_match else "#24292E"
                    path_d = path_match.group(1)
                    viewbox = viewbox_match.group(1) if viewbox_match else "0 0 24 24"
                    icon_y = (BADGE_HEIGHT - ICON_SIZE) / 2  # Vertically center the icon
                    # Use preserveAspectRatio for automatic centering
                    logo_svg_element = f'<svg x="{ICON_PADDING}" y="{icon_y}" width="{ICON_SIZE}" height="{ICON_SIZE}" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet"><path fill="{fill_color}" d="{path_d}"/></svg>'
        except:
            pass

        # Fallback to Custom Path if SimpleIcons failed
        if not logo_svg_element and icon_slug in CUSTOM_PATHS:
            path_d = CUSTOM_PATHS[icon_slug]
            logo_svg_element = f'<path fill="#24292E" transform="scale(1.1) translate(6,6)" d="{path_d}"/>'
                
        if not logo_svg_element:
             JLogger().log_warning(f"  [Warning] No logo found for {filename}")
             
        if "<path" in logo_svg_element:
             logo_svg_element = f'<svg x="0" y="0" width="{BADGE_HEIGHT}" height="{BADGE_HEIGHT}" viewBox="0 0 40 40">{logo_svg_element}</svg>'

    final_svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" 
    width="{total_width}" 
    height="{BADGE_HEIGHT}" 
    viewBox="0 0 {total_width} {BADGE_HEIGHT}">
        {bg_rect}
        {logo_svg_element}
        <text x="{total_width - (text_width_approx / 2) - 10}" y="{BADGE_HEIGHT / 2 + FONT_SIZE * 0.35}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" fill="#24292E" font-weight="600">{label}</text>
    </svg>'''
    
    try:
        ensure_dirs()
        png_path = OUTPUT_DIR / f"{filename}.png"
        src_png_path = SRC_DIR / f"{filename}.png"
        
        drawing = svg2rlg(io.BytesIO(final_svg.encode("utf-8")))
        renderPM.drawToFile(drawing, str(png_path), fmt="PNG", bg=None)
        
        # Logo-only SVG
        src_svg = f'''
        <svg xmlns="http://www.w3.org/2000/svg" 
    width="{total_width}" 
    height="{BADGE_HEIGHT}" 
    viewBox="0 0 {total_width} {BADGE_HEIGHT}">
        {bg_rect}
        {logo_svg_element}
    </svg>'''
        
        src_drawing = svg2rlg(io.BytesIO(src_svg.encode("utf-8")))
        renderPM.drawToFile(src_drawing, str(src_png_path), fmt="PNG", bg=None)
        
    except Exception as e:
        JLogger().log_error(f"  [Error] Failed to convert {filename} to PNG: {e}")

def download_resource(slug, url):
    ensure_dirs()
    try:
        target_path = SRC_DIR / f"{slug}.svg"
        if target_path.exists():
            return
            
        JLogger().log_info(f"Downloading {slug} from {url}...")
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            target_path.write_bytes(r.content)
            JLogger().log_info(f"  Successfully saved {slug}.svg")
        else:
            JLogger().log_warning(f"  Failed with status code {r.status_code}")
    except Exception as e:
        JLogger().log_error(f"  Error: {e}")

