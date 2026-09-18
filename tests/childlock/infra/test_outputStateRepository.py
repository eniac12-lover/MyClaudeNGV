"""!
@brief UNIT-011 `OutputStateRepository`(DES-005, SWD-001 §5.5)의 계약을 검증한다.
"""
import unittest

from childlock.common.dataTypes import ArbitrationResult, LockState, SystemState
from childlock.infra.outputStateRepository import OutputStateRepository


class TestGetPrevious(unittest.TestCase):
    ## @brief 최초 호출 시 안전 초기값(RELEASE/RELEASE/NORMAL)을 반환하는지 검증한다.
    # @technique 경계값 분석(초기 안전 상태)
    # @case Positive
    def test_returnsSafeInitialStateOnFirstCall(self):
        repository = OutputStateRepository()
        previous = repository.getPrevious()
        self.assertEqual(previous.leftState, LockState.RELEASE)
        self.assertEqual(previous.rightState, LockState.RELEASE)
        self.assertEqual(previous.systemState, SystemState.NORMAL)

    ## @brief update 이후 getPrevious가 갱신된 값을 반영하는지 검증한다.
    # @technique 상태 전이 테스트
    # @case Positive
    def test_reflectsUpdateOnSubsequentCall(self):
        repository = OutputStateRepository()
        result = ArbitrationResult(
            left=LockState.LOCK, right=LockState.RELEASE,
            winningRuleLeft="AutoLockRule", winningRuleRight="HoldLastOutputRule",
            reasonCode="AUTO_LOCK_SPEED", priorityReason="auto_lock_active",
        )
        repository.update(result, SystemState.NORMAL)
        previous = repository.getPrevious()
        self.assertEqual(previous.leftState, LockState.LOCK)
        self.assertEqual(previous.rightState, LockState.RELEASE)
        self.assertEqual(previous.systemState, SystemState.NORMAL)


class TestRuleStateStore(unittest.TestCase):
    ## @brief 등록되지 않은 ruleKey를 조회하면 None을 반환하는지 검증한다.
    # @technique 경계값 분석(미등록 키 기본값)
    # @case Negative
    def test_getReturnsNoneForUnknownKey(self):
        repository = OutputStateRepository()
        self.assertIsNone(repository.get("unknownRule"))

    ## @brief set 이후 동일 ruleKey의 get이 저장된 값을 반환하는지 검증한다.
    # @technique 상태 전이 테스트
    # @case Positive
    def test_getReturnsValueSetForSameKey(self):
        repository = OutputStateRepository()
        repository.set("timerRule", 42)
        self.assertEqual(repository.get("timerRule"), 42)


if __name__ == "__main__":
    unittest.main()
