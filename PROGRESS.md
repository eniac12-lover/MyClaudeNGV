# 진행 현황 (세션 인수인계용)

> 이 파일은 다른 세션/작업자가 이어서 작업할 수 있도록 현재 상태를 기록한 것이다.
> 작업이 이어질 때마다 갱신하고, 완전히 다음 Phase로 넘어가면 이 파일 내용은 커밋 이력/PR로
> 대체되므로 삭제해도 된다.

## 전체 계획 요약

`OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx`(가상 OEM-A, 전자식 차일드락 제어 SW,
후석 좌/우, ASIL B 안전요구 + QM 기능요구, PC/SIL·Web 검증, 교육용 가상 프로젝트)를
A-SPICE 생명주기(분석→설계→구현→테스트)로 3개 Phase에 걸쳐 증분 개발한다.

- **Phase 1**(진행 중, 브랜치 `feature/phase1-core-input-lock`): 입력처리·기본 잠금/해제
  — OEM-IF-001~009, OEM-SR-003, OEM-FR-001/002/007, OEM-NFR-001/002
- **Phase 2**(미착수): 안전 우선순위(ASIL B) — OEM-SR-001/002/004, OEM-FR-003/005/006
- **Phase 3**(미착수): 상태표시·전체 통합 — OEM-FR-004, OEM-IF-006 조회/직렬화

각 Phase는 분석(SWE.1)→설계(SWE.2, 아키텍처는 Phase1에서 전체 범위 1회 설계)→상세설계
(SWE.3)→구현(coding/TDD)→통합시험(SWE.5)→시스템시험(SWE.6)을 모두 거치고, **Phase 완료 후
PR 1개로 사용자 리뷰 → 승인 시 `main`에 병합**한다(Phase 내 서브 단계별 리뷰는 하지 않음).

문서 산출물은 지금 `.md`로 작성 중이며, **Phase 종료 시 공식 docx/xlsx 템플릿
(`WP_Templates/`)로 변환**하기로 확정되어 있다(아직 미수행).

## 저장 구조

```
WorkProducts/
  01_Requirements/     # SWE.1 — 누적 문서(Phase마다 개정)
  02_Architecture/      # SWE.2 — Phase1에서 전체 범위 1회 설계, 이후 개정
  Traceability/          # OEM↔SWR↔DES↔UNIT↔Code 누적 추적성 매트릭스
  Phase1_CoreInputLock/03_DetailedDesign/   # SWE.3 (Phase별)
  Phase2_SafetyPriority/                     # (미생성)
  Phase3_StatusIntegration/                  # (미생성)
src/childlock/          # 구현 소스 (Phase1부터 시작)
tests/childlock/        # unittest (TDD)
```

## Phase 1 진행 상태 (2026-09-18 기준)

| 단계 | 상태 | 산출물 |
|---|---|---|
| SWE.1 요구사항 분석 | ✅ 완료, 커밋됨 | `WorkProducts/01_Requirements/SWR-001_*.md`, `UC-001_*.md`, `WorkProducts/Traceability/TRC-001_*.md` |
| SWE.2 아키텍처 설계(전체 범위) | ✅ 완료, 커밋됨 | `WorkProducts/02_Architecture/SWA-001_*.md` (Rev 1.1) |
| SWE.3 상세설계(Phase1 범위) | ✅ 완료, 커밋됨 | `WorkProducts/Phase1_CoreInputLock/03_DetailedDesign/SWD-001_*.md`, `SBOM-001_*.md` |
| 구현(coding/TDD) | 🔄 **부분 완료 (UNIT-001~011, 013, 014 / 총 26개 중 13개)** | `src/childlock/`, `tests/childlock/` — 아래 "다음 작업" 참고 |
| 통합시험(SWE.5) | ⏳ 미착수 | — |
| 시스템시험(SWE.6) | ⏳ 미착수 | — |
| Phase1 PR 생성/리뷰 | ⏳ 미착수 | — |

### 구현 완료분 (88/88 테스트 통과, pylint 10.00/10, lizard 경고 0건, 주석비율 21~47%)

UNIT-001(공통 DTO), UNIT-002~006(인터페이스 5종), UNIT-007(VehicleSignalGateway),
UNIT-008(DriverCommandGateway), UNIT-009(InputValidityMonitor, ASIL B),
UNIT-010(DeterministicClock), UNIT-011(OutputStateRepository),
UNIT-013(IgnitionOffRule), UNIT-014(AutoLockRule)

### 다음 작업 (미착수 UNIT, `SWD-001` 참고)

권장 순서: UNIT-015(DriverCommandRule) → UNIT-016(HoldLastOutputRule) →
UNIT-022~026(Phase2 스텁 5종, 항상 `None` 반환이라 간단함) → UNIT-012(RulePriorityRegistry) →
UNIT-017(ArbitrationOrchestrator) → UNIT-018~020(출력 계층: ActuatorOutputAdapter,
StateReasonComposer, EventHistoryStore) → UNIT-021(EvaluationCycleController) →
`src/childlock/app/compositionRoot.py`(합성 루트) → **branch coverage 100% 확인**
(`coverage run --branch -m unittest discover -s . -p "test_*.py" && coverage report -m --fail-under=100`,
아직 미측정) → `TRC-001`의 Code 열 최종 검증.

구현은 `coding` 서브에이전트(`Skill: coding` → `Skill: tdd`)에 위임해 이어가면 된다. 입력
문서는 `SWD-001_SW상세설계서.md`(§2.3 UNIT 표, 함수 계약, 알고리즘, 결정표, 상태전이)를
그대로 따르면 된다.

## 확인이 필요한 미해결 사항 (사용자 검토 요망, 급하지 않음)

1. **`.pylintrc` 확장 검토**: 구현 중 `init-hook`(src를 sys.path에 추가), `method-rgx`/
   `module-rgx`(던더 메서드·`test_` 접두어 허용), `disable=too-few-public-methods,
   missing-class-docstring,missing-function-docstring`을 추가했다. 근거는 파일 내 주석에
   기록되어 있으며 CLAUDE.md의 5개 공식 품질지표(라인수/복잡도/중복/주석비율/네이밍)에는
   영향 없음. CI(`ci.yml`)가 이 설정 없이는 항상 실패하므로 반영은 필요했으나, 정책 검토 요망.
2. **문서 부채**: `SWA-001`(§4.3 reasonCode 소스, §8.1 신호수 9→12, §4.2 인터페이스
   시그니처)에 상세설계 단계에서 발견된 불일치 3건이 있고, 사용자 승인을 거쳐 상세설계
   버전을 신뢰하기로 확정했다. `SWA-001` 본문 정정은 Phase 종료 시 공식 docx 변환과 함께
   일괄 반영 예정(아직 미수행).
3. **경계선 해석**: `DriverCommandGateway.submit()`의 payload 필드 매핑(`side/action/source/
   timestamp_s` 직접 매핑)이 SWR-001 §5의 "VehicleSnapshot.timestamp_s 사용" 문구를
   개념적 설명으로 해석한 결과다 — 구현 세부사항 수준의 판단이라 진행했으나 필요시 재확인.
4. Phase1~3 전체에 걸쳐 이미 알려진 "확인 필요" 항목(Phase2 규칙 간 상대 우선순위 잠정안,
   ASIL B 논리적 FFI의 표준 원문 정합성, OEM-IF-006 reason_code의 side별 세분화 여부,
   `RawVehicleSnapshot` 단일 타임스탬프 한계)은 `SWA-001` §12, `SWD-001` §16에 그대로
   등재되어 있으며 Phase2 착수 전 재확인 예정.

## 재개 방법

1. 이 파일과 `WorkProducts/`, `src/`, `tests/`의 최신 상태를 확인한다.
2. `feature/phase1-core-input-lock` 브랜치에서 계속 작업한다(다른 브랜치로 전환하지 말 것).
3. 구현을 마저 진행하려면 `coding` 서브에이전트에 위 "다음 작업" 섹션을 그대로 지시하면 된다.
4. 구현 완료 후: 통합시험(`integration-tester` 서브에이전트, SWE.5) → 시스템시험
   (`sw-system-tester` 서브에이전트, SWE.6) → 문서(.md → 공식 docx/xlsx) 최종 변환 →
   Phase1 PR 생성 → 사용자 리뷰/승인 → `main` 병합.
