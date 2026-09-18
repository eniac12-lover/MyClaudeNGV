"""!
@brief UNIT-014 `AutoLockRule`(DES-008, SWD-001 §5.7/§6.4)의 계약을 검증한다(SWR-003/004).
"""
import unittest

from childlock.common.dataTypes import (
    CommandSource,
    LockState,
    Side,
    SignalValidity,
    ValidatedCommand,
)
from childlock.decision.rules.autoLockRule import AutoLockRule
from tests.childlock.decision.contextTestSupport import buildContext


class TestSpeedBoundary(unittest.TestCase):
    ## @brief 속도 2.9km/h(임계 미만)에서는 무관 판정(None)인지 검증한다(SWR-003 경계값).
    # @technique 경계값 분석(Boundary Value Analysis)
    # @case Positive
    def test_returnsNoneBelowThreeKph(self):
        rule = AutoLockRule()
        context = buildContext(speed=2.9, speedValidity=SignalValidity.NORMAL)
        self.assertIsNone(rule.evaluate(context))

    ## @brief 정확히 3.0km/h(경계 포함)에서 좌우 LOCK을 결정하는지 검증한다(SWR-003 경계값).
    # @technique 경계값 분석(Boundary Value Analysis)
    # @case Positive
    def test_activatesAtExactlyThreeKph(self):
        rule = AutoLockRule()
        context = buildContext(speed=3.0, speedValidity=SignalValidity.NORMAL)
        decision = rule.evaluate(context)
        self.assertEqual(decision.left, LockState.LOCK)
        self.assertEqual(decision.right, LockState.LOCK)
        self.assertEqual(decision.reasonCode, "AUTO_LOCK_SPEED")

    ## @brief 3.1km/h(임계 초과)에서도 좌우 LOCK을 결정하는지 검증한다(SWR-003 경계값).
    # @technique 경계값 분석(Boundary Value Analysis)
    # @case Positive
    def test_activatesAboveThreeKph(self):
        rule = AutoLockRule()
        context = buildContext(speed=3.1, speedValidity=SignalValidity.NORMAL)
        decision = rule.evaluate(context)
        self.assertEqual(decision.left, LockState.LOCK)
        self.assertEqual(decision.right, LockState.LOCK)


class TestValidityAndMissingSpeed(unittest.TestCase):
    ## @brief 속도 검증이 DEGRADED이면 신뢰 불가로 판단해 None을 반환하는지 검증한다.
    # @technique 경험 기반 테스트(UC-04 E1 신뢰 불가 값 처리)
    # @case Negative
    def test_returnsNoneWhenSpeedValidityIsDegraded(self):
        rule = AutoLockRule()
        context = buildContext(speed=10.0, speedValidity=SignalValidity.DEGRADED)
        self.assertIsNone(rule.evaluate(context))

    ## @brief 속도 값이 None(미결정)이면 None을 반환하는지 검증한다.
    # @technique 경계값 분석(누락 값)
    # @case Negative
    def test_returnsNoneWhenSpeedIsMissing(self):
        rule = AutoLockRule()
        context = buildContext(speed=None, speedValidity=SignalValidity.NORMAL)
        self.assertIsNone(rule.evaluate(context))


class TestReasonCodeBySwr004(unittest.TestCase):
    ## @brief 해제 명령이 없으면 reasonCode=AUTO_LOCK_SPEED인지 검증한다(SWR-003 수용기준).
    # @technique 결정 테이블 테스트 — §7-2
    # @case Positive
    def test_reasonCodeIsAutoLockSpeedWhenNoReleaseCommand(self):
        rule = AutoLockRule()
        context = buildContext(speed=5.0, speedValidity=SignalValidity.NORMAL, command=None)
        decision = rule.evaluate(context)
        self.assertEqual(decision.reasonCode, "AUTO_LOCK_SPEED")
        self.assertEqual(decision.priorityReason, "auto_lock_active")

    ## @brief 해제 명령이 있으면 reasonCode=RELEASE_BLOCKED_AUTO_LOCK인지 검증한다(SWR-004).
    # @technique 결정 테이블 테스트 — §7-2
    # @case Positive
    def test_reasonCodeIsReleaseBlockedWhenReleaseCommandPresent(self):
        rule = AutoLockRule()
        releaseCommand = ValidatedCommand(
            side=Side.LEFT, action=LockState.RELEASE,
            source=CommandSource.AVN, timestampS=1.0,
        )
        context = buildContext(
            speed=5.0, speedValidity=SignalValidity.NORMAL, command=releaseCommand
        )
        decision = rule.evaluate(context)
        self.assertEqual(decision.reasonCode, "RELEASE_BLOCKED_AUTO_LOCK")

    ## @brief 해제가 아닌 LOCK 명령이 있어도 reasonCode=AUTO_LOCK_SPEED인지 검증한다.
    # @technique 결정 테이블 테스트 — §7-2
    # @case Positive
    def test_reasonCodeIsAutoLockSpeedWhenLockCommandPresent(self):
        rule = AutoLockRule()
        lockCommand = ValidatedCommand(
            side=Side.LEFT, action=LockState.LOCK,
            source=CommandSource.AVN, timestampS=1.0,
        )
        context = buildContext(
            speed=5.0, speedValidity=SignalValidity.NORMAL, command=lockCommand
        )
        decision = rule.evaluate(context)
        self.assertEqual(decision.reasonCode, "AUTO_LOCK_SPEED")


if __name__ == "__main__":
    unittest.main()
