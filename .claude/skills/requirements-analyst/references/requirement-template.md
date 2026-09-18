TEMPLATE STATUS: PROVIDED

> 2026-09-18, MyClaudeNGV 프로젝트 사용자가 공식 템플릿을 제공했습니다. 아래 절 구조는
> `WP_Templates/Engineering/SoftwareRequirementsAnalysis/TPL-SWE1-001_SW 요구사항 명세서 템플릿.docx`
> 및 `TPL-SWE1-002_Use Case 명세서 템플릿.docx`의 실제 장 구조를 그대로 반영한 것입니다.
> 원본 docx의 각 절 안내문(작성 가이드 문구)은 실제 프로젝트 내용으로 교체해서 사용합니다.
> 이 파일이 갱신된 이후 작성되는 모든 SWE.1 산출물은 이 구조를 따릅니다. 이전에 기본 임시
> 템플릿(과거 버전)으로 작성된 산출물이 있다면 이 구조로 재구성을 제안하세요.

## TPL-SWE1-001 — SW 요구사항 명세서 (12개 장)

문서 상단에 문서통제/변경이력/작성-검토-승인 상태 표를 둔다(문서 ID, Revision, 프로세스,
효력일, 책임 조직, 베이스라인, 문서 상태/승인 여부 등 — OEM 원본 문서의 헤더 표 패턴 참고).

1. 목적 및 적용범위
   - 1.1 목적
   - 1.2 적용범위
   - 1.3 적용 경계
2. 요구사항 작성 및 판정 규칙
   - 2.1 식별 및 상태 규칙 (ID 체계는 `references/traceability.md` §1 준수, 상태값: Draft/Reviewed/Approved/Verified)
   - 2.2 품질 판정 기준 (EARS 패턴·원자성·명확성은 `references/requirement-writing-rules.md` 준수)
3. 상태와 우선순위 (요구사항 상태 정의, 우선순위 체계 — 필수/권고/선택 등)
4. 기능 및 안전 관련 SW 요구사항
   - 4.1 기능 요구사항 (아래 "SWR 항목" 필드 세트로 작성)
   - 4.2 안전 관련 SW 요구사항 (ASIL, 안전목표 연계 포함 — `references/iso26262-aspice-mapping.md` 참고)
5. 입력 데이터 사전 (각 입력 신호의 이름/타입/단위/범위/freshness 요건/오류 처리)
6. 외부 인터페이스 요구 (인터페이스 ID/방향/데이터/단위·범위/오류 처리 — OEM 인터페이스 계약과 매핑)
7. 비기능 및 환경 제약 (ISO 25010 매핑 — `references/nfr-iso25010.md` 참고)
8. 분석 결과와 가정 (해석 불가 항목, 가정, 확인 필요 사항 명시)
9. 하향 할당 및 검증 계획 (상위 요구 → SWR 할당 근거, 검증 수준/방법 개요)
10. 범위 밖 주장 (이 문서가 주장하지 않는 것 — 준수/인증/ASIL 달성 등)
11. 추적성 (양방향 추적 요약 — 상세는 공식 추적성 매트릭스 참조, `references/traceability.md`)
12. 참고자료

### SWR 항목 필드 (4.1/4.2 절에서 요구사항 1건당 사용)

| 필드 | 설명 |
|---|---|
| ID | SWR-nnn (`references/traceability.md` ID 체계) |
| 제목 | 한 줄 요약 |
| 설명 | EARS 패턴 서술 (`references/requirement-writing-rules.md`) |
| 출처(상위 요구) | OEM 요구 ID 등 상위 요구사항 참조 |
| 관련 다이어그램 | Use Case/Activity/Sequence/State Machine 중 해당 Mermaid 다이어그램 참조 |
| 우선순위 | 필수/권고/선택 |
| 안전 관련 여부 | 예/아니오, 예인 경우 ASIL 및 안전목표 ID |
| 수용기준(Acceptance Criteria) | 측정 가능한 통과/실패 조건 |
| 검증 방법 | 리뷰/분석/테스트/시뮬레이션 중 실행 가능한 구체적 절차, 검증 수준(단위/PC-SIL/통합 등) |
| 하위 추적 | 공식 추적성 매트릭스의 해당 행 참조 |
| 상태 | Draft/Reviewed/Approved/Verified |

## TPL-SWE1-002 — Use Case 명세서 (7개 장)

1. 목적 및 적용범위
   - 1.1 목적 / 1.2 적용범위 / 1.3 적용 경계 (SWE1-001과 동일 패턴)
2. 액터와 시스템 경계
3. Use Case 목록
4. Use Case 상세 (Use Case마다 반복)
   - 4.1 기본 정보 (ID, 이름, 관련 SWR)
   - 4.2 사전조건/트리거
   - 4.3 기본 흐름
   - 4.4 대안 흐름
   - 4.5 예외 흐름
   - 4.6 사후조건
5. 비대상 시나리오 (범위 밖으로 명시적으로 제외한 시나리오)
6. 추적성
7. 참고자료

## 비기능 요구사항(NFR) 항목 필드 (7장에서 사용)

| 필드 | 설명 |
|---|---|
| ID | NFR-nnn 또는 SWR-nnn(비기능 성격의 SWR) |
| 제목 | 한 줄 요약 |
| ISO 25010 특성/하위특성 | `references/nfr-iso25010.md` 표 참조 |
| 설명 | EARS 패턴 서술, 측정 가능한 목표치 포함 |
| 목표치(Target Metric) | 정량적 수치와 단위 |
| 검증 방법 | 실행 가능한 구체적 절차(도구/부하 조건/측정 방법/합격 기준) |
| 안전 관련 여부 | 예/아니오, 예인 경우 ASIL |
| 상위/하위 추적 | 공식 추적성 매트릭스 참조 |
| 상태 | Draft/Reviewed/Approved/Verified |
