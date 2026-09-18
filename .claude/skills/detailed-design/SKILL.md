---
name: detailed-design
description: 소프트웨어 상세설계 및 단위 구현(A-SPICE SWE.3)을 작성할 때 사용합니다. 아키텍처 요소를 구현 단위(모듈/클래스/함수)로 분해하고, 호출관계, 공통 자료형, 함수 계약, 알고리즘, 상태전이, API 상세, 오류처리, 코딩/검증 규칙, SBOM/FOSS 점검, 단위-요구사항 할당, 추적성을 작성할 때 이 스킬을 로드하세요.
---

# 상세설계 스킬 (SWE.3)

`architecture-design` 스킬로 만든 아키텍처를 구현 가능한 수준까지 구체화하는 절차입니다. A-SPICE SWE.3와 ISO 26262 Part 6(안전 관련 코딩/구현 원칙)을 준수하고, `architecture-design`이 확립한 응집도/결합도·SOLID·인터페이스 전용 통신 원칙을 함수/모듈 수준까지 그대로 이어갑니다.

> 이 스킬의 체크리스트는 공개적으로 통용되는 표준 구조를 요약한 참고 자료입니다. 정확한 조항/문구는 실제 표준 원문과 대조하세요.

## 0. 템플릿 확인 (최우선, 그리고 이미 제공됨)

이 프로젝트는 공식 상세설계 산출물 템플릿을 이미 보유하고 있습니다. `references/detailed-design-template.md`를 먼저 읽으세요(TEMPLATE STATUS: PROVIDED) — 실제 문서(`WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/TPL-SWE3-001_...docx`)의 15개 절 구조와 각 절에 무엇을 채워야 하는지 정리되어 있습니다. 문서를 새로 만들지 말고, 그 템플릿을 프로젝트 규칙(`WP_Templates/Engineering/README.md`)대로 `<산출물 ID>_<산출물명>.docx`로 복사한 뒤 `anthropic-skills:docx` 스킬로 편집하세요.

> ⚠️ 이 템플릿은 "SW 품질교육을 위한 교육용 샘플"이며 저작권이 Synetics에 있습니다. 교육 과정 밖 배포·공개·상업적 이용은 사전 서면 승인이 필요합니다. 이 프로젝트 저장소가 그 범위를 벗어나 사용되고 있는 것으로 보이면 사용자에게 알리세요.

## 1. 입력 파악

`architecture-design`으로 작성된 아키텍처 문서와 인터페이스 명세, 그리고 공식 추적성 매트릭스(`requirements-analyst`의 `references/traceability.md` §0)에서 이번에 상세설계할 대상 아키텍처 요소(DES-nnn)와 그에 배분된 요구사항(ASIL 포함)을 확인합니다. 아키텍처 산출물이 없으면 먼저 `architecture-design`을 수행하거나 대상 요소 정보를 사용자에게 확인합니다.

## 2. 모듈 분해 (문서 §2)

각 아키텍처 요소(DES-nnn)를 구현 단위(모듈/클래스/함수 그룹)로 분해합니다. 각 단위에 `UNIT-nnn` ID, 책임(단일 책임 원칙 근거), 소스 위치(예정 경로)를 부여합니다. 분해 시 `architecture-design`의 `references/cohesion-coupling-solid.md` 체크리스트(응집도/SOLID)를 단위 수준에서도 그대로 적용합니다 — 별도로 다시 만들지 말고 그 파일을 참고합니다.

## 3. 상세 호출관계 (문서 §3) — 다이어그램

`references/diagrams-drawio.md`에 따라 함수/클래스 간 호출 순서, 의존 방향, 주요 데이터 흐름을 다이어그램으로 표현합니다. 이 프로젝트의 공식 다이어그램 산출물은 **drawio**(`TPL-SWE3-002_...drawio`)이므로, 초안은 Mermaid로 빠르게 잡아보되 최종 산출물은 drawio 파일로 작성합니다.

아키텍처 인터페이스(`architecture-design`의 `references/interface-design.md`)를 위반하는 호출(컴포넌트 경계를 넘어 인터페이스 없이 직접 호출)이 없는지 반드시 확인하세요.

## 4. 공통 자료형 (문서 §4)

공통 데이터 구조, 열거형, 단위, 유효범위, 불변조건, 직렬화 규칙을 정의합니다. `requirements-analyst`의 일관성 규칙(`references/requirement-writing-rules.md`)과 동일한 원칙으로, 기존 요구사항/아키텍처 문서에서 이미 쓰인 용어·단위와 충돌하지 않는지 확인합니다.

## 5. 핵심 함수 계약 (문서 §5)

`references/function-contracts-and-algorithms.md`의 계약 명세 형식(입력/출력/사전조건/사후조건/부작용/예외/시간제약)을 모든 핵심 함수에 적용합니다. 이는 `interface-design.md`의 인터페이스 명세 원칙을 함수 수준으로 확장한 것입니다.

## 6. 핵심 알고리즘 (문서 §6)

`references/function-contracts-and-algorithms.md`의 알고리즘 서술 규칙(의사코드/흐름도, 경계값 명시, 판단 조건 명확화)을 따릅니다. `requirements-analyst`의 명확성 원칙(모호한 표현 금지, 원자적 단계)을 알고리즘 서술에도 동일하게 적용합니다.

## 7. 정책 의사결정표 (문서 §7)

`references/function-contracts-and-algorithms.md`의 결정표(Decision Table) 형식으로 입력 조건 조합, 우선순위, 기대 동작, 충돌 해결 규칙을 표로 정의합니다. 조건 조합에 빠짐(gap)이나 중복(모순되는 두 행)이 없는지 반드시 검토합니다.

## 8. 상태전이 상세 (문서 §8)

`architecture-design`의 `references/architecture-diagrams.md`에 있는 State Machine 다이어그램을 상세화합니다 — 상태 저장 위치, 전이 함수, 이벤트, 가드 조건, 타이머, 초기화 동작을 명시합니다.

## 9. Web 및 API 상세 (문서 §9, 해당하는 경우)

엔드포인트, 요청/응답 스키마, 입력 검증 규칙, 오류 코드, 세션/보안 경계를 정의합니다. `interface-design.md`의 인터페이스 필수 항목을 프로토콜 수준으로 구체화한 것으로 취급합니다. 해당 없는(Web/API가 없는) 컴포넌트는 "해당 없음"으로 명시합니다.

## 10. 오류와 방어 동작 (문서 §10)

유효하지 않은 입력, 예외, 자원 실패에 대한 검출·처리·기록·복구를 기술합니다. 안전 관련(ASIL) 단위는 `architecture-design`의 `references/iso26262-part6-aspice-mapping.md`에 정의된 안전 메커니즘(오류 감지/안전 상태 전이 등)이 실제 코드 수준에서 어떻게 구현되는지 여기서 구체화합니다.

## 11. 코딩 및 검증 규칙 (문서 §11)

`references/coding-verification-rules.md`를 참고해 코딩 표준, 정적분석 규칙, 단위검증 방식, 커버리지 목표, 리뷰 기준을 정의합니다. 이 절차 자체의 실행(테스트 작성/실행)은 SWE.4(단위검증) 범위이므로, 여기서는 "무엇을 어떤 기준으로 검증할 것인가"만 정의합니다.

## 12. SBOM 및 오픈소스(FOSS) 점검 (문서 범위 밖, 별도 산출물)

Python(또는 해당 언어) 의존성을 사용하는 경우 `references/sbom-foss.md`에 따라 SBOM과 FOSS 라이선스 검토를 수행하고 공식 템플릿(`TPL-SBOM-001_...xlsx`)에 기록합니다. 실제 패키지 매니페스트/락파일에서 확인한 사실만 기록하고 버전·라이선스를 추측하지 않습니다.

## 13. 단위와 요구사항 할당 / 구현 경계 (문서 §12~13)

구현 단위를 아키텍처 요소·SW 요구사항·(예정) 단위시험에 연결하는 표를 작성하고, 생성 코드/외부 라이브러리/플랫폼 종속부/구현하지 않는 범위를 명시합니다.

## 14. 추적성 (문서 §14)

`requirements-analyst`의 `references/traceability.md` §0에 정의된 공식 매트릭스(`TPL-TRC-001_...xlsx`)에서 해당 요구사항 행을 찾아 `Detailed Design` 컬럼에 `UNIT-nnn` ID를, `Code` 컬럼에 예정 소스 경로를 채웁니다. 새 매트릭스나 형식을 만들지 않습니다.

## 15. 참고자료 (문서 §15) 및 출력

아키텍처 설계서, 코딩 규칙, API 문서, 외부 라이브러리 자료를 식별해 기록합니다. 마지막으로 다음을 요약해 보고합니다: 템플릿 준수 여부, 각 단위의 응집도/SOLID 점검 결과, 인터페이스 전용 통신 위반 여부, 함수 계약/결정표/상태전이 완결성, SBOM/FOSS 점검 결과, 추적성 매트릭스 갱신 여부.
