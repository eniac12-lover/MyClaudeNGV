TEMPLATE STATUS: PROVIDED

> 공식 템플릿:
> - `WP_Templates/Engineering/SoftwareComponentVerificationAndIntegrationVerification/TPL-SWE5-001_SW 통합전략 및 통합시험 명세서 템플릿.docx`
> - `WP_Templates/Engineering/SoftwareComponentVerificationAndIntegrationVerification/TPL-SWE5-002_SW 통합시험 케이스 템플릿.xlsx`
> - `WP_Templates/Engineering/SoftwareComponentVerificationAndIntegrationVerification/TPL-SWE5-003_SW 통합시험 결과서 템플릿.xlsx`
>
> ⚠️ 저작권/이용 제한: 교육용 샘플, 저작권 Synetics. 교육 과정 안 열람·복제·실습 사용만 허용, 과정 밖 배포·공개·상업적 이용은 사전 서면 승인 필요. 이 프로젝트 저장소가 그 범위를 벗어나 사용되고 있는 것으로 보이면 사용자에게 알리세요.

## 사용 방법

원본을 직접 수정하지 않습니다. `WP_Templates/Engineering/README.md`/`PRC-TPL-001` 규칙대로 복사한 뒤 `<산출물 ID>_<산출물명>.<확장자>`로 이름을 바꾸고 채웁니다. docx는 `anthropic-skills:docx`, xlsx는 `anthropic-skills:xlsx` 스킬 절차를 따릅니다(이 환경에 pandoc/LibreOffice/python이 없을 수 있으므로 `detailed-design`의 사례처럼 unzip 후 XML 직접 편집으로 대체할 수 있습니다).

## TPL-SWE5-001 문서 구조 (14개 절)

| 절 | 제목 | 대응 스킬 절차 |
|---|---|---|
| 1 | 목적 및 적용범위 | §1 입력 파악 |
| 2 | 통합 원칙 | §2 |
| 3 | 통합 항목과 순서 | §3 (아키텍처 `integration-order.md` 그대로 반영) |
| 4 | 환경 및 형상 | §4 |
| 5 | 진입 및 종료 기준 | §5 (커버리지 100% 포함) |
| 6 | 통합시험 케이스 요약 | §7 (TPL-SWE5-002) |
| 7 | 시험 설계기법 | §6 |
| 8 | 실행 및 결과 기록 규칙 | §9 (TPL-SWE5-003) |
| 9 | 회귀 전략 | §10 |
| 10 | 실패 및 편차 처리 | §11 |
| 11 | 추적성과 보고 | §12 |
| 12 | 적용 한계 | §13 |
| 13 | 추적성 | §12 |
| 14 | 참고자료 | §14 |

## TPL-SWE5-002 (통합시험 케이스) 컬럼

시트 표 `TPLSWE5002IntegrationCasesTable`, 9행 헤더/10행부터 데이터.

| 컬럼 | 의미 |
|---|---|
| Test ID | 케이스 고유 ID (예: `ITC-001`) |
| Trace | 근거 인터페이스 ID/요구사항 ID (`interface-design.md`, `TPL-TRC-001`) |
| Integration Item | 이 케이스가 검증하는 통합 항목(컴포넌트 조합) |
| Stimulus | 입력/자극(호출, 이벤트, 결함 주입 등) |
| Expected Result | 기대 결과(인터페이스 계약의 사후조건/오류 처리와 일치해야 함) |
| Technique | ISO 26262 통합시험 방법 + 도출 기법 (예: "인터페이스 시험 + 경계값분석") |
| Automation | 자동화 여부(Yes/No/부분) |

## TPL-SWE5-003 (통합시험 결과서) 시트

**Integration Results** (`TPLSWE5003IntegrationResultsTable`, 9행 헤더/10행부터):

| 컬럼 | 의미 |
|---|---|
| Test ID | TPL-SWE5-002의 Test ID와 일치 |
| Trace | 케이스와 동일 |
| Result | Pass/Fail/Blocked |
| Actual Result | 실제 관찰된 결과 |
| Evidence Locator | 로그/커버리지 리포트/캡처 경로 |
| Defect ID | 실패 시 결함 식별자 |
| Disposition | 처리 방침(재시험/수정 후 재시험/허용된 편차 등) |

**Run Summary** (`TPLSWE5003RunSummaryTable`): Run ID, Date, Baseline, Environment, Planned, Pass, Fail, Overall, Limitation — 실행 회차별 요약.
