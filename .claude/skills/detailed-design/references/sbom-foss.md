TEMPLATE STATUS: PROVIDED

> 공식 템플릿: `WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/TPL-SBOM-001_Python 의존성 SBOM FOSS 라이선스 목록 템플릿.xlsx`
>
> ⚠️ 동일한 저작권/이용 제한이 적용됩니다(`references/detailed-design-template.md` 상단 참고).

## 시트 구조

| 시트 | 컬럼 |
|---|---|
| SBOM | Package, Version, Dependency Type, SPDX, Evidence Type, Evidence Locator, Distribution, Remark |
| FOSS Review | Review ID, Scope, Criterion, Evidence, Result, Owner, Date, Limitation |
| Change History | Revision, 변경일, 작성 역할, 변경 내용, 검토 상태, 승인 상태 |

(각 시트 표는 9행이 헤더, 10행부터 데이터 — `WP_Templates/Engineering/README.md` 규칙과 동일)

## 작성 원칙 — 사실만 기록, 추측 금지

- **Package/Version**: 실제 의존성 매니페스트(`requirements.txt`, `pyproject.toml`, `poetry.lock`, `Pipfile.lock` 등)나 패키지 관리자 출력(`pip freeze`, `pip show`)에서 확인한 값만 기록합니다. 프로젝트에 아직 의존성 파일이 없으면 "확인 필요"로 남기고 임의 버전을 채우지 않습니다.
- **Dependency Type**: 직접(Direct) / 전이(Transitive) 구분.
- **SPDX**: 해당 패키지의 실제 라이선스 식별자(예: MIT, Apache-2.0, BSD-3-Clause). 패키지 메타데이터(`pip show <pkg>`의 License 필드, PyPI 페이지)에서 확인합니다. 확인되지 않으면 "확인 필요"로 남깁니다.
- **Evidence Type / Evidence Locator**: 근거 종류(예: "pip show 출력", "PyPI 페이지", "LICENSE 파일")와 실제 위치/경로/URL.
- **Distribution**: 이 패키지가 최종 배포물에 포함되는지(런타임 의존) 여부.
- **Remark**: 특이사항(예: 카피레프트 라이선스로 인한 배포 방식 제약).

## FOSS Review 시트 작성

- **Criterion**: 예) "카피레프트 라이선스(GPL 계열) 포함 시 배포 방식 검토", "상업적 이용 제한 여부", "특허 조항 유무" 등 프로젝트의 실제 FOSS 정책 기준을 기록(정책이 없으면 사용자에게 기준을 확인).
- **Result**: Pass/Fail/조건부(제약 조건 명시).
- **Limitation**: 조건부 통과 시 그 제약사항을 구체적으로 기술(막연히 "주의 필요"라고만 쓰지 않음).

## 절차

1. 프로젝트의 실제 의존성 목록을 `Glob`/`Read`로 확인합니다(`requirements.txt`, `pyproject.toml`, lock 파일 등). 없으면 사용자에게 의존성 목록 제공을 요청하거나, 상세설계 단계에서 아직 확정되지 않았음을 명시합니다.
2. 각 패키지에 대해 SPDX 라이선스를 확인하고 FOSS Review 기준에 따라 평가합니다.
3. `anthropic-skills:xlsx` 스킬 절차로 공식 템플릿을 복사한 사본에 기록합니다.
4. 카피레프트 라이선스나 배포 제약이 있는 패키지가 발견되면, 이를 §13(구현 경계)와 최종 보고서에 반드시 명시합니다.
