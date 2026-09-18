# 양방향 추적성(Bidirectional Traceability) 관리 방안

> **공식 산출물**: `WP_Templates/Engineering/Traceability/TPL-TRC-001_양방향 요구사항 추적 매트릭스 템플릿.xlsx` (TEMPLATE STATUS: PROVIDED). 이 파일이 프로젝트의 유일한 추적성 매트릭스입니다. `requirements-analyst`, `architecture-design`, `detailed-design` 등 어떤 스킬로 작업하든 항상 이 파일을 갱신하고, 별도의 CSV나 자체 매트릭스를 새로 만들지 않습니다.
>
> 실제 산출물 사본은 프로젝트 규칙(`WP_Templates/Engineering/README.md`, `WP_Templates/PRC-TPL-001_표준 산출물 양식 등록부.xlsx`)에 따라 `<산출물 ID>_<산출물명>.xlsx` 형식으로 복사해 사용하고, 원본 템플릿 파일 자체는 수정하지 않습니다.

## 0. 공식 매트릭스 구조

시트 "Bidirectional Trace"에 엑셀 표(Table) `TPLTRC001BidirectionalTraceTable`가 있으며, 9행이 헤더, **10행부터 실제 데이터**를 추가합니다(빈 행 유지 규칙, `WP_Templates/Engineering/README.md` 참고). 컬럼은 다음과 같습니다.

| 컬럼 | 의미 |
|---|---|
| Upper Req | 상위 요구사항 ID (STR/SG 등) |
| SW Req | 소프트웨어 요구사항 ID (SR/SWR/NFR/FSR/TSR) |
| Architecture | 아키텍처 설계 요소 ID (DES-nnn) |
| Detailed Design | 상세설계 단위 ID (UNIT-nnn, `detailed-design` 스킬 참고) |
| Code | 실제 소스 파일/함수 경로 또는 식별자 |
| SWE.4 | 단위검증(테스트) ID |
| SWE.5 | 통합시험 ID |
| SWE.6 | 검증시험(Qualification Test) ID |
| Coverage | 이 체인의 검증 커버리지 상태(예: 통과/실패/미검증, 또는 비율) |

한 행은 하나의 요구사항에서 시작하는 추적 체인을 나타냅니다. 여러 하위 요소가 걸리면(예: 하나의 SW Req가 여러 Detailed Design 단위로 분해) 셀 안에 쉼표로 여러 ID를 나열하거나, 필요 시 행을 나누어 각 조합을 별도로 기록합니다 — 프로젝트에서 일관된 방식 하나를 정해 계속 사용하세요.

## 편집 방법

이 파일은 `.xlsx`이므로 `anthropic-skills:xlsx` 스킬의 규칙(엑셀 표 구조 유지, `openpyxl`로 기존 서식/표 범위 존중, 편집 후 `recalc.py`로 수식 재계산)을 따라 편집합니다. 표 범위(`ref="A9:I10"` 등)를 넘어서는 새 행을 추가할 때는 표 정의(`x:table ref`)도 함께 확장해야 정상적인 엑셀 표로 인식됩니다.

## 1. 요구사항/설계 ID 체계

매트릭스 컬럼 자체는 ID 체계를 강제하지 않으므로, 각 셀에 넣는 값은 아래 접두어 체계를 따릅니다.

| 접두어 | 의미 | 상위 출처 |
|---|---|---|
| STR-nnn | Stakeholder Requirement (이해관계자 요구, SYS.1) | 이해관계자 니즈/규정 |
| SG-nnn | Safety Goal (ISO 26262 HARA 산출물) | HARA |
| SR-nnn | System Requirement (SYS.2, 기능) | STR |
| NFR-nnn | System-level 비기능 요구사항 | STR 또는 품질 목표 |
| FSR-nnn | Functional Safety Requirement | SG |
| TSR-nnn | Technical Safety Requirement | FSR |
| SWR-nnn | Software Requirement (SWE.1) | SR / TSR |
| DES-nnn | 아키텍처 설계 요소 ID (SWE.2 산출물) | SWR/TSR |
| UNIT-nnn | 상세설계 구현 단위 ID (SWE.3 산출물) | DES-nnn |
| TC-nnn | 테스트 케이스 ID (SWE.4~SWE.6 산출물) | UNIT/SWR |

`nnn`은 3자리 이상 zero-padded 일련번호(예: SR-001). 삭제된 ID는 재사용하지 않고, 매트릭스 행에 "Obsolete"로 표시만 하고 유지합니다(행 자체를 삭제하지 않음 — 이력 보존).

## 2. 유지 절차 (요구사항/설계/구현 산출물 작성·수정 시마다 수행)

1. 새 요구사항을 작성하면(주로 SW Req 단계) §1 체계로 ID를 부여하고, §0 매트릭스에 새 행을 추가한 뒤 `Upper Req`/`SW Req` 컬럼을 채웁니다.
2. 이후 단계(아키텍처/상세설계/코드/각 테스트 단계) 산출물이 생기면, 그 산출물을 만든 스킬(`architecture-design`, `detailed-design` 등)이 **새 행을 추가하지 않고 해당 요구사항의 기존 행을 찾아 대응 컬럼을 채웁니다**. 대응 행을 찾을 수 없으면(즉, 상위 요구사항이 매트릭스에 없으면) 고아 산출물이므로 사용자에게 보고합니다.
3. 여러 하위 요소가 걸리는 경우 쉼표로 나열하거나 행을 나눕니다(§0 참고) — 한 프로젝트 내에서는 하나의 방식으로 통일합니다.
4. 정기 점검(또는 요청 시) `Read`로 시트를 열어 아래를 확인하고 보고합니다.
   - **빈 다운스트림 컬럼**: `SW Req`는 있는데 그 이후 단계(Architecture/Detailed Design/Code/SWE.4~6)가 계속 비어 있는 행 — 진행이 멈춘 요구사항일 수 있습니다.
   - **Coverage 미기재/미검증** 행 집계.
   - 상위 산출물(`architecture-design` 등)이 참조하는 ID가 매트릭스 어디에도 없는 경우(끊어진 링크).
5. 매트릭스는 `.xlsx` 표이므로, 갱신 시 `anthropic-skills:xlsx` 스킬 규칙(표 범위 확장, 서식 유지, `recalc.py` 재계산)을 따릅니다.

## 3. 외부 요구사항 관리 도구로 전환 시

DOORS, Jama, Polarion 등 외부 도구를 사용하게 되면, 이 매트릭스는 해당 도구로 이관하고 이 파일은 ID 체계/관계 정의(§1) 기준 문서로만 유지합니다.
