TEMPLATE STATUS: PENDING

> 사용자가 아직 공식 요구사항 템플릿을 제공하지 않았습니다. 아래는 그때까지 사용할 **기본 임시 템플릿**입니다.
> 사용자가 공식 템플릿을 제공하면, 이 파일 전체를 그 내용으로 교체하고 최상단을 `TEMPLATE STATUS: PROVIDED`로 바꾸세요. 그 뒤로는 이 기본 템플릿을 사용하지 않습니다.

## 기본 임시 템플릿

### 기능 요구사항(FR) 항목

| 필드 | 설명 |
|---|---|
| ID | 예: SR-001 (`references/traceability.md`의 ID 체계 참고) |
| 제목 | 한 줄 요약 |
| 설명 | EARS 패턴 기반 서술 (`references/requirement-writing-rules.md`) |
| 출처(상위 요구/이해관계자 니즈) | 상위 요구사항 ID 또는 이해관계자 니즈 참조 |
| 관련 다이어그램 | Use Case / Activity / Sequence / State Machine 중 해당 Mermaid 다이어그램 링크 또는 삽입 |
| 우선순위 | 필수/권고/선택 |
| 안전 관련 여부 | 예/아니오, 예인 경우 ASIL 및 안전목표 ID |
| 검증 기준(Acceptance Criteria) | 측정 가능한 통과/실패 조건 |
| 검증 방법 | 리뷰/분석/테스트/시뮬레이션 중 실행 가능한 구체적 절차 |
| 하위 추적(설계/코드/테스트) | 추적성 매트릭스의 해당 행 참조 |
| 상태 | Draft/Reviewed/Approved/Verified |

### 비기능 요구사항(NFR) 항목

| 필드 | 설명 |
|---|---|
| ID | 예: NFR-001 |
| 제목 | 한 줄 요약 |
| ISO 25010 특성/하위특성 | `references/nfr-iso25010.md` 표 참조 |
| 설명 | EARS 패턴 기반 서술, 측정 가능한 목표치 포함 |
| 목표치(Target Metric) | 정량적 수치와 단위 |
| 검증 방법 | 실행 가능한 구체적 절차(도구/부하 조건/측정 방법/합격 기준) |
| 안전 관련 여부 | 예/아니오, 예인 경우 ASIL |
| 상위/하위 추적 | 추적성 매트릭스 참조 |
| 상태 | Draft/Reviewed/Approved/Verified |

### 문서 공통 헤더

- 문서 ID / 버전 / 작성일 / 작성자 / 승인자
- 변경 이력(버전, 일자, 변경내용, 변경자)
- 용어집(Glossary) 참조 또는 인라인 정의
