# 양방향 추적성(Bidirectional Traceability) 관리 방안

## 1. 요구사항 ID 체계

| 접두어 | 의미 | 상위 출처 |
|---|---|---|
| STR-nnn | Stakeholder Requirement (이해관계자 요구, SYS.1) | 이해관계자 니즈/규정 |
| SG-nnn | Safety Goal (ISO 26262 HARA 산출물) | HARA |
| SR-nnn | System Requirement (SYS.2, 기능) | STR |
| NFR-nnn | System-level 비기능 요구사항 | STR 또는 품질 목표 |
| FSR-nnn | Functional Safety Requirement | SG |
| TSR-nnn | Technical Safety Requirement | FSR |
| SWR-nnn | Software Requirement (SWE.1) | SR / TSR |
| DES-nnn | 설계 요소 ID (SWE.2/SWE.3 산출물, 이 스킬 범위 밖이지만 추적 대상) | SWR |
| TC-nnn | 테스트 케이스 ID (SWE.4~SWE.6 산출물, 이 스킬 범위 밖이지만 추적 대상) | SWR/SR |

`nnn`은 3자리 이상 zero-padded 일련번호(예: SR-001). 삭제된 ID는 재사용하지 않고 "Obsolete" 상태로만 표시합니다.

## 2. 추적성 매트릭스 형식

기본 위치: `traceability/requirements-traceability.csv` (프로젝트가 다른 경로를 지정하면 그에 따름). 컬럼:

```
ID,Type,Title,ParentIDs,ChildIDs,ASIL,VerificationMethod,VerificationStatus,Status
SR-001,Functional,"...",STR-001,"SWR-001;SWR-002",QM,Test,Not Verified,Approved
```

- `ParentIDs` / `ChildIDs`: 세미콜론으로 구분된 다중 ID. 이 두 컬럼이 있어야 **양방향** 추적이 가능합니다(상위→하위는 ChildIDs, 하위→상위는 ParentIDs로 상호 검증).
- `VerificationStatus`: Not Verified / Passed / Failed.

## 3. 유지 절차 (요구사항 작성/수정 시마다 수행)

1. 새 요구사항 작성 시 §1 체계에 따라 ID를 부여하고, 매트릭스에 행을 추가합니다.
2. 상위 요구사항(ParentIDs)을 지정한 경우, 해당 상위 요구사항 행의 `ChildIDs`에도 이 ID를 추가합니다(양방향 동기화).
3. 요구사항을 삭제/폐기할 때는 매트릭스에서 즉시 삭제하지 않고 `Status`를 `Obsolete`로 변경하고, 연결된 Parent/Child 쪽의 참조도 정리합니다.
4. 정기 점검(또는 요청 시):
   - **고아 요구사항(Orphan)**: `ParentIDs`가 비어 있는데 상위 출처가 있어야 하는 타입(SR/NFR/FSR/TSR/SWR)인 행을 찾아 보고합니다.
   - **미검증 요구사항**: `VerificationStatus`가 `Not Verified`인 항목을 집계해 보고합니다.
   - **끊어진 링크**: 매트릭스에 존재하지 않는 ID를 Parent/ChildIDs가 참조하는 경우를 찾아 보고합니다.
5. 위 점검은 `Grep`/`Read`로 CSV를 파싱해 수행하고, 발견된 문제는 요구사항 산출물과 함께 사용자에게 보고합니다.

## 4. 외부 요구사항 관리 도구로 전환 시

DOORS, Jama, Polarion 등 외부 도구를 사용하게 되면, 이 매트릭스는 해당 도구로 이관하고 이 파일은 ID 체계/관계 정의(§1) 기준 문서로만 유지합니다.
