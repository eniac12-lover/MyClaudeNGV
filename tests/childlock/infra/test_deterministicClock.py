"""!
@brief UNIT-010 `DeterministicClock`(DES-004, ASIL B 수준 개발)의 계약을 검증한다.
"""
import unittest

from childlock.infra.deterministicClock import DeterministicClock


class TestNowInTestMode(unittest.TestCase):
    ## @brief 테스트 모드에서 now()가 고정 시각을 반환하는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning)
    # @case Positive
    def test_returnsFixedTimeWhenTestModeEnabled(self):
        clock = DeterministicClock(testModeEnabled=True, fixedTimeSeconds=5.0)
        self.assertEqual(clock.now(), 5.0)

    ## @brief 운영 모드에서 now()가 실제 단조 시계 기반 float를 반환하는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning)
    # @case Positive
    def test_returnsMonotonicFloatWhenTestModeDisabled(self):
        clock = DeterministicClock(testModeEnabled=False)
        firstReading = clock.now()
        secondReading = clock.now()
        self.assertIsInstance(firstReading, float)
        self.assertGreaterEqual(secondReading, firstReading)


class TestSetFixed(unittest.TestCase):
    ## @brief 테스트 모드에서 setFixed가 값을 갱신하는지 검증한다.
    # @technique 경계값 분석
    # @case Positive
    def test_updatesFixedTimeWhenTestModeEnabled(self):
        clock = DeterministicClock(testModeEnabled=True, fixedTimeSeconds=1.0)
        clock.setFixed(9.0)
        self.assertEqual(clock.now(), 9.0)

    ## @brief 운영 모드에서 setFixed 호출 시 RuntimeError가 발생하는지 검증한다.
    # @technique 경험 기반 테스트(오용 방지 가드)
    # @case Negative
    def test_rejectsCallWhenTestModeDisabled(self):
        clock = DeterministicClock(testModeEnabled=False)
        with self.assertRaises(RuntimeError):
            clock.setFixed(10.0)

    ## @brief 단조성 위반(과거 시각 설정 시도) 시 ValueError가 발생하는지 검증한다.
    # @technique 경계값 분석(단조성 위반 경계)
    # @case Negative
    def test_rejectsRegressionBelowCurrentFixedTime(self):
        clock = DeterministicClock(testModeEnabled=True, fixedTimeSeconds=5.0)
        with self.assertRaises(ValueError):
            clock.setFixed(4.999)

    ## @brief 현재값과 동일한 시각 설정은 단조성 위반이 아니므로 허용되는지 검증한다.
    # @technique 경계값 분석(단조성 경계 포함)
    # @case Positive
    def test_allowsSettingSameValueAsCurrentFixedTime(self):
        clock = DeterministicClock(testModeEnabled=True, fixedTimeSeconds=5.0)
        clock.setFixed(5.0)
        self.assertEqual(clock.now(), 5.0)


class TestAdvance(unittest.TestCase):
    ## @brief 테스트 모드에서 advance가 고정 시각을 델타만큼 전진시키는지 검증한다.
    # @technique 경계값 분석
    # @case Positive
    def test_increasesFixedTimeByDelta(self):
        clock = DeterministicClock(testModeEnabled=True, fixedTimeSeconds=2.0)
        clock.advance(0.02)
        self.assertAlmostEqual(clock.now(), 2.02)

    ## @brief 운영 모드에서 advance 호출 시 RuntimeError가 발생하는지 검증한다.
    # @technique 경험 기반 테스트(오용 방지 가드)
    # @case Negative
    def test_rejectsCallWhenTestModeDisabled(self):
        clock = DeterministicClock(testModeEnabled=False)
        with self.assertRaises(RuntimeError):
            clock.advance(0.1)

    ## @brief 음수 델타 전진 시도 시 ValueError가 발생하는지 검증한다.
    # @technique 경계값 분석(음수 경계)
    # @case Negative
    def test_rejectsNegativeDelta(self):
        clock = DeterministicClock(testModeEnabled=True, fixedTimeSeconds=2.0)
        with self.assertRaises(ValueError):
            clock.advance(-0.001)

    ## @brief 델타 0 전진은 거부되지 않고 값이 그대로 유지되는지 검증한다.
    # @technique 경계값 분석(0 경계 포함)
    # @case Positive
    def test_allowsZeroDelta(self):
        clock = DeterministicClock(testModeEnabled=True, fixedTimeSeconds=2.0)
        clock.advance(0.0)
        self.assertEqual(clock.now(), 2.0)


if __name__ == "__main__":
    unittest.main()
