---
name: architecture-design
description: 시스템/소프트웨어 아키텍처를 설계할 때 사용합니다. A-SPICE(SYS.3/SWE.2)와 ISO 26262 Part 6 아키텍처 설계 원칙, 높은 응집력/낮은 결합도, SOLID 원칙, 인터페이스 기반 통신, 변경 유연성, 컴포넌트 통합 순서 정의가 필요한 아키텍처 산출물을 만들 때 이 스킬을 로드하세요.
---

# 아키텍처 설계 스킬

A-SPICE와 ISO 26262 Part 6을 준수하면서, 높은 응집력/낮은 결합도, SOLID 원칙, 인터페이스 기반 통신, 변경 유연성을 갖춘 아키텍처를 설계하기 위한 절차입니다.

> 이 스킬의 체크리스트는 공개적으로 통용되는 표준 구조를 요약한 참고 자료입니다. 정확한 조항/문구는 실제 표준 원문과 대조하세요.

## 0. 템플릿 확인 (최우선)

`references/architecture-template.md`를 읽습니다.
- "TEMPLATE STATUS: PROVIDED"면 그 템플릿을 그대로 따릅니다. 이 스킬의 나머지 절차는 템플릿의 각 항목을 채우는 방법을 안내하는 보조 자료로만 사용합니다.
- "TEMPLATE STATUS: PENDING"이면 사용자가 아직 양식을 제공하지 않은 것입니다. 작업을 멈추지 말고 그 파일의 **기본 임시 양식**으로 진행하되, 산출물 상단에 "⚠️ 사용자 지정 아키텍처 설계서 양식 미제공 — 기본 양식 사용 중"이라고 명시합니다. 사용자가 나중에 양식을 제공하면 그 파일을 교체(PROVIDED로 변경)하고 기존 산출물의 재구성을 제안합니다.

## 1. 입력 파악

작업 디렉토리에서 관련 요구사항 산출물(`requirements-analyst` 스킬로 작성된 SR/SWR/NFR, 안전요구 ASIL 등)과 추적성 매트릭스(`traceability/requirements-traceability.csv`)를 `Glob`/`Grep`/`Read`로 찾아 설계 범위와 제약(ASIL, 성능/신뢰성 목표 등)을 파악합니다. 요구사항 산출물이 없으면 사용자에게 설계 범위와 주요 제약을 질문합니다.

## 2. 후보 아키텍처 구조 제안 (필수 — 상세 설계 전에 반드시 수행)

**상세 설계로 바로 들어가지 마세요.** `references/architecture-alternatives.md`를 참고해 이 문제에 적합한 아키텍처 스타일 2~4개를 후보로 도출하고, 각 후보를 §3~§5 기준(응집도/결합도, SOLID 적용 용이성, 변경 유연성, ISO 26262 Part 6 적합성/FFI 실현 가능성)으로 비교한 표를 제시한 뒤, **사용자에게 직접 선택하게 합니다**(`AskUserQuestion` 사용, 없으면 명시적으로 텍스트로 질문). 사용자가 하나를 선택하거나 절충안을 지시한 후에만 §3 이후 상세 설계로 진행합니다.

## 3. 응집도/결합도 & SOLID 원칙 적용

`references/cohesion-coupling-solid.md`의 체크리스트를 적용합니다.
- 각 컴포넌트가 단일 책임을 갖는지(높은 응집력), 컴포넌트 간 의존이 필요한 만큼만 존재하는지(낮은 결합도) 설계 근거와 함께 명시합니다.
- SOLID 5원칙(SRP/OCP/LSP/ISP/DIP) 각각에 대해 이 아키텍처가 어떻게 준수하는지 자체 점검표로 기록합니다.
- 순환 의존(circular dependency)이 없는지 확인합니다.

## 4. 인터페이스 정의 (필수)

`references/interface-design.md`에 따라 **모든** 컴포넌트 간 통신 경로에 대해 인터페이스를 정의합니다. 컴포넌트가 다른 컴포넌트의 내부 구현이나 데이터에 직접 접근하는 설계는 허용하지 않습니다 — 반드시 정의된 인터페이스를 통해서만 상호작용하도록 설계하고, 이를 다이어그램과 인터페이스 명세 표로 함께 제시합니다.

## 5. 변경 유연성 및 ISO 26262 Part 6 / A-SPICE 정합성

`references/iso26262-part6-aspice-mapping.md`를 참고해 다음을 반영합니다.
- 변경이 예상되는 지점(variation point)을 식별하고, 해당 지점이 인터페이스/추상화로 격리되어 있는지 확인합니다.
- 안전 관련 요소는 ASIL 배분/분해, 간섭으로부터의 자유(Freedom From Interference, FFI) 분석, 안전 메커니즘(감시/이중화/오류 감지 등)을 아키텍처에 반영합니다.
- A-SPICE SYS.3/SWE.2 기대 산출물(정적 뷰, 동적 뷰, 자원 사용 추정, 요구사항 배분, 추적성)을 모두 포함합니다.

## 6. 다이어그램

`references/architecture-diagrams.md`의 Mermaid 다이어그램(Component/Block Definition, Interface, Deployment, 동적 뷰용 Sequence)을 사용해 정적 구조와 동적 동작을 함께 표현합니다.

## 7. 컴포넌트 통합 순서 정의

`references/integration-order.md`의 절차에 따라 컴포넌트 의존성 그래프를 만들고, 이를 근거로 통합 순서를 정의합니다. 각 통합 단계에서 필요한 스텁/드라이버와 그 이유를 함께 명시합니다.

## 8. 추적성

설계 요소에 `requirements-analyst` 스킬의 ID 체계(`DES-nnn`)를 부여하고, 동일한 추적성 매트릭스(`traceability/requirements-traceability.csv`)에 `ParentIDs`(연계된 SR/SWR/TSR)를 채워 넣어 양방향 추적을 유지합니다. `requirements-analyst`의 `references/traceability.md` 규칙을 그대로 따릅니다.

## 9. 출력 및 자체 점검

§0에서 확인한 양식(제공되었으면 그 양식, 아니면 기본 양식)으로 문서를 작성하고, 다음을 요약해 보고합니다: 사용자가 선택한 아키텍처 구조, 응집도/결합도 및 SOLID 점검 결과, 모든 컴포넌트 간 통신이 인터페이스를 통해서만 이루어지는지 여부, 안전/A-SPICE 반영 여부, 통합 순서, 추적성 매트릭스 갱신 여부.
