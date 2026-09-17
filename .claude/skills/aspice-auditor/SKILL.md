---
name: aspice-auditor
description: Automotive SPICE(A-SPICE) 4.1 기준으로 프로세스 산출물(Work Product)을 감사/점검할 때 사용합니다. Capability Level(CL) 판정, 특히 CL2(Managed) 수준의 PA1.1(Process Performance)/PA2.1(Performance Management)/PA2.2(Work Product Management) 제네릭 프랙티스 점검, 프로세스별 Base Practice·산출물 점검, N/P/L/F 등급 산정, 감사 리포트(강점/약점/개선권고) 작성이 필요할 때 이 스킬을 로드하세요.
---

# A-SPICE 4.1 감사원 (Auditor) 스킬

Automotive SPICE(A-SPICE) 4.1 PAM(Process Assessment Model) 기준으로 프로젝트 산출물을 감사하기 위한 절차와 체크리스트입니다. 이 스킬은 **감사 방법론과 체크리스트**를 제공하며, 실제 산출물 파일은 사용자가 지정한 디렉토리/경로에서 직접 확인해야 합니다.

> 본 스킬의 세부 체크리스트는 공개된 A-SPICE PAM 구조(ISO/IEC 33020 제네릭 프랙티스 포함)를 요약한 참고 자료입니다. 실제 감사/심사 보고서 작성 시에는 반드시 공식 A-SPICE 4.1 PAM 원문과 문구를 대조해 확정하세요. 불확실한 항목은 추정하지 말고 "확인 필요"로 표기합니다.

## 0. 감사 대상 확정

먼저 다음을 확인합니다.
1. **대상 프로세스**: 예) SYS.2, SWE.1~SWE.6, SUP.1, SUP.8, SUP.9, SUP.10, MAN.3 등. 사용자가 특정하지 않았다면 어떤 프로세스를 볼지 질문하거나, 디렉토리 구조/파일명에서 유추합니다.
2. **감사 목표 Capability Level**: 이 스킬은 기본적으로 CL2 판정에 초점을 둡니다. CL2 판정을 위해서는 ISO/IEC 33020 규칙에 따라 다음이 모두 "Fully achieved(F)"여야 합니다.
   - PA 1.1 Process Performance (프로세스별 Base Practice 및 산출물 존재)
   - PA 2.1 Performance Management
   - PA 2.2 Work Product Management
3. **산출물 위치**: 감사할 문서/코드/기록이 있는 경로.

세부 등급 척도(NPLF, ISO/IEC 33020 기준):
| 등급 | 의미 | 달성률 |
|---|---|---|
| N (Not achieved) | 미달성 | 0~15% |
| P (Partially achieved) | 부분 달성 | >15~50% |
| L (Largely achieved) | 대부분 달성 | >50~85% |
| F (Fully achieved) | 완전 달성 | >85~100% |

CL2 판정 규칙: PA1.1=F **그리고** PA2.1=F **그리고** PA2.2=F 일 때만 해당 프로세스가 CL2를 달성한 것으로 간주합니다. 하나라도 F 미만이면 CL2 미달성이며, 어느 PA가 어느 등급인지, 무엇이 부족한지 리포트에 명시합니다.

## 1. PA1.1 (Process Performance) 점검 — 프로세스별 Base Practice/산출물

프로세스마다 요구되는 Base Practice(BP)와 산출물(Work Product, WP)이 다릅니다. `references/process-workproducts.md`에 자주 감사되는 프로세스(SYS.1~SYS.5, SWE.1~SWE.6, SUP.1, SUP.8, SUP.9, SUP.10, MAN.3)의 BP/WP 요약 체크리스트가 있습니다. 필요한 프로세스 섹션만 읽어서 사용하세요(전체를 한 번에 로드할 필요 없음).

각 BP에 대해:
- 실제 산출물에서 해당 BP의 증거(문서, 트레이서빌리티 항목, 리뷰 기록 등)를 찾습니다.
- 증거가 없거나 형식적으로만 존재하면 "부분/미달성"으로 표기하고 구체적 사유를 남깁니다.
- 산출물 간 트레이서빌리티(예: 요구사항 ↔ 아키텍처 ↔ 테스트케이스)가 A-SPICE의 핵심 관심사이므로, 단순히 문서 존재 여부가 아니라 **양방향 추적성**과 **일관성**을 확인합니다.

## 2. PA2.1 (Performance Management) 점검 — 제네릭 프랙티스

`references/generic-practices-cl2.md`의 GP 2.1.1~2.1.6을 참조해 아래 관점에서 증거를 확인합니다.

- 목표 설정(objectives), 계획/모니터링, 계획 대비 이탈 시 조정, 역할/책임 정의, 자원(인력/도구/스킬) 배정, 이해관계자 간 인터페이스 관리.
- 전형적 증거: 프로젝트 계획서, 일정/WBS, 진척 리뷰 기록, 조직도/RACI, 교육/역량 기록, 회의록/커뮤니케이션 기록.

## 3. PA2.2 (Work Product Management) 점검 — 제네릭 프랙티스

`references/generic-practices-cl2.md`의 GP 2.2.1~2.2.4를 참조해 아래 관점에서 증거를 확인합니다.

- 산출물에 대한 요구사항(양식/내용 기준) 정의 여부, 문서화·형상관리 요구사항 정의 여부, 식별·버전관리·형상통제 여부, 계획된 방식의 리뷰 및 리뷰 결과 반영 여부.
- 전형적 증거: 문서 템플릿/기준, 형상관리 도구 이력(버전, 베이스라인), 리뷰 기록(리뷰어, 발견사항, 조치 완료 확인), 변경관리 이력.

## 4. 등급 산정 및 판정

각 PA에 대해 세부 GP/BP 충족도를 취합해 N/P/L/F 등급을 산정합니다. 판단이 애매한 경우 보수적으로(낮은 등급으로) 판정하고 근거를 명시합니다. CL2 최종 판정은 §0의 규칙을 적용합니다.

## 5. 리포트 작성

`references/report-template.md`의 템플릿을 사용해 한국어로 감사 리포트를 작성합니다. 리포트에는 최소한 다음이 포함되어야 합니다.
- 감사 대상 프로세스/범위/일자
- PA1.1/PA2.1/PA2.2 각각의 등급과 근거
- 최종 CL2 달성 여부
- 강점(Strength), 약점/미흡사항(Weakness/Gap), 개선 권고(Improvement Recommendation) — 각 항목에 관련 산출물 경로 인용
- 확인이 필요해 보류한 항목 목록

리포트는 확정적 심사 결과가 아니라 **내부 사전 점검(pre-assessment/gap analysis)** 용도임을 리포트 상단에 명시하세요(공식 인증 심사는 공인 심사원이 수행).
