"""!
@brief UNIT-011 `OutputStateRepository`(DES-005, SWD-001 §5.5). 순수 저장소(판단 없음).
"""
from typing import Any, Dict

from childlock.common.dataTypes import (
    ArbitrationResult,
    LockState,
    PreviousOutputSnapshot,
    SystemState,
)
from childlock.interfaces.decisionInterfaces import IOutputStateAccess, IRuleStateStore


class OutputStateRepository(IOutputStateAccess, IRuleStateStore):
    """!
    @brief 직전 side별 출력/시스템 상태 및 규칙별 스크래치 상태를 보관한다.

    @details AIF-006(IOutputStateAccess)과 AIF-013(IRuleStateStore) 두 계약을
    한 클래스가 구현한다(SWD-001 §3.1 클래스 다이어그램). 두 계약 모두 "저장"
    책임만 가지므로 SRP를 위반하지 않는다.
    """

    def __init__(self) -> None:
        """! @brief 안전 초기값(RELEASE/RELEASE/NORMAL)으로 저장소를 초기화한다(SWD-001 §8.2)."""
        ## @brief 좌측 잠금 상태(초기값 RELEASE, 안전 초기 상태).
        self.leftState = LockState.RELEASE
        ## @brief 우측 잠금 상태(초기값 RELEASE, 안전 초기 상태).
        self.rightState = LockState.RELEASE
        ## @brief 시스템 상태(초기값 NORMAL, 최초 평가주기 종료 즉시 재계산됨).
        self.systemState = SystemState.NORMAL
        ## @brief 규칙별 독립 스크래치 상태 공간(AIF-013, Phase1 규칙은 미사용).
        self.ruleScratch: Dict[str, Any] = {}

    def getPrevious(self) -> PreviousOutputSnapshot:
        """! @brief 직전 평가주기의 출력/상태 스냅샷을 반환한다."""
        return PreviousOutputSnapshot(self.leftState, self.rightState, self.systemState)

    def update(self, result: ArbitrationResult, state: SystemState) -> None:
        """! @brief 이번 평가주기의 결과로 직전 출력/상태를 갱신한다."""
        self.leftState = result.left
        self.rightState = result.right
        self.systemState = state

    def get(self, ruleKey: str) -> Any:
        """! @brief `ruleKey`에 저장된 값을 반환한다(없으면 None)."""
        return self.ruleScratch.get(ruleKey)

    def set(self, ruleKey: str, value: Any) -> None:
        """! @brief `ruleKey`에 값을 저장한다."""
        self.ruleScratch[ruleKey] = value
