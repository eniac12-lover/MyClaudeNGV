"""!
@brief UNIT-013 `IgnitionOffRule`(DES-007, SWD-001 §5.7)의 계약을 검증한다(SWR-020).
"""
import unittest

from childlock.common.dataTypes import LockState, SignalValidity
from childlock.decision.rules.ignitionOffRule import IgnitionOffRule
from tests.childlock.decision.contextTestSupport import buildContext


class TestIgnitionOffRule(unittest.TestCase):
    ## @brief ignitionOn=False & 검증 NORMAL이면 좌우 RELEASE, reasonCode=ignition_off인지 검증한다.
    # @technique 결정 테이블 테스트 — SWR-020 수용기준
    # @case Positive
    def test_returnsReleaseBothSidesWhenIgnitionOffConfirmed(self):
        rule = IgnitionOffRule()
        context = buildContext(ignitionOn=False, ignitionValidity=SignalValidity.NORMAL)
        decision = rule.evaluate(context)
        self.assertEqual(decision.left, LockState.RELEASE)
        self.assertEqual(decision.right, LockState.RELEASE)
        self.assertEqual(decision.reasonCode, "ignition_off")
        self.assertEqual(decision.priorityReason, "ignition_off")

    ## @brief ignitionOn=True(시동 켜짐)이면 무관 판정(None)인지 검증한다.
    # @technique 동등분할(Equivalence Partitioning)
    # @case Positive
    def test_returnsNoneWhenIgnitionIsOn(self):
        rule = IgnitionOffRule()
        context = buildContext(ignitionOn=True, ignitionValidity=SignalValidity.NORMAL)
        self.assertIsNone(rule.evaluate(context))

    ## @brief ignitionOn 값이 검증 실패(DEGRADED)면 직전 상태 유지에 위임(None)하는지 검증한다.
    # @technique 경험 기반 테스트(UC-03 E1 "직전 상태 유지" 패턴)
    # @case Negative
    def test_returnsNoneWhenIgnitionValidityIsDegraded(self):
        rule = IgnitionOffRule()
        context = buildContext(ignitionOn=False, ignitionValidity=SignalValidity.DEGRADED)
        self.assertIsNone(rule.evaluate(context))

    ## @brief ignitionOn 값이 None(미결정)이면 None을 반환하는지 검증한다.
    # @technique 경계값 분석(누락 값)
    # @case Negative
    def test_returnsNoneWhenIgnitionValueIsMissing(self):
        rule = IgnitionOffRule()
        context = buildContext(ignitionOn=None, ignitionValidity=SignalValidity.NORMAL)
        self.assertIsNone(rule.evaluate(context))


if __name__ == "__main__":
    unittest.main()
