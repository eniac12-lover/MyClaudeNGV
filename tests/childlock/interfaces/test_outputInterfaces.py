"""!
@brief UNIT-004 출력 인터페이스(AIF-007/008/009/010)의 추상 계약을 검증한다.
"""
import unittest

from childlock.common.dataTypes import Ack, LockState
from childlock.interfaces.outputInterfaces import (
    IActuatorOutputSink,
    IControlResultComposition,
    IEventHistoryQuery,
    IEventHistoryRecording,
)


class TestActuatorOutputSinkContract(unittest.TestCase):
    ## @brief IActuatorOutputSink 직접 인스턴스화가 거부되는지 검증한다(AIF-007).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IActuatorOutputSink()  # pylint: disable=abstract-class-instantiated

    ## @brief apply를 구현한 구체 싱크가 Ack를 반환하는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteImplementationSatisfiesInterface(self):
        class FakeSink(IActuatorOutputSink):
            def apply(self, left, right):
                return Ack(accepted=True)

        result = FakeSink().apply(LockState.LOCK, LockState.RELEASE)
        self.assertTrue(result.accepted)


class TestControlResultCompositionContract(unittest.TestCase):
    ## @brief IControlResultComposition 직접 인스턴스화가 거부되는지 검증한다(AIF-008).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IControlResultComposition()  # pylint: disable=abstract-class-instantiated


class TestEventHistoryRecordingContract(unittest.TestCase):
    ## @brief IEventHistoryRecording 직접 인스턴스화가 거부되는지 검증한다(AIF-009).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IEventHistoryRecording()  # pylint: disable=abstract-class-instantiated


class TestEventHistoryQueryContract(unittest.TestCase):
    ## @brief IEventHistoryQuery 직접 인스턴스화가 거부되는지 검증한다(AIF-010).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IEventHistoryQuery()  # pylint: disable=abstract-class-instantiated

    ## @brief query를 구현한 구체 클래스가 리스트를 반환하는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteImplementationSatisfiesInterface(self):
        class FakeQuery(IEventHistoryQuery):
            def query(self, limit):
                return []

        self.assertEqual(FakeQuery().query(10), [])


if __name__ == "__main__":
    unittest.main()
