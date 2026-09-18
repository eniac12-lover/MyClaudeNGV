# 네이밍 규칙

`CLAUDE.md` "구현 지침": 함수명·변수명은 **3글자 이상**, **camelCase**를 사용합니다.

## 규칙

- 첫 글자는 소문자, 이후 각 단어의 첫 글자만 대문자(camelCase). 예: `calculateRoute`, `sensorValue`, `isValidInput`.
- 전체 길이 3글자 미만 금지: `id`, `n`, `db` 같은 이름은 `itemId`, `count`, `database`처럼 늘립니다.
- 예외: 반복문 인덱스(`i`, `j`, `k`)처럼 스코프가 매우 짧고 관례적으로 통용되는 경우만 허용하되, 남발하지 않습니다. 예외를 쓸 때는 `references/quality-metrics-tools.md`의 pylint `good-names` 설정에 등록합니다.
- 클래스명은 PascalCase(camelCase의 대문자 시작 변형)를 사용합니다(Python 관례와 일치, `CLAUDE.md`에 별도 명시가 없으면 이 관례를 따름) — 함수/변수 camelCase 규칙과 구분됩니다.
- 상수는 프로젝트에 별도 지침이 없으면 `UPPER_SNAKE_CASE`(Python 관례)를 유지할지, camelCase로 통일할지 사용자에게 확인합니다(`CLAUDE.md`가 상수에 대해서는 명시하지 않았으므로 임의로 정하지 않습니다).
- 약어만으로 된 이름(`tmp`, `val`, `obj`)은 피하고 의미를 드러내는 이름을 사용합니다.

## 자동 검증

`references/quality-metrics-tools.md` §4의 pylint 정규식 설정으로 강제합니다. 코드 리뷰/자체 점검 시 `pylint`의 `C0103 invalid-name` 경고가 0건이어야 합니다.
