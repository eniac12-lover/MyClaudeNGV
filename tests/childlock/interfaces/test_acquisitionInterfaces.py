"""!
@brief UNIT-002 입력수집 인터페이스(AIF-001/002/003)의 추상 계약을 검증한다.
"""
import unittest

from childlock.common.dataTypes import RawVehicleSnapshot, SignalValidity, ValidityReport
from childlock.interfaces.acquisitionInterfaces import (
    IDriverCommandAcquisition,
    IInputValidityEvaluation,
    IVehicleSignalAcquisition,
)


class TestVehicleSignalAcquisitionContract(unittest.TestCase):
    ## @brief IVehicleSignalAcquisition을 직접 인스턴스화하면 거부되는지 검증한다(AIF-001).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IVehicleSignalAcquisition()  # pylint: disable=abstract-class-instantiated

    ## @brief 두 오퍼레이션을 모두 구현한 구체 클래스가 계약을 만족하는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteImplementationSatisfiesInterface(self):
        class FakeGateway(IVehicleSignalAcquisition):
            def ingest(self, payload):
                return None

            def acquire(self):
                return RawVehicleSnapshot(*([None] * 13))

        gateway = FakeGateway()
        gateway.ingest({"vehicle_speed_kph": 1.0})
        self.assertIsInstance(gateway.acquire(), RawVehicleSnapshot)


class TestDriverCommandAcquisitionContract(unittest.TestCase):
    ## @brief IDriverCommandAcquisition을 직접 인스턴스화하면 거부되는지 검증한다(AIF-002).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IDriverCommandAcquisition()  # pylint: disable=abstract-class-instantiated

    ## @brief 두 오퍼레이션을 모두 구현한 구체 클래스가 계약을 만족하는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteImplementationSatisfiesInterface(self):
        class FakeCommandGateway(IDriverCommandAcquisition):
            def submit(self, payload):
                return None

            def acquireNext(self):
                return None

        gateway = FakeCommandGateway()
        self.assertIsNone(gateway.acquireNext())


class TestInputValidityEvaluationContract(unittest.TestCase):
    ## @brief IInputValidityEvaluation을 직접 인스턴스화하면 거부되는지 검증한다(AIF-003).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IInputValidityEvaluation()  # pylint: disable=abstract-class-instantiated

    ## @brief evaluate 오퍼레이션을 구현한 구체 클래스가 계약을 만족하는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteImplementationSatisfiesInterface(self):
        class FakeMonitor(IInputValidityEvaluation):
            def evaluate(self, snapshot, nowSeconds):
                return ValidityReport({}, (), (), SignalValidity.NORMAL)

        monitor = FakeMonitor()
        report = monitor.evaluate(RawVehicleSnapshot(*([None] * 13)), 0.0)
        self.assertEqual(report.overallValidity, SignalValidity.NORMAL)


if __name__ == "__main__":
    unittest.main()
