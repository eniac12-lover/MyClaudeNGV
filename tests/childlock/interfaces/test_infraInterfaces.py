"""!
@brief UNIT-005 인프라 인터페이스(AIF-012/016)의 추상 계약을 검증한다.
"""
import unittest

from childlock.interfaces.infraInterfaces import IClockControl, IClockSource


class TestClockSourceContract(unittest.TestCase):
    ## @brief IClockSource 직접 인스턴스화가 거부되는지 검증한다(AIF-012).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IClockSource()  # pylint: disable=abstract-class-instantiated

    ## @brief now를 구현한 구체 클래스가 float를 반환하는지 검증한다.
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Positive
    def test_concreteImplementationSatisfiesInterface(self):
        class FakeClock(IClockSource):
            def now(self):
                return 1.5

        self.assertEqual(FakeClock().now(), 1.5)


class TestClockControlContract(unittest.TestCase):
    ## @brief IClockControl 직접 인스턴스화가 거부되는지 검증한다(AIF-016).
    # @technique 체크리스트 기반 테스트(ABC 추상 계약 준수)
    # @case Negative
    def test_rejectsDirectInstantiation(self):
        with self.assertRaises(TypeError):
            IClockControl()  # pylint: disable=abstract-class-instantiated


if __name__ == "__main__":
    unittest.main()
