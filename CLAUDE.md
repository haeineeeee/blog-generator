# Blog Generator Agent

## 프로젝트 개요
키워드를 입력받아 단계별로 고품질 블로그 글을 생성하는 AI 에이전트 서비스.

## 기술 스택
- **언어**: Python 3.11+
- **프레임워크**: FastAPI
- **LLM**: Anthropic Claude API (claude-sonnet-4-5-20250929)
- **발행**: WordPress REST API, 로컬 마크다운 파일 저장
- **패키지 관리**: pip + requirements.txt
- **테스트**: pytest

## 아키텍처
```
blog-generator/
├── app/
│   ├── main.py              # FastAPI 엔트리포인트
│   ├── config.py            # 설정 관리 (API 키, WordPress 설정 등)
│   ├── api/
│   │   └── routes.py        # API 엔드포인트
│   ├── agents/
│   │   ├── outline.py       # 아웃라인 생성 에이전트
│   │   ├── writer.py        # 초안 작성 에이전트
│   │   └── reviewer.py      # 검토/수정 에이전트
│   ├── services/
│   │   ├── llm.py           # Claude API 클라이언트
│   │   ├── wordpress.py     # WordPress 발행
│   │   └── markdown.py      # 마크다운 파일 저장
│   └── models/
│       └── schemas.py       # Pydantic 모델
├── output/                  # 생성된 마크다운 파일 저장 디렉토리
├── prompts/                 # 프롬프트 템플릿 (txt/yaml)
├── tests/
├── requirements.txt
├── .env.example
└── CLAUDE.md
```

## 핵심 워크플로우
1. **키워드 입력** → 사용자가 키워드/주제 입력
2. **아웃라인 생성** → 글의 구조(제목, 소제목, 핵심 포인트) 생성
3. **초안 작성** → 아웃라인 기반으로 본문 작성
4. **검토/수정** → 문법, 가독성, SEO 관점에서 검토 후 수정
5. **완성/발행** → 마크다운 저장 또는 WordPress 발행

## 코딩 컨벤션
- Python 코드는 PEP 8 준수
- 함수/변수명: snake_case
- 클래스명: PascalCase
- 타입 힌트 사용
- docstring: 공개 함수에만 간결하게 작성
- 환경 변수: .env 파일로 관리 (python-dotenv)
- 비동기 처리: async/await 사용 (FastAPI 기본)

## API 엔드포인트 설계
- `POST /generate/outline` - 키워드로 아웃라인 생성
- `POST /generate/draft` - 아웃라인으로 초안 생성
- `POST /generate/review` - 초안 검토/수정
- `POST /generate/full` - 키워드 → 완성글 한번에 생성
- `POST /publish/wordpress` - WordPress 발행
- `POST /publish/markdown` - 마크다운 파일 저장

## 명령어
- `pip install -r requirements.txt` - 의존성 설치
- `uvicorn app.main:app --reload` - 개발 서버 실행
- `pytest` - 테스트 실행

## 주의사항
- API 키는 절대 코드에 하드코딩하지 않음 (.env 사용)
- LLM 호출 시 에러 핸들링 필수 (rate limit, timeout 등)
- 프롬프트는 코드와 분리하여 prompts/ 디렉토리에서 관리
