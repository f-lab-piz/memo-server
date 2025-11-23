# memo-server

FastAPI 기반의 간단한 메모 서비스입니다. 로컬 실행, Docker 이미지 빌드, CI/CD(ghcr + memo-deploy 연동) 예제를 포함합니다.

## 로컬 실행
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 엔드포인트
- `GET /health` 헬스체크
- `GET /memos` 메모 목록
- `POST /memos` 메모 생성 `{ "title": "...", "content": "..." }`
- `GET /memos/{id}` 단일 조회
- `PUT /memos/{id}` 수정
- `DELETE /memos/{id}` 삭제

## 테스트
```bash
pytest
```

## Docker 빌드
```bash
docker build -t memo-server:local .
```

## 환경 변수
- `DATABASE_URL` (기본: `sqlite:///./memo.db`)

## CI/CD 개요
`main`, `dev` 브랜치에 push 시 GitHub Actions가 동작합니다.
1) 현재 시각을 태그로 이미지 빌드 후 GHCR에 push
2) `memo-deploy` 레포의 대응 브랜치(main/dev)에서 Helm values의 이미지 태그 업데이트 후 커밋/푸시
3) `dev`는 자동 실행, `main`은 GitHub 환경 보호(Production) 승인 후 실행하도록 설계

필요한 시크릿/변수는 `.github/workflows/build-and-deploy.yml`을 참고하세요.

### GitHub Actions 시크릿/변수 예시
- `GHCR_TOKEN` (secret): GHCR 푸시용 토큰  
  - fine-grained: `write:packages`  
  - classic: `packages:write`
- `DEPLOY_REPO_TOKEN` (secret): `memo-deploy` 레포에 push 가능한 토큰  
  - fine-grained: `Contents: Read/Write`  
  - classic: `repo`
- `DEPLOY_REPO` (repo variable): `org/repo` 형식으로 `memo-deploy` 위치를 재정의할 때 사용 (없으면 `${{ github.repository_owner }}/memo-deploy`)
- GitHub Environments: `development`(dev), `production`(main) – production에 승인자 설정

### memo-deploy Helm 값 파일 위치
- dev: `helm/memo-server/values.yaml`
- prod: `helm/memo-server/values-prod.yaml`
