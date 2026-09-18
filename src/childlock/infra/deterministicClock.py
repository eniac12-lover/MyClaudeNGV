"""!
@brief UNIT-010 `DeterministicClock`(DES-004, ASIL B 수준 개발, SWD-001 §5.4).
"""
import time

from childlock.interfaces.infraInterfaces import IClockControl, IClockSource


class DeterministicClock(IClockSource, IClockControl):
    """!
    @brief 단조 증가 시각 소스. 테스트 모드에서만 고정/전진을 허용한다(AIF-012/016).

    @details ASIL B 수준 개발 대상이므로 분기 없는 단순 로직(CCN 목표 ≤3)을 유지한다.
    """

    def __init__(self, testModeEnabled: bool = False, fixedTimeSeconds: float = 0.0):
        """!
        @brief 시계를 초기화한다.
        @param testModeEnabled True면 `fixedTimeSeconds`를 반환, False면 실제 단조 시계 사용.
        @param fixedTimeSeconds 테스트 모드 초기 고정 시각(초).
        """
        self.testModeEnabled = testModeEnabled
        self.fixedTimeSeconds = fixedTimeSeconds

    def now(self) -> float:
        """!
        @brief 현재 시각을 반환한다.
        @return 테스트 모드면 `fixedTimeSeconds`, 아니면 `time.monotonic()`.
        두 경우 모두 이전 호출값 이상(단조 증가)이다.
        """
        if self.testModeEnabled:
            return self.fixedTimeSeconds
        return time.monotonic()

    def setFixed(self, targetSeconds: float) -> None:
        """!
        @brief 고정 시각을 설정한다(테스트 모드 전용, 단조성 위반 시 거부).
        @param targetSeconds 설정할 목표 시각(초).
        @throws RuntimeError 테스트 모드가 아니면 발생한다.
        @throws ValueError `targetSeconds`가 현재 고정 시각보다 작으면 발생한다.
        """
        self.guardTestModeOnly()
        if targetSeconds < self.fixedTimeSeconds:
            raise ValueError("setFixed cannot move the clock backward")
        self.fixedTimeSeconds = targetSeconds

    def advance(self, deltaSeconds: float) -> None:
        """!
        @brief 고정 시각을 `deltaSeconds`만큼 전진시킨다(테스트 모드 전용).
        @param deltaSeconds 전진시킬 시간(초, 0 이상).
        @throws RuntimeError 테스트 모드가 아니면 발생한다.
        @throws ValueError `deltaSeconds`가 음수면 발생한다.
        """
        self.guardTestModeOnly()
        if deltaSeconds < 0:
            raise ValueError("advance requires a non-negative deltaSeconds")
        self.fixedTimeSeconds += deltaSeconds

    def guardTestModeOnly(self) -> None:
        """! @brief 내부 전용: 운영 경로 오용을 차단하는 공통 가드(SWD-001 §10)."""
        if not self.testModeEnabled:
            raise RuntimeError("IClockControl operations require testModeEnabled=True")
