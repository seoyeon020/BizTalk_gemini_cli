# GEMINI.md for BizTone Converter

## 프로젝트 개요

**BizTone Converter (업무 말투 변환기)**는 사용자가 일상적인 텍스트를 상사, 타팀 동료, 외부 고객 등 다양한 대상에게 적합한 비즈니스 커뮤니케이션 톤으로 변환할 수 있도록 돕는 AI 기반 웹 애플리케이션입니다. 이 솔루션은 의사소통 효율성을 높이고, 커뮤니케이션 품질을 표준화하며, 비즈니스 글쓰기 교육 비용을 절감하는 것을 목표로 합니다.

## 사용 기술

*   **프론트엔드:** HTML5, CSS3, JavaScript (ES6+). 텍스트 입력, 대상 선택, 변환 결과 표시를 위한 사용자 친화적인 인터페이스를 제공합니다.
*   **백엔드:** Python 3.11, Flask (경량 웹 프레임워크), Flask-CORS (교차 출처 요청 처리용), `python-dotenv` (환경 변수 관리용).
*   **AI/ML 통합:** Groq AI API와 `moonshotai/kimi-k2-instruct-0905` 모델을 활용하여 맞춤형 프롬프트 엔지니어링 기반의 자연어 변환을 수행합니다.
*   **배포:** Git/GitHub를 통한 버전 관리 및 Vercel을 통한 정적 파일 호스팅 및 서버리스 기능 배포가 예정되어 있습니다.

## 아키텍처

이 애플리케이션은 클라이언트-서버 아키텍처를 따릅니다:
*   **프론트엔드** (HTML/CSS/JS)는 사용자 브라우저에서 실행되며, UI 상호작용 및 API 요청을 처리합니다.
*   **백엔드** (Flask)는 API 게이트웨이 역할을 하며, 정적 프론트엔드 파일을 제공하고 변환 요청을 처리합니다.
*   **Flask 백엔드**는 **Groq AI API**와 통신하여 실제 텍스트 톤 변환을 수행합니다.

## 주요 기능

*   **대상별 말투 변환:** 상사에게는 정중하고 격식 있는 보고체, 타팀 동료에게는 친절하고 상호 존중하는 협조 요청체, 고객에게는 극존칭을 사용하는 전문적이고 서비스 지향적인 말투로 텍스트를 변환합니다.
*   **실시간 변환 처리:** 평균 3초 이내의 응답 시간을 목표로 합니다.
*   **원본 및 변환 텍스트 표시:** 원본 텍스트와 변환된 텍스트를 나란히 표시하여 쉽게 비교할 수 있도록 합니다.
*   **복사 기능:** 변환된 텍스트를 클립보드에 쉽게 복사할 수 있습니다.
*   **반응형 디자인:** 다양한 기기(데스크톱, 태블릿, 모바일)에 최적화된 화면을 제공합니다.
*   **입력 글자 수 제한:** 입력 텍스트는 최대 500자로 제한됩니다.

## 빌드 및 실행 방법

### 백엔드 (Python/Flask)

1.  **`backend` 디렉토리로 이동:**
    ```bash
    cd backend
    ```
2.  **Python 가상 환경 생성 및 활성화:**
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```
3.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **환경 변수 설정:**
    프로젝트 루트 (`biztalk_llm/.env`)에 `.env` 파일을 생성하고 `GROQ_API_KEY`를 추가합니다.
    **중요: `.env` 파일을 프로그램적으로 수정하지 마십시오.**
    ```
    GROQ_API_KEY="your_groq_api_key_here"
    ```
5.  **Flask 애플리케이션 실행:**
    ```bash
    python app.py
    ```
    백엔드 서버는 일반적으로 `http://127.0.0.1:5000`에서 실행됩니다.

### 프론트엔드 (HTML/CSS/JavaScript)

프론트엔드는 Flask 백엔드에 의해 직접 제공됩니다. 백엔드 서버를 시작한 후 웹 브라우저에서 `http://127.0.0.1:5000`으로 접속하십시오.

## 개발 컨벤션

*   **언어:** Gemini CLI와의 모든 상호작용 및 문서는 한국어로 작성되어야 합니다.
*   **코드 서식:** 표준 Python 및 JavaScript 서식 컨벤션을 따릅니다.
*   **API 키 관리:** `GROQ_API_KEY`는 `.env` 파일에 안전하게 저장하고 환경 변수를 통해 접근해야 합니다. 클라이언트 측에 노출되어서는 안 됩니다.
*   **`.env` 파일:** `.env` 파일은 프로그램적으로 수정되어서는 안 됩니다.
*   **버전 관리:** 코드 검토를 위해 풀 리퀘스트(`Pull Request`)를 사용하는 `feature -> develop -> main` 브랜칭 전략을 따릅니다.

## 프로젝트 구조

```
biztalk_llm/
├── .env                  # 환경 변수 (예: GROQ_API_KEY)
├── .gitignore            # Git ignore 파일
├── my-rules.md           # Gemini CLI (본 에이전트) 지침
├── PRD.md                # 제품 요구사항 문서 (Product Requirements Document)
├── 프로그램개요서.md       # 프로그램 개요 문서 (Program Overview Document)
├── backend/
│   ├── app.py            # Flask 애플리케이션 진입점, AI 통합 로직
│   └── requirements.txt  # Python 의존성 목록
├── frontend/
│   ├── css/
│   │   └── style.css     # 프론트엔드 스타일링
│   ├── js/
│   │   └── script.js     # 프론트엔드 JavaScript 로직 (API 호출, DOM 조작)
│   └── index.html        # 메인 프론트엔드 HTML 파일
└── .venv/                # Python 가상 환경
```