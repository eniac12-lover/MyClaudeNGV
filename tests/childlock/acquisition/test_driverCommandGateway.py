"""!
@brief UNIT-008 `DriverCommandGateway`(DES-002, SWD-001 §5.2/§6.2)의 계약을 검증한다.
"""
import unittest

from childlock.acquisition.driverCommandGateway import DriverCommandGateway
from childlock.common.dataTypes import CommandSource, LockState, Side


class TestValidCombinations(unittest.TestCase):
    ## @brief source×action×side 정상 조합 24가지가 모두 유효 명령으로 인식되는지 검증한다.
    # @technique 전수 조합 테스트(Exhaustive Combinatorial Testing) — SWR-001 수용기준(1)
    # @case Positive
    def test_acceptsAllTwentyFourValidCombinations(self):
        sources = ["physical_button", "avn", "voice", "mobile_app"]
        actions = ["lock", "unlock"]
        sides = ["left", "right", "all"]
        expectedSource = {
            "physical_button": CommandSource.PHYSICAL_BUTTON,
            "avn": CommandSource.AVN,
            "voice": CommandSource.VOICE,
            "mobile_app": CommandSource.MOBILE_APP,
        }
        expectedAction = {"lock": LockState.LOCK, "unlock": LockState.RELEASE}
        expectedSide = {"left": Side.LEFT, "right": Side.RIGHT, "all": Side.ALL}

        checkedCount = 0
        for source in sources:
            for action in actions:
                for side in sides:
                    gateway = DriverCommandGateway()
                    gateway.submit(
                        {"side": side, "action": action, "source": source, "timestamp_s": 1.0}
                    )
                    command = gateway.acquireNext()
                    self.assertIsNotNone(command)
                    self.assertEqual(command.side, expectedSide[side])
                    self.assertEqual(command.action, expectedAction[action])
                    self.assertEqual(command.source, expectedSource[source])
                    checkedCount += 1
        self.assertEqual(checkedCount, 24)


class TestFieldValidationRejection(unittest.TestCase):
    ## @brief 미등록 side 값을 4개 source 각각에서 주입 시 거절되고 로그가 남는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning) — 무효 입력 클래스, SWR-001 수용기준(2)
    # @case Negative
    def test_rejectsUnregisteredSideForEverySource(self):
        for source in ["physical_button", "avn", "voice", "mobile_app"]:
            gateway = DriverCommandGateway()
            gateway.submit(
                {"side": "BOTH", "action": "lock", "source": source, "timestamp_s": 1.0}
            )
            self.assertIsNone(gateway.acquireNext())
            self.assertEqual(gateway.getRejectionLog()[0].reasonCode, "INVALID_COMMAND")

    ## @brief 미등록 action 값이 거절되는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning) — 무효 입력 클래스
    # @case Negative
    def test_rejectsUnregisteredAction(self):
        gateway = DriverCommandGateway()
        gateway.submit(
            {"side": "left", "action": "OPEN", "source": "avn", "timestamp_s": 1.0}
        )
        self.assertIsNone(gateway.acquireNext())

    ## @brief 미등록 source 값이 거절되는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning) — 무효 입력 클래스
    # @case Negative
    def test_rejectsUnregisteredSource(self):
        gateway = DriverCommandGateway()
        gateway.submit(
            {"side": "left", "action": "lock", "source": "bluetooth", "timestamp_s": 1.0}
        )
        self.assertIsNone(gateway.acquireNext())

    ## @brief timestamp_s 누락 명령이 거절되는지 검증한다.
    # @technique 경계값 분석(필수 필드 누락)
    # @case Negative
    def test_rejectsMissingTimestamp(self):
        gateway = DriverCommandGateway()
        gateway.submit({"side": "left", "action": "lock", "source": "avn"})
        self.assertIsNone(gateway.acquireNext())


class TestQueueBehavior(unittest.TestCase):
    ## @brief 큐가 비어있으면 acquireNext가 None을 반환하는지 검증한다.
    # @technique 경계값 분석(빈 큐)
    # @case Positive
    def test_returnsNoneWhenQueueEmpty(self):
        gateway = DriverCommandGateway()
        self.assertIsNone(gateway.acquireNext())

    ## @brief acquireNext가 큐에서 정확히 1건만 꺼내는지(FIFO) 검증한다.
    # @technique 상태 전이 테스트
    # @case Positive
    def test_acquireNextDequeuesExactlyOneItemInOrder(self):
        gateway = DriverCommandGateway()
        gateway.submit({"side": "left", "action": "lock", "source": "avn", "timestamp_s": 1.0})
        gateway.submit({"side": "right", "action": "lock", "source": "avn", "timestamp_s": 2.0})
        first = gateway.acquireNext()
        second = gateway.acquireNext()
        self.assertEqual(first.side, Side.LEFT)
        self.assertEqual(second.side, Side.RIGHT)
        self.assertIsNone(gateway.acquireNext())


if __name__ == "__main__":
    unittest.main()
