---
trigger: always_on
---

# 로컬 Git 전략 (Badge Generator)

## 1. 단순화된 브랜치 전략
*   이 프로젝트는 단일 도구이므로 복잡한 피처 브랜치보다 **빠른 반복(Iteration)**을 중시합니다.
*   다만, 안정성을 위해 `main` 브랜치에 직접 푸시하기 전 로컬 테스트(`python main.py --help`)를 반드시 통과해야 합니다.

## 2. 에셋 관리
*   `icons_src/` (원본 SVG)와 `icons/` (생성된 PNG) 폴더의 변경 사항을 주의 깊게 추적하십시오.
*   `.gitignore` 규칙에 따라 생성된 결과물이 저장소에 불필요하게 포함되지 않는지 확인하십시오.
