"""!
@brief UNIT-006 제어 계층 인터페이스(AIF-015, SWD-001 §4.5).
"""
from abc import ABC, abstractmethod

from childlock.common.dataTypes import CycleResult


class IEvaluationCycleControl(ABC):
    """! @brief AIF-015: 평가주기 실행 계약(합성 루트 중재자)."""

    @abstractmethod
    def runCycle(self) -> CycleResult:
        """!
        @brief 1회 평가주기(입력수집→판정→출력→발행→기록)를 완주한다.
        @return `CycleResult`. 파이프라인 내부 예외는 안전 열화로 흡수되어
        밖으로 전파되지 않는다(SWD-001 §6.6).
        """
