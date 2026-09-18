# 품질 지표 측정 — 오픈소스 도구 사용법

`CLAUDE.md` "구현 지침"이 요구하는 5개 지표를 아래 오픈소스 도구로 측정합니다. 프로젝트에 아직 설치되어 있지 않으면 `pip install lizard pylint radon`으로 설치합니다(이미 설치돼 있으면 재설치하지 않습니다).

> 이 환경에 `python`/`pip`이 정상 설치되어 있지 않을 수 있습니다. 실행 전 `python --version`으로 확인하고, 없으면 사용자에게 Python 3.14 설치 여부를 확인하세요 — 임의로 다른 언어/도구로 대체하지 않습니다.

## 1. 함수 순수코드라인(NLOC) ≤ 50, 순환복잡도(CCN) ≤ 10 — `lizard`

```
lizard <대상 경로> -l python -C 10 -L 50
```

- 출력의 각 행이 함수 하나이며 `NLOC`(주석/공백 제외 순수 코드 라인수)와 `CCN`(순환복잡도) 컬럼을 보여줍니다.
- `-C 10 -L 50` 임계값을 넘는 함수는 경고로 표시됩니다(도구 버전에 따라 표시 방식이 다를 수 있으니, 표시되지 않으면 출력의 NLOC/CCN 값을 직접 임계값과 비교해 판정하세요).
- 임계값을 넘는 함수는 더 작은 함수로 분리(추출)하거나 분기를 줄여 리팩터링합니다.

## 2. 중복 코드 7줄까지 허용 (8줄 이상 금지) — `pylint`

프로젝트 루트의 `.pylintrc`에 이미 이 설정이 있습니다(직접 새로 만들지 마세요, CI(`​.github/workflows/ci.yml`)도 이 파일을 그대로 사용합니다).

```ini
[SIMILARITIES]
min-similarity-lines=8
ignore-comments=yes
ignore-docstrings=yes
ignore-imports=yes
```

```
pylint <대상 경로>
```

- `min-similarity-lines=8`로 설정하면 **8줄 이상** 중복 블록만 `R0801 duplicate-code`로 보고됩니다 — 즉 7줄까지는 허용 기준과 일치합니다.
- `R0801`이 보고되면 공통 로직을 함수/모듈로 추출해 중복을 제거합니다.

## 3. Doxygen 주석 비율 ≥ 20% — `radon raw`

```
radon raw -s <파일>
```

출력 예시 필드: `LOC`, `LLOC`, `SLOC`, `Comments`, `Multi`(멀티라인 문자열/독스트링), `Blank`.

- Doxygen 스타일 주석을 `#`으로 시작하는 라인 주석(`##`)으로 쓰면 `Comments`에 집계되고, 삼중따옴표 독스트링(`"""! ... """`)으로 쓰면 `Multi`에 집계됩니다. 어느 방식이든 됩니다(`references/doxygen-comments.md` 참고).
- 주석 비율 = `(Comments + Multi) / LOC`. 이 값이 0.20 미만이면 함수/클래스에 Doxygen 주석을 보강합니다(의미 없는 채우기용 주석 금지 — 실제 계약/근거를 기술).

## 4. 네이밍 규칙(3글자 이상, camelCase) — `pylint`

프로젝트 루트의 `.pylintrc`에 이미 이 설정이 있습니다(최소 3글자를 강제하기 위해 `naming-style` 대신 정규식을 직접 지정한 것입니다 — 새로 만들지 마세요).

```ini
[BASIC]
function-rgx=^[a-z][a-zA-Z0-9]{2,}$
variable-rgx=^[a-z][a-zA-Z0-9]{2,}$
argument-rgx=^[a-z][a-zA-Z0-9]{2,}$
attr-rgx=^[a-z][a-zA-Z0-9]{2,}$
method-rgx=^[a-z][a-zA-Z0-9]{2,}$
```

- 이 정규식은 소문자로 시작하고(camelCase) 전체 길이가 3자 이상(`[a-z]` 1자 + `[a-zA-Z0-9]{2,}` 2자 이상)인 이름만 허용합니다.
- 반복문 카운터처럼 관용적으로 짧은 이름(`i`, `j`)이 필요하면 `good-names` 옵션에 예외로 등록하고, 왜 예외인지 주석/보고서에 근거를 남깁니다. 예외를 남발하지 않습니다.
- `pylint <대상 경로>` 실행 시 `C0103 invalid-name`으로 위반이 보고됩니다.

## 게이트 통과 기준

위 4개 명령(`lizard`, `pylint` 중복, `radon raw` 비율 계산, `pylint` 네이밍) 결과가 모두 기준을 만족해야 해당 구현 단위를 "완료"로 표시합니다. 하나라도 위반이면 `tdd` 스킬의 Refactor 단계로 돌아갑니다.

이 게이트는 로컬에서 직접 실행해 확인하는 것이 원칙이지만, PR을 올리면 `.github/workflows/ci.yml`이 동일한 도구(lizard/pylint, 그리고 branch coverage 100%)로 다시 검증합니다 — CI 실패를 로컬 확인 없이 PR로 넘기지 않습니다(`.github/BRANCH_POLICY.md` 참고).
