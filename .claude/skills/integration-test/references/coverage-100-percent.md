# 함수 커버리지 / Call 커버리지 100% 측정 절차

ISO 26262 Part 6은 소프트웨어 통합시험의 구조적 커버리지 지표로 **함수 커버리지(Function Coverage)**와 **Call 커버리지(Call Coverage)**를 사용합니다(단위시험 수준의 구문/분기/MC-DC 커버리지와 구분됩니다). 이 프로젝트는 두 지표 모두 **100%**를 목표로 합니다.

> 커버리지는 **통합시험 스위트 실행만으로** 측정합니다(`tdd` 스킬의 단위 테스트가 아니라, 이 스킬이 만든 통합시험 케이스를 실행한 결과). 단위 테스트로 이미 커버된 줄이 있어도, 통합시험 자체가 그 함수/호출을 실행하지 않으면 이 지표는 충족되지 않습니다.

## 정의

- **함수 커버리지**: 통합 대상 컴포넌트의 전체 함수 중, 통합시험 실행 중 최소 1줄 이상 실행된 함수의 비율.
- **Call 커버리지**: 아키텍처/상세설계에서 정의된 컴포넌트·함수 간 호출 관계(엣지) 중, 통합시험 실행 중 실제로 발생한 호출의 비율.

오픈소스 도구(`coverage.py`, Python 표준 라이브러리 `ast`/`sys.settrace`)로 측정합니다. `pip install coverage`가 필요하면 설치합니다(이 환경에 `python`/`pip`이 없을 수 있으니 먼저 확인하세요).

## 1. 함수 커버리지 측정

1. `coverage.py`로 통합시험 스위트만 실행합니다.
   ```
   coverage run -m unittest discover -s <통합시험 디렉토리> -p "test_*.py"
   coverage json -o coverage.json
   ```
2. 대상 소스 파일들을 Python 표준 라이브러리 `ast` 모듈로 파싱해 모든 함수 정의의 라인 범위를 추출하는 스크립트를 작성해 실행합니다(예: `scripts/list_functions.py`).
   ```python
   import ast, json, sys

   def listFunctions(filePath):
       with open(filePath, encoding="utf-8") as f:
           tree = ast.parse(f.read(), filename=filePath)
       functions = []
       for node in ast.walk(tree):
           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
               endLine = getattr(node, "end_lineno", node.lineno)
               functions.append({"name": node.name, "start": node.lineno, "end": endLine})
       return functions
   ```
3. `coverage.json`의 파일별 `executed_lines`와 §1-2에서 뽑은 함수별 라인 범위를 대조해, 각 함수가 실행된 줄을 하나라도 포함하는지 판정합니다.
4. 함수 커버리지 = (실행된 함수 수) / (전체 함수 수) × 100. 100% 미만이면 커버되지 않은 함수 목록을 보고하고, §7(케이스 작성)으로 돌아가 해당 함수를 실행하는 케이스를 추가합니다.

## 2. Call 커버리지 측정

1. **기대 호출 엣지 목록** 작성: `architecture-design`의 인터페이스 명세(컴포넌트 간 호출)와 `detailed-design` §3(상세 호출관계)의 함수 간 호출관계를 근거로 `(호출자 함수, 피호출 함수)` 쌍의 목록을 만듭니다(예: `expected_call_edges.json`).
2. **실제 호출 엣지 추적**: Python 표준 라이브러리 `sys.settrace`로 통합시험 실행 중 발생한 함수 호출을 기록하는 스크립트를 작성해 실행합니다.
   ```python
   import sys, json, unittest

   calledEdges = set()

   def traceCalls(frame, event, arg):
       if event == "call":
           calleeName = frame.f_code.co_name
           callerFrame = frame.f_back
           callerName = callerFrame.f_code.co_name if callerFrame else "<entry>"
           calledEdges.add((callerName, calleeName))
       return traceCalls

   sys.settrace(traceCalls)
   suite = unittest.defaultTestLoader.discover("<통합시험 디렉토리>", pattern="test_*.py")
   unittest.TextTestRunner(verbosity=2).run(suite)
   sys.settrace(None)

   with open("actual_call_edges.json", "w", encoding="utf-8") as f:
       json.dump(sorted(list(edge) for edge in calledEdges), f, ensure_ascii=False, indent=2)
   ```
3. `expected_call_edges.json`과 `actual_call_edges.json`을 대조합니다. Call 커버리지 = (실제 발생한 기대 엣지 수) / (기대 엣지 총수) × 100.
4. 100% 미만이면 커버되지 않은 호출 엣지를 보고하고, §7(케이스 작성)으로 돌아가 그 호출 경로를 실행하는 케이스를 추가합니다.

## 3. 100%에 도달하지 못할 때

- **도달 불가능한(죽은) 코드**가 원인이면: 그 코드를 제거할지, 왜 남겨두는지(예: 향후 확장을 위한 자리표시자 — 이 프로젝트 원칙상 지양) 사용자에게 확인합니다. 임의로 커버리지 모수에서 제외해 100%를 "인위적으로" 맞추지 않습니다.
- **방어적 코드(defensive code, 이론상 도달 불가능하지만 안전을 위해 남긴 코드)**가 원인이면: 결함 주입 시험(`references/iso26262-integration-methods.md`)으로 그 경로를 강제로 트리거하는 케이스를 추가합니다. 그래도 도달이 불가능하면(예: 하드웨어 없이는 트리거 불가) 그 사유와 대안 검증 방법(리뷰/분석)을 문서 §5(진입/종료 기준) 예외로 기록하고 사용자 승인을 받습니다 — 조용히 100% 미만으로 넘어가지 않습니다.

## 4. 결과 기록

측정 결과(함수 커버리지 %, Call 커버리지 %, 미달 시 목록과 조치)를 `references/integration-test-template.md`의 TPL-SWE5-003 `Integration Results`의 `Evidence Locator`에 리포트 파일 경로로 남기고, `Run Summary` 시트에도 커버리지 달성 여부를 기록합니다.
