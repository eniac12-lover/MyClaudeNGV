"""!
@brief UNIT-003 판정 인터페이스(AIF-004/005/006/013/014)의 추상 계약을 검증한다.
"""
import unittest

from childlock.common.dataTypes import LockState, PreviousOutputSnapshot, SystemState
from childlock.interfaces.decisionInterfaces import (
    IArbitrationDecision,
    IOutputStateAccess,
    IPriorityRule,
    IRulePriorityRegistry,
    IRuleStateStore,
)


class TestArbitrationDecisionContract(unittest.TestCase):
    ## @brief IArbitrationDecision 직접 인스턴스화가 거부되는지 검증한다(AIF-004).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IArbitrationDecision()  # pylint: disable=abstract-class-instantiated


class TestPriorityRuleContract(unittest.TestCase):
    ## @brief IPriorityRule 직접 인스턴스화가 거부되는지 검증한다(AIF-005).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IPriorityRule()  # pylint: disable=abstract-class-instantiated

    ## @brief evaluate를 구현한 구체 규칙이 None을 반환할 수 있는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteRuleMayReturnNone(self):
        class FakeRule(IPriorityRule):
            def evaluate(self, context):
                return None

        self.assertIsNone(FakeRule().evaluate(None))


class TestOutputStateAccessContract(unittest.TestCase):
    ## @brief IOutputStateAccess 직접 인스턴스화가 거부되는지 검증한다(AIF-006).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IOutputStateAccess()  # pylint: disable=abstract-class-instantiated

    ## @brief getPrevious/update를 구현한 구체 저장소가 계약을 만족하는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteImplementationSatisfiesInterface(self):
        class FakeRepository(IOutputStateAccess):
            def getPrevious(self):
                return PreviousOutputSnapshot(
                    LockState.RELEASE, LockState.RELEASE, SystemState.NORMAL
                )

            def update(self, result, state):
                return None

        repository = FakeRepository()
        self.assertEqual(repository.getPrevious().systemState, SystemState.NORMAL)


class TestRuleStateStoreContract(unittest.TestCase):
    ## @brief IRuleStateStore 직접 인스턴스화가 거부되는지 검증한다(AIF-013).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IRuleStateStore()  # pylint: disable=abstract-class-instantiated


class TestRulePriorityRegistryContract(unittest.TestCase):
    ## @brief IRulePriorityRegistry 직접 인스턴스화가 거부되는지 검증한다(AIF-014).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IRulePriorityRegistry()  # pylint: disable=abstract-class-instantiated


if __name__ == "__main__":
    unittest.main()
