TEMPLATE STATUS: PROVIDED

> 공식 템플릿:
> - `WP_Templates/Engineering/SoftwareVerification/TPL-SWE6-001_SW 검증 명세서 템플릿.xlsx`
> - `WP_Templates/Engineering/SoftwareVerification/TPL-SWE6-002_SW 검증 결과서 템플릿.xlsx`
>
> ⚠️ 저작권/이용 제한: 교육용 샘플, 저작권 Synetics. 교육 과정 안 열람·복제·실습 사용만 허용, 과정 밖 배포·공개·상업적 이용은 사전 서면 승인 필요. 이 프로젝트 저장소가 그 범위를 벗어나 사용되고 있는 것으로 보이면 사용자에게 알리세요.

## 사용 방법

원본을 직접 수정하지 않습니다. `WP_Templates/Engineering/README.md`/`PRC-TPL-001` 규칙대로 복사한 뒤 `<산출물 ID>_<산출물명>.xlsx`로 이름을 바꾸고 채웁니다(`anthropic-skills:xlsx` 스킬 절차 사용, 이 환경에 python/LibreOffice가 없으면 다른 스킬들처럼 unzip 후 XML 직접 편집으로 대체 가능).

## TPL-SWE6-001 (SW 검증 명세서) 컬럼

시트 표 `TPLSWE6001VerificationSpecificationTable`, 9행 헤더/10행부터 데이터.

| 컬럼 | 의미 |
|---|---|
| Test ID | 케이스 고유 ID (예: `SYT-001`) |
| SW Req | 근거 요구사항 ID (`requirements-analyst`가 작성한 SR/SWR/NFR) |
| Level/Environment | 시험 수준/환경(예: SW 단독, HIL 없이 SW-only 시스템 시험 등) |
| Stimulus | 입력값/시나리오 |
| Expected Result | 기대 결과(요구사항 명세서에 근거, 임의 가정 금지) |
| Technique | 적용한 테스트 설계 기법(`tdd`의 `references/test-design-techniques.md`에서 선택) |
| Execution | 실행 방법(수동/자동) |

기능 요구사항 케이스는 이 표에, 비기능 요구사항 케이스는 별도 "비기능 테스트 케이스" 시트를 추가해 `requirements-analyst`의 `references/nfr-iso25010.md` 품질특성별로 구분합니다(이 템플릿에는 비기능 시트가 기본 포함되어 있지 않으므로, 필요 시 위 표와 동일한 컬럼 구성으로 새 시트를 추가하고 `ISO25010 특성` 컬럼을 추가합니다).

## TPL-SWE6-002 (SW 검증 결과서) 시트

**Verification Results** (`TPLSWE6002VerificationResultsTable`):

| 컬럼 | 의미 |
|---|---|
| Test ID | TPL-SWE6-001의 Test ID와 일치 |
| SW Req | 케이스와 동일 |
| Result | Pass/Fail/Blocked |
| Actual Result | 실제 관찰된 결과 |
| Evidence Locator | 로그/캡처/리포트 경로 |
| Execution Time | 실행 일시 |
| Scope Note | 이 실행이 다루지 못한 범위(있는 경우) |

**Summary** (`TPLSWE6002SummaryTable`): 항목, 계획, 실행, Pass, Fail, 미실행, 판정, 제한 — 실행 회차 요약.
