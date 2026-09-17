# 프로세스별 Base Practice / 산출물(Work Product) 요약 체크리스트 (PA1.1 점검용)

> 아래 내용은 A-SPICE PAM에 공개적으로 정리되어 통용되는 프로세스 목적/BP/WP를 실무 감사에서 쓰기 쉽게 **요약**한 것입니다. 정확한 BP 번호·문구·필수 산출물 특성(Work Product Characteristics)은 공식 A-SPICE 4.1 PAM 원문을 반드시 대조하세요. 특정 프로세스 섹션만 필요 시 읽어서 사용합니다.

## SYS.1 요구사항 도출 (Requirements Elicitation)
- 목적: 이해관계자 요구사항을 수집·기록.
- 확인 포인트: 이해관계자 요구사항 문서, 요구사항 출처(고객/규정/표준) 기록, 변경 이력.
- 대표 산출물: Stakeholder Requirements, 회의록/인터뷰 기록.

## SYS.2 시스템 요구사항 분석
- 목적: 이해관계자 요구사항을 시스템 요구사항으로 구체화, 분류(기능/비기능), 우선순위, 검증기준 정의.
- 확인 포인트: 요구사항 ID 체계, 검증기준(acceptance criteria), Stakeholder 요구사항과의 양방향 추적성.
- 대표 산출물: System Requirements Specification, 추적성 매트릭스(Traceability Matrix).

## SYS.3 시스템 아키텍처 설계
- 목적: 시스템을 요소(하드웨어/소프트웨어 등)로 분해, 인터페이스 정의, 요구사항 배분.
- 확인 포인트: 아키텍처가 요구사항을 모두 커버하는지(추적성), 동적/정적 관점, 자원 사용량 추정, 인터페이스 정의.
- 대표 산출물: System Architectural Design, Interface Requirement/Design, Traceability(요구사항↔아키텍처).

## SYS.4 시스템 통합 및 통합 테스트
- 목적: 시스템 요소 통합 전략 수립, 통합 테스트 수행.
- 확인 포인트: 통합 전략/순서, 테스트 케이스와 아키텍처 요소의 추적성, 테스트 결과 및 결함 처리.
- 대표 산출물: Integration Test Strategy/Spec, Integration Test Results, Traceability(아키텍처↔통합테스트).

## SYS.5 시스템 검증 테스트 (Qualification Test)
- 목적: 시스템이 요구사항을 충족하는지 검증.
- 확인 포인트: 테스트 케이스와 시스템 요구사항의 추적성, 테스트 커버리지, 결과의 회귀/재검증 관리.
- 대표 산출물: System Qualification Test Spec/Results, Traceability(요구사항↔검증테스트).

## SWE.1 소프트웨어 요구사항 분석
- 확인 포인트: 시스템 요구사항으로부터 SW 요구사항 도출, 인터페이스/자원 제약 반영, 검증기준 정의, 추적성.
- 대표 산출물: Software Requirements Specification, Traceability(시스템요구↔SW요구).

## SWE.2 소프트웨어 아키텍처 설계
- 확인 포인트: SW 아키텍처가 SW 요구사항을 모두 커버, 컴포넌트 간 인터페이스/동적 동작 정의, 자원 사용 추정.
- 대표 산출물: Software Architectural Design, Traceability(SW요구↔아키텍처).

## SWE.3 소프트웨어 상세설계 및 단위 구현
- 확인 포인트: 상세설계가 아키텍처를 구체화, 코딩 표준 준수, 단위 구현과 설계의 추적성.
- 대표 산출물: Software Detailed Design, Source Code, Traceability(아키텍처↔상세설계↔코드).

## SWE.4 소프트웨어 단위 검증 (Unit Verification)
- 확인 포인트: 단위 테스트/정적분석 전략, 커버리지 기준 및 실제 달성률, 결함 처리.
- 대표 산출물: Unit Verification Strategy/Spec, Unit Test Results, 코드 커버리지 리포트.

## SWE.5 소프트웨어 통합 및 통합 테스트
- 확인 포인트: SW 통합 전략, 통합 테스트와 아키텍처 요소의 추적성, 결과 관리.
- 대표 산출물: Software Integration Test Spec/Results, Traceability.

## SWE.6 소프트웨어 검증 테스트 (Qualification Test)
- 확인 포인트: SW 요구사항 대비 테스트 커버리지, 추적성, 결과/회귀 관리.
- 대표 산출물: Software Qualification Test Spec/Results, Traceability(SW요구↔검증테스트).

## SUP.1 품질보증 (Quality Assurance)
- 확인 포인트: QA 활동이 계획대로 독립적으로 수행되는지, 프로세스/산출물 부적합 발견 시 에스컬레이션 및 추적 관리, 경영진 보고.
- 대표 산출물: QA Plan, QA 감사/점검 기록, 부적합(Non-conformance) 리스트 및 조치 이력.

## SUP.8 형상관리 (Configuration Management)
- 확인 포인트: 형상항목 식별 기준, 베이스라인 관리, 변경 통제, 형상감사(Configuration Status Accounting/Audit).
- 대표 산출물: Configuration Management Plan, 형상 항목 목록, 베이스라인 기록, 형상관리 도구 이력.

## SUP.9 문제해결 관리 (Problem Resolution Management)
- 확인 포인트: 문제(결함) 기록·분류·우선순위·원인분석·해결·종결까지의 전체 라이프사이클 관리, 재발 방지.
- 대표 산출물: Problem Resolution Plan/절차, 문제 기록(Problem Report) 이력, 상태 추적.

## SUP.10 변경요청 관리 (Change Request Management)
- 확인 포인트: 변경요청 접수·영향분석·승인·구현·검증·종결의 전체 흐름 관리, 영향 받는 산출물과의 연계.
- 대표 산출물: Change Request 기록, 영향분석 문서, 승인 이력(CCB 등), 변경 이력과 형상관리 연계.

## MAN.3 프로젝트 관리
- 확인 포인트: 프로젝트 범위/일정/자원/리스크 계획 수립 및 실제 모니터링, 계획 대비 이탈 시 조정, 이해관계자 커뮤니케이션.
- 대표 산출물: Project Plan, WBS/일정, 리스크 관리 대장, 진척 보고서, 회의록.

## 공통 감사 팁
- **추적성(Traceability)**이 A-SPICE 감사에서 가장 자주 지적되는 항목입니다. 요구사항-설계-구현-테스트 간 양방향 추적이 실제로 유지되는지(문서상 존재가 아니라 최신 상태로 일관되는지) 반드시 샘플링해서 확인하세요.
- 리뷰/테스트 "완료"로 표시된 항목이 실제 근거 기록(리뷰 서명, 테스트 로그, 결함 종결 근거)을 갖는지 샘플 확인합니다.
- 프로세스별 대표 산출물이 하나도 없으면 해당 프로세스는 PA1.1부터 N(미달성)이며, CL2 판정 자체가 불가합니다.
