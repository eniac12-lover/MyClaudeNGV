# SBOM-001 Python 의존성 SBOM / FOSS 라이선스 목록 (Phase 1 — Core Input & Lock)

> ⚠️ 본 문서는 **교육용 가상 프로젝트 산출물**이다. 공식 템플릿(`WP_Templates/Engineering/
> SoftwareDetailedDesignAndUnitConstruction/TPL-SBOM-001_Python 의존성 SBOM FOSS 라이선스
> 목록 템플릿.xlsx`)은 "SW 품질교육을 위한 교육용 샘플"이며 저작권이 Synetics에 있다.
> 이번 작업 지시는 Phase 종료 시 공식 docx/xlsx/drawio로 변환하기로 확정한 기존 프로젝트
> 결정에 따라 `.md`로 작성하도록 명시적으로 지정했으므로 원본 템플릿 파일은 수정/복제하지
> 않았다. 시트 구조(SBOM / FOSS Review / Change History)는
> `.claude/skills/detailed-design/references/sbom-foss.md`가 요약한 정의를 그대로 따른다.
> **문서 상태: 미승인(Draft).**

## 문서 통제

| 항목 | 값 |
|---|---|
| 문서 ID / 문서명 | SBOM-001_Python의존성SBOM |
| Revision | 1.0 (Phase 1 baseline) |
| 대상 | `SWD-001_SW상세설계서`가 정의한 Phase1 구현 단위(UNIT-001~026), `src/childlock/` 예정 트리 |
| 작성일 | 2026-09-18 |
| 문서 상태 | 교육 시나리오 초안 — 실제 승인 미수행 |

### 변경 이력

| Revision | 변경일 | 작성 역할 | 변경 내용 | 검토 상태 | 승인 상태 |
|---|---|---|---|---|---|
| 1.0 | 2026-09-18 | detailed-design 서브에이전트 | 최초 작성. 실제 의존성 매니페스트 부재 확인, 외부 패키지 없음으로 확정 | 미수행 | 미수행 |

---

## 조사 방법 및 근거 (추측 금지 원칙 준수)

`Glob`/`Bash find`로 프로젝트 루트를 확인한 결과, 다음 의존성 매니페스트/락파일이
**존재하지 않음**을 확인했다(2026-09-18 기준):

- `requirements.txt` — 없음
- `requirements-dev.txt` — 없음(단, `.github/workflows/ci.yml`이 참조하도록 조건부 설치
  구문은 있으나 파일 자체는 아직 생성되지 않음)
- `pyproject.toml` — 없음
- `Pipfile` / `Pipfile.lock` — 없음
- `poetry.lock` — 없음

또한 `src/` 디렉터리 자체가 아직 생성되지 않았다(본 상세설계 단계는 `SWD-001`에서
소스 파일 경로만 확정했고, 실제 `import` 문이 존재하는 코드는 아직 없다 — `coding`
서브에이전트의 구현 단계에서 실제 SBOM 재확인이 필요하다).

`.github/workflows/ci.yml`은 `lizard`, `pylint`, `radon`, `coverage`를 CI 환경에
설치하지만, 이들은 **프로젝트 코드가 런타임에 의존(import)하는 패키지가 아니라
품질 게이트 실행용 개발 도구**이므로 SBOM(런타임/배포 의존성) 대상이 아니다(SBOM
시트 정의 "Distribution: 최종 배포물에 포함되는지" 기준으로 명확히 구분).

## SBOM 시트

| Package | Version | Dependency Type | SPDX | Evidence Type | Evidence Locator | Distribution | Remark |
|---|---|---|---|---|---|---|---|
| (해당 없음 — 외부 런타임 의존성 없음) | — | — | — | 매니페스트/락파일 부재 확인 | `find`/`Glob` 결과(위 "조사 방법" 절), 2026-09-18 | — | Phase1 상세설계(`SWD-001`)가 계획한 구현은 표준 라이브러리(`dataclasses`, `enum`, `typing`, `abc`, `collections`, `queue`, `time`)만 사용하며, 이들은 CPython 배포판에 내장되어 있어 별도 패키지 설치·SBOM 추적 대상이 아니다(SPDX 기준 별도 라이선스 고지 불필요 — Python Software Foundation License, 프로젝트 코드와 별도 배포 단위) |

## FOSS Review 시트

| Review ID | Scope | Criterion | Evidence | Result | Owner | Date | Limitation |
|---|---|---|---|---|---|---|---|
| FR-001 | Phase1 구현 예정 범위(`src/childlock/*`) | 카피레프트 라이선스(GPL 계열) 포함 시 배포 방식 검토 | 외부 패키지 없음(위 SBOM 시트) | Pass(해당 없음) | detailed-design 서브에이전트 | 2026-09-18 | 해당 없음 — 재평가 조건: 구현 단계에서 외부 패키지가 실제로 추가되면 즉시 본 문서를 갱신하고 FOSS Review를 재수행해야 함 |
| FR-002 | Phase1 구현 예정 범위 | 상업적 이용 제한 여부 | 상동 | Pass(해당 없음) | detailed-design 서브에이전트 | 2026-09-18 | 상동 |
| FR-003 | Phase1 구현 예정 범위 | 특허 조항 유무 | 상동 | Pass(해당 없음) | detailed-design 서브에이전트 | 2026-09-18 | 상동 |
| FR-004 | 표준 라이브러리 사용(`dataclasses` 등) | Python Software Foundation License 조건 적합성 | Python 3.14 배포 조건(PSF License, 별도 설치·전이 의존성 없음) | Pass | detailed-design 서브에이전트 | 2026-09-18 | 표준 라이브러리이므로 프로젝트 배포물에 별도로 포함/재배포되지 않음(런타임 환경이 이미 제공) |

## Change History 시트

| Revision | 변경일 | 작성 역할 | 변경 내용 | 검토 상태 | 승인 상태 |
|---|---|---|---|---|---|
| 1.0 | 2026-09-18 | detailed-design 서브에이전트 | 최초 작성(외부 의존성 없음 확정) | 미수행 | 미수행 |

---

## 재확인 필요 시점 (구현 단계 인계 사항)

`coding` 서브에이전트가 실제 구현 중 아래 중 하나라도 발생하면 **본 SBOM 문서를 즉시
갱신**해야 한다(추측이 아니라 실제 설치/임포트 발생 시점에 사실 기반으로 갱신).

1. `pip install` 또는 `requirements*.txt`/`pyproject.toml`에 외부 패키지가 추가되는 경우.
2. `queue.Queue`/`collections.deque`/`time.monotonic` 외에 표준 라이브러리 밖의 기능이
   필요해지는 경우(예: 성능상의 이유로 서드파티 큐/직렬화 라이브러리 도입).
3. 테스트 하네스가 `unittest` 외 도구(예: `pytest` 플러그인)를 실제로 설치하는 경우 —
   `CLAUDE.md`가 `unittest`를 지정했으므로 원칙적으로 발생해서는 안 되나, 발생 시
   정책 위반으로 별도 보고해야 한다.
