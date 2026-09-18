# Doxygen 스타일 주석 작성 가이드 (Python)

Doxygen은 원래 C/C++/Java 관례에서 출발했지만, Python 코드에도 동일한 태그 체계를 적용할 수 있습니다. 아래 두 가지 표기 방식 중 프로젝트에서 하나를 정해 일관되게 사용합니다.

## 방식 A — 독스트링(권장)

```python
def calculateRoute(currentPos, destination):
    """!
    @brief 현재 위치에서 목적지까지의 경로를 계산한다.

    @param currentPos 현재 좌표 (x, y)
    @param destination 목적지 좌표 (x, y)
    @return 경로 좌표 리스트. 경로가 없으면 빈 리스트.
    @throws ValueError currentPos 또는 destination이 유효 범위를 벗어난 경우

    @pre currentPos, destination은 지도 경계 내 좌표여야 한다.
    @post 반환된 경로의 첫 좌표는 currentPos와 같다.
    """
    ...
```

## 방식 B — 라인 주석(`##`)

```python
## @brief 현재 위치에서 목적지까지의 경로를 계산한다.
# @param currentPos 현재 좌표 (x, y)
# @param destination 목적지 좌표 (x, y)
# @return 경로 좌표 리스트. 경로가 없으면 빈 리스트.
def calculateRoute(currentPos, destination):
    ...
```

## 필수 태그

| 태그 | 용도 | 생략 가능 조건 |
|---|---|---|
| `@brief` | 함수/클래스의 한 줄 요약 | 없음(항상 작성) |
| `@param` | 각 파라미터 설명 | 파라미터가 없으면 생략 |
| `@return` | 반환값 설명 | 반환값이 없으면(`None` 고정) 생략 |
| `@throws` | 발생 가능한 예외 | 예외를 던지지 않으면 생략 |
| `@pre` / `@post` | 사전조건/사후조건 | `detailed-design` 함수 계약에 정의되어 있으면 반드시 옮겨 적음 |

## 원칙

- 주석은 `detailed-design`의 함수 계약(`references/function-contracts-and-algorithms.md`)과 **일치**해야 합니다 — 계약에 없는 내용을 지어내거나, 계약과 다른 내용을 쓰지 않습니다.
- 코드를 그대로 번역한 주석("i를 1 증가시킨다" 같은)은 금지합니다 — 왜(why)와 계약을 설명합니다.
- 주석 비율 20% 기준을 채우기 위해 의미 없는 주석을 채워 넣지 않습니다. 실제로는 계약을 충실히 옮기면 자연스럽게 기준을 충족하는 경우가 많습니다 — 비율을 억지로 맞추는 것이 목적이 아니라 계약을 명확히 문서화하는 것이 목적입니다.
- 비율 계산 방법은 `references/quality-metrics-tools.md` §3을 따릅니다.
