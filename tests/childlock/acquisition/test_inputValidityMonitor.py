"""!
@brief UNIT-009 `InputValidityMonitor`(DES-003, ASIL B, SWD-001 §5.3/§6.3)의 계약을 검증한다.

@details SWR-013a(freshness 경계값 199/200/201/300/301ms)와 SWR-013b(형식/범위 오류)의
수용기준을 모두 실행 가능한 테스트로 변환한다.
"""
import unittest

from childlock.acquisition.inputValidityMonitor import InputValidityMonitor
from childlock.common.dataTypes import RawVehicleSnapshot, SignalValidity


## @brief 12개 신호가 모두 형식적으로 유효한 기준 스냅샷을 만든다(테스트 헬퍼, 프로덕션 코드 아님).
def buildValidSnapshot(sourceTimestampS=0.0):
    return RawVehicleSnapshot(
        vehicleSpeedKph=10.0, gear="D", crashStatus="NONE",
        rearLeftApproachRisk=False, rearRightApproachRisk=False,
        fireDetected=False, overtemperatureDetected=False, adultPresent=False,
        isofixLeft=False, isofixRight=False, ignitionOn=True, sensorFault=False,
        sourceTimestampS=sourceTimestampS,
    )


class TestAllSignalsValidAndFresh(unittest.TestCase):
    ## @brief 12개 신호가 전부 형식 유효+신선하면 overall이 NORMAL인지 검증한다.
    # @technique 동등분할(Equivalence Partitioning) — 정상 입력 클래스
    # @case Positive
    def test_overallIsNormalWhenAllSignalsValidAndFresh(self):
        monitor = InputValidityMonitor()
        report = monitor.evaluate(buildValidSnapshot(0.0), nowSeconds=0.1)
        self.assertEqual(report.overallValidity, SignalValidity.NORMAL)
        self.assertEqual(len(report.perSignal), 12)
        self.assertEqual(report.staleSignalNames, ())
        self.assertEqual(report.invalidSignalNames, ())


class TestFreshnessBoundaries(unittest.TestCase):
    ## @brief 199ms 경과 시 NORMAL(경계 이내)인지 검증한다(SWR-013a 경계값).
    # @technique 경계값 분석(Boundary Value Analysis)
    # @case Positive
    def test_normalAt199MsElapsed(self):
        monitor = InputValidityMonitor()
        report = monitor.evaluate(buildValidSnapshot(0.0), nowSeconds=0.199)
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.NORMAL)

    ## @brief 정확히 200ms 경과 시에도 NORMAL(<=200ms는 신선)인지 검증한다(SWR-013a 경계값).
    # @technique 경계값 분석(Boundary Value Analysis)
    # @case Positive
    def test_normalAt200MsElapsedInclusiveBoundary(self):
        monitor = InputValidityMonitor()
        report = monitor.evaluate(buildValidSnapshot(0.0), nowSeconds=0.200)
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.NORMAL)

    ## @brief 201ms 경과 시 DEGRADED로 즉시 전이하는지 검증한다(SWR-013a 경계값).
    # @technique 경계값 분석(Boundary Value Analysis)
    # @case Negative
    def test_degradedAt201MsElapsed(self):
        monitor = InputValidityMonitor()
        report = monitor.evaluate(buildValidSnapshot(0.0), nowSeconds=0.201)
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.DEGRADED)
        self.assertIn("vehicleSpeedKph", report.staleSignalNames)

    ## @brief 300ms 경과 시에도 DEGRADED가 유지되는지 검증한다(SWR-013a 경계값).
    # @technique 경계값 분석(Boundary Value Analysis)
    # @case Negative
    def test_degradedAt300MsElapsed(self):
        monitor = InputValidityMonitor()
        report = monitor.evaluate(buildValidSnapshot(0.0), nowSeconds=0.300)
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.DEGRADED)

    ## @brief 301ms 경과 시에도 DEGRADED가 유지되는지 검증한다(SWR-013a 경계값).
    # @technique 경계값 분석(Boundary Value Analysis)
    # @case Negative
    def test_degradedAt301MsElapsed(self):
        monitor = InputValidityMonitor()
        report = monitor.evaluate(buildValidSnapshot(0.0), nowSeconds=0.301)
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.DEGRADED)

    ## @brief sourceTimestampS가 None이면 신선하지 않음(DEGRADED)으로 처리되는지 검증한다.
    # @technique 경계값 분석(누락 기준시각)
    # @case Negative
    def test_treatsMissingSourceTimestampAsNotFresh(self):
        monitor = InputValidityMonitor()
        report = monitor.evaluate(buildValidSnapshot(None), nowSeconds=1.0)
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.DEGRADED)


class TestFormatValidation(unittest.TestCase):
    ## @brief 속도가 범위 하한 미만(-5)이면 INVALID인지 검증한다(SWR-013b).
    # @technique 경계값 분석 + 동등분할
    # @case Negative
    def test_invalidWhenSpeedBelowRange(self):
        monitor = InputValidityMonitor()
        snapshot = buildValidSnapshot(0.0)
        snapshot = RawVehicleSnapshot(**{**snapshot.__dict__, "vehicleSpeedKph": -5.0})
        report = monitor.evaluate(snapshot, nowSeconds=0.0)
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.INVALID)
        self.assertIn("vehicleSpeedKph", report.invalidSignalNames)

    ## @brief 속도가 범위 상한 초과(301)이면 INVALID인지 검증한다(SWR-013b).
    # @technique 경계값 분석 + 동등분할
    # @case Negative
    def test_invalidWhenSpeedAboveRange(self):
        monitor = InputValidityMonitor()
        snapshot = buildValidSnapshot(0.0)
        snapshot = RawVehicleSnapshot(**{**snapshot.__dict__, "vehicleSpeedKph": 301.0})
        report = monitor.evaluate(snapshot, nowSeconds=0.0)
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.INVALID)

    ## @brief gear가 미등록 값("X")이면 INVALID인지 검증한다(SWR-013b).
    # @technique 동등분할(Equivalence Partitioning) — 무효 열거값
    # @case Negative
    def test_invalidWhenGearIsUnregisteredValue(self):
        monitor = InputValidityMonitor()
        snapshot = buildValidSnapshot(0.0)
        snapshot = RawVehicleSnapshot(**{**snapshot.__dict__, "gear": "X"})
        report = monitor.evaluate(snapshot, nowSeconds=0.0)
        self.assertEqual(report.perSignal["gear"], SignalValidity.INVALID)

    ## @brief crashStatus가 미등록 값("UNKNOWN")이면 INVALID인지 검증한다(SWR-013b).
    # @technique 동등분할(Equivalence Partitioning) — 무효 열거값
    # @case Negative
    def test_invalidWhenCrashStatusIsUnknown(self):
        monitor = InputValidityMonitor()
        snapshot = buildValidSnapshot(0.0)
        snapshot = RawVehicleSnapshot(**{**snapshot.__dict__, "crashStatus": "UNKNOWN"})
        report = monitor.evaluate(snapshot, nowSeconds=0.0)
        self.assertEqual(report.perSignal["crashStatus"], SignalValidity.INVALID)

    ## @brief boolean 신호에 비boolean 값이 들어오면 INVALID인지 검증한다(SWR-013b).
    # @technique 동등분할(Equivalence Partitioning) — 타입 불일치
    # @case Negative
    def test_invalidWhenBooleanSignalHasNonBooleanValue(self):
        monitor = InputValidityMonitor()
        snapshot = buildValidSnapshot(0.0)
        snapshot = RawVehicleSnapshot(**{**snapshot.__dict__, "ignitionOn": "yes"})
        report = monitor.evaluate(snapshot, nowSeconds=0.0)
        self.assertEqual(report.perSignal["ignitionOn"], SignalValidity.INVALID)

    ## @brief 신호값이 None(누락)이면 INVALID인지 검증한다.
    # @technique 경계값 분석(누락 값)
    # @case Negative
    def test_invalidWhenSignalValueIsNone(self):
        monitor = InputValidityMonitor()
        snapshot = buildValidSnapshot(0.0)
        snapshot = RawVehicleSnapshot(**{**snapshot.__dict__, "sensorFault": None})
        report = monitor.evaluate(snapshot, nowSeconds=0.0)
        self.assertEqual(report.perSignal["sensorFault"], SignalValidity.INVALID)

    ## @brief evaluate가 극단적으로 잘못된 타입 입력에도 예외를 던지지 않는지 검증한다.
    # @technique 경험 기반 테스트(예외 없음 설계 불변, AIF-003)
    # @case Negative
    def test_neverRaisesEvenWithGarbageTypes(self):
        monitor = InputValidityMonitor()
        snapshot = buildValidSnapshot(0.0)
        snapshot = RawVehicleSnapshot(
            **{**snapshot.__dict__, "vehicleSpeedKph": "not-a-number", "gear": 123}
        )
        try:
            report = monitor.evaluate(snapshot, nowSeconds=0.0)
        except Exception as error:  # pylint: disable=broad-exception-caught
            self.fail(f"evaluate raised an exception: {error}")
        self.assertEqual(report.perSignal["vehicleSpeedKph"], SignalValidity.INVALID)
        self.assertEqual(report.perSignal["gear"], SignalValidity.INVALID)


class TestOverallValidityPriority(unittest.TestCase):
    ## @brief INVALID와 DEGRADED가 혼재하면 overall이 INVALID(최악값)인지 검증한다.
    # @technique 결정 테이블 테스트(우선순위 규칙)
    # @case Positive
    def test_overallIsInvalidWhenInvalidAndDegradedBothPresent(self):
        monitor = InputValidityMonitor()
        snapshot = buildValidSnapshot(0.0)
        snapshot = RawVehicleSnapshot(**{**snapshot.__dict__, "gear": "X"})
        report = monitor.evaluate(snapshot, nowSeconds=0.201)
        self.assertEqual(report.overallValidity, SignalValidity.INVALID)


if __name__ == "__main__":
    unittest.main()
