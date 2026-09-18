"""!
@brief UNIT-006 제어 인터페이스(AIF-015)의 추상 계약을 검증한다.
"""
import unittest

from childlock.common.dataTypes import ControlResultRecord, CycleResult, SignalValidity, SystemState
from childlock.interfaces.controlInterfaces import IEvaluationCycleControl


class TestEvaluationCycleControlContract(unittest.TestCase):
    ## @brief IEvaluationCycleControl 직접 인스턴스화가 거부되는지 검증한다(AIF-015).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IEvaluationCycleControl()  # pylint: disable=abstract-class-instantiated

    ## @brief runCycle을 구현한 구체 클래스가 CycleResult를 반환하는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteImplementationSatisfiesInterface(self):
        class FakeController(IEvaluationCycleControl):
            def runCycle(self):
                controlResult = ControlResultRecord(
                    SystemState.NORMAL, "hold_last_output",
                    "HOLD_LAST_OUTPUT", SignalValidity.NORMAL,
                )
                return CycleResult(0.0, controlResult, 1)

        result = FakeController().runCycle()
        self.assertEqual(result.eventId, 1)


if __name__ == "__main__":
    unittest.main()
