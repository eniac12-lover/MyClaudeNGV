"""!
@brief UNIT-005 인프라 계층 인터페이스(AIF-012/016, SWD-001 §4.5).
"""
from abc import ABC, abstractmethod


class IClockSource(ABC):
    """! @brief AIF-012: 단조 증가 시각 소스 조회 계약."""

    @abstractmethod
    def now(self) -> float:
        """! @brief 현재 시각(초)을 반환한다. 이전 호출값 이상(단조 증가)이어야 한다."""


class IClockControl(ABC):
    """! @brief AIF-016: 테스트 전용 시계 제어 계약(운영 경로 호출 금지, SWD-001 §10)."""

    @abstractmethod
    def setFixed(self, targetSeconds: float) -> None:
        """!
        @brief 고정 시각을 설정한다(테스트 모드 전용).
        @param targetSeconds 설정할 목표 시각(초).
        @throws RuntimeError 테스트 모드가 아니면 발생한다.
        @throws ValueError 단조성을 위반하면(현재값보다 작으면) 발생한다.
        """

    @abstractmethod
    def advance(self, deltaSeconds: float) -> None:
        """!
        @brief 고정 시각을 전진시킨다(테스트 모드 전용).
        @param deltaSeconds 전진시킬 시간(초, 0 이상).
        @throws RuntimeError 테스트 모드가 아니면 발생한다.
        @throws ValueError `deltaSeconds`가 음수면 발생한다.
        """
