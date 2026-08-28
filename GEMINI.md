---
trigger: always_on
---

# GEMINI.md: Gemini 로컬 규칙 인덱스
*   이 파일은 현재 워크스페이스에 적용되는 **로컬 규칙의 인덱스(Entry Point)**입니다.
*   이 워크스페이스는 프로젝트의 **특정 포지션(Position)**을 전담하는 **특화 에이전트(Specialized Agent)** 공간입니다.

## 규칙 구조 (Structure)
*   이곳의 규칙들은 글로벌 규칙을 상속받으며, 해당 포지션에 최적화된 **특화 페르소나**와 관리 체계를 정의합니다.

### 포함된 규칙 파일 (Included Rules)

#### 1. [rule-persona.md](./.gemini/rules/rule-persona.md)
*   **핵심 역할**: **Specialized Agent (포지션 전담 요원)**
*   **주요 임무**: 전담 포지션(Frontend, Backend, etc)의 전문 작업 수행 및 유지보수.

#### 2. [rule-chat.md](./.gemini/rules/rule-chat.md)
*   **핵심 역할**: **Control Space Chat Rules (컨트롤 워크스페이스 대화 규칙)**
*   **주요 임무**: 관리자급 소통 표준(Tone & Manner) 및 명확한 보고 체계 수립.

#### 3. [rule-git.md](./.gemini/rules/rule-git.md)
*   **핵심 역할**: **Local Git Strategy (로컬 Git 전략)**
*   **주요 임무**: `core-config` 브랜치 관리, 백업 프로토콜 및 원자적 커밋 준수.

#### 4. [rule-safety.md](./.gemini/rules/rule-safety.md)
*   **핵심 역할**: **Local Safety Compliance (로컬 안전 지침)**
*   **주요 임무**: 고위험 작업(Critical Action) 통제 및 로컬 설정 무결성 유지.

---

## 🚀 에이전트 행동 지침 요약
1.  **Orchestrate First**: 직접 코딩보다 전체 그림을 보고 업무를 쪼개고 위임하십시오. (`skill-task-breakdown` 적극 활용)
2.  **Maintain Order**: 모든 산출물은 지정된 폴더(`.gemini/tasks/...`)에 체계적으로 관리되어야 합니다.
3.  **Local First**: 작업 수행 시 항상 이 로컬 규칙 인덱스를 먼저 확인하십시오.
