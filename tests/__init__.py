"""!
@brief 테스트 최상위 패키지 초기화.

@details `src` 레이아웃(패키지 미설치)에서 `python -m unittest discover`가
정상적으로 `childlock` 패키지를 임포트할 수 있도록 `src` 디렉터리를
`sys.path`에 등록한다. 이 파일은 discover가 `tests` 패키지를 순회할 때
1회 임포트되므로, 이후 모든 하위 테스트 모듈에서 별도 경로 설정 없이
`import childlock...`을 사용할 수 있다.
"""
import pathlib
import sys

repoRoot = pathlib.Path(__file__).resolve().parent.parent
srcDir = repoRoot / "src"
if str(srcDir) not in sys.path:
    sys.path.insert(0, str(srcDir))
