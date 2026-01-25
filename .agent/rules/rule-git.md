---
trigger: always_on
---

# 🌿 Project: MilkyWayGod2 (Git Rules)

## 1. Branch Strategy (브랜치 전략)
이 프로젝트의 Git 작업은 다음 규칙을 엄격히 준수해야 합니다.

*   **Target Branch (작업 브랜치)**: **`feature/project-init`**
    *   모든 기능 개발, 버그 수정, 리팩토링은 반드시 이 브랜치에서 수행해야 합니다.
    *   `main` 브랜치에 직접 커밋하거나 푸시하는 것은 **금지**됩니다.

*   **Upstream Strategy**:
    *   `feature/project-init`에서 작업 완료 후, 글로벌 워크플로우(`/git-push-main`)를 통해 안전하게 `main`으로 병합하십시오.

## 2. Global Skill Usage (글로벌 스킬 사용)
본 프로젝트는 시스템의 안정성을 위해 `.gemini/antigravity`의 **글로벌 Git 스킬**을 사용합니다.

*   **필수 사용 (Mandatory)**:
    *   `skill-git-stage.py`, `skill-git-commit.py`, `skill-git-push.py`
    *   직접적인 `git` 명령어 사용보다, 검증된 스킬 사용을 우선하십시오.
