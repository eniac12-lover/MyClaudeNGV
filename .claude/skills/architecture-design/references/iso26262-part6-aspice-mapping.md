# ISO 26262 Part 6 / A-SPICE 아키텍처 설계 정합성 가이드

> 아래는 공개적으로 통용되는 ISO 26262 Part 6(소프트웨어 수준 설계) 및 A-SPICE SYS.3/SWE.2 아키텍처 설계 관련 핵심 개념 요약입니다. 정확한 조항 번호/문구는 표준 원문 및 프로젝트 Safety Plan과 대조하세요.

## ISO 26262 Part 6 핵심 개념

| 개념 | 설계 반영 사항 |
|---|---|
| ASIL 배분(Allocation) | 상위 요구(FSR/TSR)의 ASIL을 아키텍처 요소에 배분. 요소별 ASIL을 아키텍처 문서에 명시 |
| ASIL 분해(Decomposition) | 하나의 안전요구를 여러 요소로 분해해 각기 다른(낮은) ASIL을 배정할 경우, 분해 규칙(예: ASIL D → ASIL(B,B) 등)과 요소 간 충분한 독립성 근거 필요 |
| 간섭으로부터의 자유(Freedom From Interference, FFI) | 서로 다른 ASIL(또는 QM)을 가진 요소가 공존할 때, 낮은 ASIL/QM 요소의 고장이 높은 ASIL 요소에 영향을 주지 않도록 공간적/시간적 분리, 통신 간섭 방지, 자원(메모리/CPU) 간섭 방지를 설계에 반영. FFI가 입증 안 되면 전체를 가장 높은 ASIL로 취급해야 함 |
| 안전 메커니즘(Safety Mechanism) | 오류 감지(모니터링, 워치독, 플러시빌리티 체크 등), 오류 처리(안전 상태 전이, 이중화, 페일세이프/페일오퍼레이셔널) 요소를 아키텍처에 명시적으로 포함 |
| 소프트웨어 아키텍처 설계 원칙(Part 6 표 기반 권고, ASIL별 강도 상이) | 모듈성, 캡슐화, 낮은 복잡도, 계층적 구조, 적절한 수준의 세분화 등 — 이 스킬의 §3(응집도/결합도/SOLID)이 이를 지원 |
| 검증(Verification of Architecture) | 아키텍처가 요구사항을 모두 충족하는지, 내부 일관성/실현가능성이 있는지 리뷰·분석으로 확인 |

## FFI 분석 시 확인할 것

- [ ] 서로 다른 ASIL 요소가 같은 하드웨어 자원(CPU 코어, 메모리 영역, 통신 버스)을 공유하는가? 공유한다면 시간/공간 파티셔닝 메커니즘이 있는가?
- [ ] 낮은 ASIL 요소가 높은 ASIL 요소의 입력(인터페이스)에 영향을 줄 수 있는가? 있다면 입력 검증/범위 체크 등 안전 메커니즘이 인터페이스 명세(`references/interface-design.md`)에 반영되어 있는가?
- [ ] 간섭 가능성이 입증되지 않으면, 관련 요소 전체를 더 높은 ASIL로 취급했는가?

## A-SPICE SYS.3 (시스템 아키텍처 설계) / SWE.2 (소프트웨어 아키텍처 설계) 기대 산출물

| 산출물 관점 | 이 스킬의 대응 절차 |
|---|---|
| 정적 뷰(구조) | §3 응집도/결합도, `references/architecture-diagrams.md`의 Component/Block Diagram |
| 동적 뷰(상호작용) | `references/architecture-diagrams.md`의 Sequence/State 다이어그램 |
| 인터페이스 정의 | §4, `references/interface-design.md` |
| 자원 사용 추정 | 기본 양식 §8 (컴포넌트별 CPU/메모리/대역폭 추정) |
| 요구사항 배분 | 기본 양식 §8, 추적성 매트릭스 |
| 추적성(요구사항 ↔ 아키텍처) | §8, `requirements-analyst`의 `traceability.md` 규칙 재사용 |
| 통합 전략 근거 제공 | §7 통합 순서 (`references/integration-order.md`) — 실제 SYS.4/SWE.5 통합 테스트 전략의 입력이 됨 |

이 스킬로 작성한 아키텍처가 A-SPICE CL2 감사 대상이 되는 경우, `aspice-auditor` 스킬/`aspice-cl2-auditor` 서브 에이전트로 점검할 수 있습니다.
