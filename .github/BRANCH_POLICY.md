# Git 브랜치 정책 (AI 지원 개발 / "바이브 코딩" 워크플로우)

AI 에이전트(Claude Code 등)가 코드 대부분을 작성하는 프로젝트에서 일반적으로 권장되는 GitHub 워크플로우입니다. 핵심 목적은 **AI가 만든 변경이 사람의 검토·CI 검증 없이 곧바로 `main`에 들어가지 않도록** 하는 것입니다.

## 브랜치 전략

- `main`: 배포 가능한 안정 브랜치. **보호됨** — 직접 push 금지, 반드시 Pull Request를 통해서만 변경.
- 작업 브랜치 네이밍(Conventional Commits 접두어와 동일하게 맞춤):
  - `feature/<설명>` — 신규 기능
  - `fix/<설명>` — 버그 수정
  - `refactor/<설명>` — 동작 변경 없는 리팩터링
  - `docs/<설명>` — 문서/스킬/에이전트 정의 변경
  - `chore/<설명>` — 빌드/CI/설정 등 기타 작업
- 브랜치는 짧게 유지하고, PR 하나 = 논리적 변경 하나 단위로 쪼갭니다 — AI가 만든 diff를 사람이 리뷰하기 쉽게 유지하기 위함입니다.

## PR / 머지 규칙

- 모든 변경(AI 에이전트가 만든 변경 포함)은 PR을 통해 `main`에 병합합니다.
- **CI(GitHub Actions) 상태 체크가 모두 통과해야 병합 가능**합니다(`.github/workflows/ci.yml`) — 이것이 AI 실수/환각으로 인한 회귀를 병합 전에 잡아내는 핵심 게이트입니다.
- `main`으로의 force-push와 브랜치 삭제는 금지합니다.
- 병합 방식은 **Squash merge**를 권장합니다 — TDD Red/Green/Refactor 등 AI가 만든 중간 커밋을 하나의 의미 있는 커밋으로 정리합니다.
- 사람 승인(Required reviewers)은 프로젝트 인원 구성에 따라 선택 사항입니다. 1인 프로젝트라면 "CI 통과"를 필수 게이트로, 팀 프로젝트라면 최소 1인 승인을 추가하세요.

## 커밋 메시지

[Conventional Commits](https://www.conventionalcommits.org/) 스타일을 권장합니다: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`. AI가 생성하는 커밋도 이 형식을 따르면 변경 이력을 사람이 읽기 쉽고, 추후 자동 변경로그 생성에도 유리합니다.

## 이 정책을 실제로 적용하는 방법 (GitHub 저장소 설정)

이 문서와 `.github/workflows/ci.yml`은 저장소 파일이라 커밋만으로 적용되지만, **브랜치 보호 규칙(Branch Protection Rule) 자체는 GitHub 저장소 설정이라 API/UI로 별도 적용해야 합니다** — Claude Code가 이 저장소의 git 파일을 커밋할 수는 있어도, GitHub 계정 권한으로 저장소 설정을 바꾸는 것은 별도 인증이 필요해 이 환경에서 직접 실행하지 않았습니다.

### 방법 1 — GitHub 웹 UI
`Settings → Branches → Add branch protection rule` (또는 신규 UI는 `Rulesets`)에서 `main`에 대해:
- Require a pull request before merging (필요 시 "Require approvals" 추가)
- Require status checks to pass before merging → `CI / test-and-quality` 체크 선택
- Require branches to be up to date before merging
- Restrict force pushes
- Restrict deletions

### 방법 2 — `gh` CLI (설치·로그인 되어 있다면 사용자가 직접 실행)
```
gh api repos/eniac12-lover/MyClaudeNGV/branches/main/protection \
  --method PUT \
  -f required_status_checks='{"strict":true,"contexts":["test-and-quality"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":0}' \
  -f restrictions=null \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```
