# Copyright (c) 2026 [milkywaygod2@gmail.com]. All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

import os, sys
from typing import Tuple

################################################################################################
########### import 'PATH_JFW_PY' from environment variable and add to sys.path #################
PATH_JFW_PY = "path_jfw_py"
path_jfw_py = os.environ.get(PATH_JFW_PY)
if path_jfw_py == None:
    print(f"[ERROR] 환경변수 '{PATH_JFW_PY}'를 IDE가 인식하지 못 할 수 있습니다. 재시작해보세요.")
    sys.exit(1)
else:
    if os.path.isdir(path_jfw_py):
        if path_jfw_py not in sys.path:
            sys.path.insert(0, path_jfw_py)
        try:
            from jcore import *
        except ImportError as e:
            print(f"[ERROR] japp-framework-py 모듈 import 실패: {e}")
            sys.exit(1)
    else:
        print(f"[ERROR] 환경변수 '{PATH_JFW_PY}'에 경로가 세팅되어 있지 않거나, 경로가 잘못되었습니다.")
        sys.exit(1)
################################################################################################

import badge_lib

# Configuration: (filename, Label, HexColor, icon_slug, [Optional] ForcedURL)
BADGES = [
    # C / C++ Group
    ("c", "C", "#A8B9CC", "c", None),
    ("cpp11", "C++11", "#00599C", "cpp", None),
    ("cpp14", "C++14", "#00599C", "cpp", None),
    ("cpp17", "C++17", "#00599C", "cpp", None),
    ("cpp20", "C++20", "#00599C", "cpp", None),
    ("boost", "Boost", "#F7931E", "boost", None),
    ("opencv", "OpenCV", "#5C3EE8", "opencv", None),
    ("tesseract", "Tesseract", "#1E90FF", "tesseract", None),
    ("paddle-ocr", "PaddleOCR", "#0062B0", "paddle-ocr", None),
    ("mfc", "MFC", "#0078D4", "microsoft", None),
    ("unreal5", "UnrealEngine5", "#0E1128", "unrealengine", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/unrealengine/unrealengine-original.svg"),

    # Python / Web
    ("python", "Python", "#3776AB", "python", None),
    ("flask", "Flask", "#000000", "flask", None),
    ("ollama", "Ollama", "#000000", "ollama", None),
    ("deepseek-ocr", "DeepSeek", "#1E40AF", "deepseek-ocr", None, True),

    # Java
    ("java", "Java", "#E34F26", "java", None),
    ("spring", "Spring", "#6DB33F", "spring", None),

    # Mobile / Front
    ("dart", "Dart", "#0175C2", "dart", None),
    ("flutter", "Flutter", "#02569B", "flutter", None),
    ("html5", "HTML5", "#E34F26", "html5", None),

    # DB / NAS
    ("mysql", "MySQL", "#4479A1", "mysql", None),
    ("postgresql", "PostgreSQL", "#4169E1", "postgresql", None),
    ("synology", "Synology", "#B3B3B3", "synology", None, True), # Wordmark

    # Tools
    ("git", "Git", "#F05032", "git", None),
    ("github", "GitHub", "#181717", "github", None),
    ("gitextensions", "GitExtensions", "#252525", "gitextensions", "https://gitextensions.github.io/images/gitextensions-logo.png"), 
    ("winmerge", "WinMerge", "#82937F", "winmerge", None), # Pale Green
    ("windbg", "WinDbg", "#00599C", "windbg", None), # Microsoft Blue
    ("figma", "Figma", "#F24E1E", "figma", None),
    ("drawio", "Draw.io", "#F08705", "drawio", None), # Orange

    # IDEs
    ("visualstudio", "VisualStudio", "#5C2D91", "visualstudio", None),
    ("vscode", "Vscode", "#007ACC", "vscode", None),
    ("rider", "Rider", "#000000", "rider", None), # JetBrains Black
    ("androidstudio", "AndroidStudio", "#3DDC84", "androidstudio", None),

    # Internal / Custom Agentic
    ("antigravity", "Antigravity", "#4B0082", "antigravity", None), # Local custom icon
    ("context7", "Context7", "#008080", "context7", None), # Local custom icon
    ("sequentialthinking", "SequentialThinking", "#FF4500", "sequentialthinking", None), # Local custom icon
    ("flywright", "Flywright", "#45BA4B", "playwright", None),

    # Design / 3D
    ("photoshop", "Photoshop", "#31A8FF", "photoshop", None),
    ("illustrator", "Illustrator", "#FF9A00", "illustrator", None),
    ("lightroom", "Lightroom", "#31A8FF", "adobelightroom", None), 
    ("premiere", "Premiere", "#9999FF", "premiere", None),
    ("aftereffects", "AfterEffects", "#9999FF", "aftereffects", None),
    ("c4d", "Cinema4D", "#004886", "c4d", None, True), # Wordmark
    ("rhino", "Rhino", "#800000", "rhino", None),
    ("blender", "Blender", "#E87D0D", "blender", None),
    ("keyshot", "KeyShot", "#000000", "keyshot", None),

    # Other
    ("visualbasic", "VisualBasic", "#5C2D91", "visualbasic", None), 
    ("excel-xlsm", "ExcelXlsm", "#217346", "microsoftexcel", None),

    # Certs (Proxies)
    ("sqld", "SQLD", "#FFA500", "sqld", None),
    ("qnet", "Q-Net", "#000080", "qnet", None),
    ("notion", "Notion", "#000000", "notion", None),
]

# Assets to download if missing
SVG_ASSETS = [
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
    ("keyshot", "https://cdn.simpleicons.org/keyshot/white"),
    ("playwright", "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/playwright/playwright-original.svg"),
]

def main() -> Tuple[str, bool]:
    try:
        ###################### core-process ######################
        badge_lib.ensure_dirs()
        
        JLogger().log_info("--- 1. Checking Assets ---")
        for slug, url in SVG_ASSETS:
            badge_lib.download_resource(slug, url)
            
        JLogger().log_info("--- 2. Generating Badges ---")
        pw, browser = badge_lib.create_browser()
        page = None
        if browser:
            context = browser.new_context(viewport={"width": 400, "height": badge_lib.BADGE_HEIGHT})
            page = context.new_page()

        try:
            for badge in BADGES:
                args = {
                    'filename': badge[0], 'label': badge[1],
                    'color_hex': badge[2], 'icon_slug': badge[3],
                    'forced_url': badge[4] if len(badge) > 4 else None,
                    'wordmark': badge[5] if len(badge) > 5 else False,
                    'page': page,
                }
                badge_lib.generate_badge(**args)
        finally:
            badge_lib.close_browser(pw, browser)
                
        # JLogger().log_info("All badges generated successfully.")
        
        ###################### return-normal ######################
        _msg_success: str = "All badges generated successfully."
        _msg_failure: str = "Validation failed."
        _success: bool = True
        return _msg_success if _success else _msg_failure, _success
    
    except Exception as _except:
        ###################### return-exception ######################
        _msg_exception = f": {_except}"
        return _msg_exception, False

if __name__ == "__main__":
    try:
        # Define Arguments options of kwargs
        args_config = [
            {
                'flags': ['--admin'], 
                'kwargs': {
                    'action': 'store_true',
                    'help': 'Run with admin privileges'
                }
            }
        ]

        # Launch with args config
        SystemServiceManager().launch_proper(admin=False, args_config=args_config, description="Badge Generator")
        return_main: Tuple[str, bool] = GuiEndpointManager().run_with_loading(main, title="Generating Badges")

    except ArgServiceManagerHelpExit:
        return_main = (None, True, True)
    except Exception as _except:
        return_main = (_except, False)
    finally:
        SystemServiceManager().exit_proper(*return_main)
