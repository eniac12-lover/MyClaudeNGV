# ISO 26262 / A-SPICE 요구사항 정합성 가이드

> 아래는 공개적으로 통용되는 ISO 26262(도로차량 기능안전) 및 A-SPICE 요구공학 프로세스의 핵심 개념을 요약한 것입니다. 정확한 조항 번호와 문구는 표준 원문 및 프로젝트의 기능안전 계획(Safety Plan)과 대조하세요.

## ISO 26262 핵심 개념과 요구사항 속성

| 개념 | 설명 | 요구사항에 반영할 속성 |
|---|---|---|
| HARA (Hazard Analysis and Risk Assessment) | 위험원 분석 및 리스크 평가로 안전목표(Safety Goal) 도출 | 안전 관련 요구사항은 관련 Safety Goal ID를 상위 추적으로 명시 |
| ASIL (A/B/C/D, QM) | 위험도에 따른 안전무결성 수준 | 모든 안전 관련 요구사항에 ASIL 등급 필드 필수 |
| Safety Goal (SG) | 최상위 안전요구, HARA의 산출물 | FSR/TSR의 최상위 출처로 추적 |
| FSR (Functional Safety Requirement) | 안전목표를 시스템 기능 수준에서 구체화 | SYS.2 산출물과 연계, ASIL 상속 |
| TSR (Technical Safety Requirement) | FSR을 기술적으로 구체화(HW/SW 배분 포함) | SYS.3/SWE.1과 연계, ASIL 상속 또는 분해(decomposition) 근거 명시 |
| 안전 분석(FMEA/FTA 등) | 고장 모드/영향 분석 | 도출된 요구사항에 분석 산출물 ID를 근거로 링크 |
| ASIL 분해(Decomposition) | 상위 ASIL을 하위 요소에 분배 시 규칙 준수 | 분해 적용 시 분해 방식과 독립성 근거를 요구사항에 명시 |

## 안전 관련 요구사항 작성 시 필수 필드

`references/requirement-template.md`의 공통 필드 외에 안전 관련 요구사항은 다음을 추가로 포함합니다.
- ASIL 등급 (QM/A/B/C/D)
- 상위 Safety Goal ID
- 안전 분석 근거(FMEA/FTA 등 산출물 ID), 해당 시
- ASIL 분해 여부 및 근거(해당 시)
- 검증 방법이 해당 ASIL 등급에 요구되는 엄격도를 충족하는지(예: 높은 ASIL일수록 독립적 검증/정형 기법 등이 요구될 수 있음 — 프로젝트 Safety Plan 확인)

## A-SPICE 요구공학 프로세스와의 연계

| 프로세스 | 목적 | 이 스킬이 지원하는 부분 |
|---|---|---|
| SYS.1 요구사항 도출 | 이해관계자 요구 수집 | STR 항목 작성, 출처 기록 |
| SYS.2 시스템 요구사항 분석 | 시스템 요구사항 구체화, 분류, 검증기준 정의 | FR/NFR 작성, EARS 서술, 검증기준, STR↔SR 추적 |
| SWE.1 소프트웨어 요구사항 분석 | 시스템 요구로부터 SW 요구 도출 | SWR 작성, SR↔SWR 추적 |
| SUP.10 변경요청 관리 | 요구사항 변경 이력 관리 | 요구사항 상태(Draft/Reviewed/Approved) 및 변경 이력 필드로 연계 |

이 스킬로 작성한 요구사항이 실제 A-SPICE CL2 감사 대상이 되는 경우, `aspice-auditor` 스킬/`aspice-cl2-auditor` 서브 에이전트로 점검할 수 있습니다(추적성·리뷰기록·형상관리 등 PA2.1/PA2.2 관점은 별도 관리 필요).
