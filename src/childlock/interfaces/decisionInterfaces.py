"""!
@brief UNIT-003 판정 계층 인터페이스(AIF-004/005/006/013/014, SWD-001 §4.5).

@details 판정 계층의 계약만 정의한다. `IOutputStateAccess`/`IRuleStateStore`는
구현체가 인프라 계층(`OutputStateRepository`, UNIT-011)에 있지만, 이 계약은
판정 계층(오케스트레이터/규칙)이 필요로 하는 인터페이스이므로 DIP 원칙에 따라
소비 계층 패키지에 정의한다(SWD-001 §2.1 근거).
"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from childlock.common.dataTypes import (
    ArbitrationResult,
    PreviousOutputSnapshot,
    RuleDecision,
    RuleEvaluationContext,
    SystemState,
)


class IArbitrationDecision(ABC):
    """! @brief AIF-004: 규칙 순회를 합성해 최종 결정을 산출하는 계약."""

    @abstractmethod
    def decide(self, context: RuleEvaluationContext) -> ArbitrationResult:
        """!
        @brief 등록된 규칙을 고정 순서로 순회해 side별 최종 결정을 합성한다.
        @param context 이번 평가주기의 불변 컨텍스트.
        @return `ArbitrationResult`(좌/우 항상 확정값).
        """


class IPriorityRule(ABC):
    """! @brief AIF-005: 개별 우선순위 규칙 계약(전략 패턴, SRP)."""

    @abstractmethod
    def evaluate(self, context: RuleEvaluationContext) -> Optional[RuleDecision]:
        """!
        @brief 이 규칙이 이번 컨텍스트에 대해 결정할 수 있는지 평가한다.
        @param context 이번 평가주기의 불변 컨텍스트.
        @return 무관하면 `None`, 결정 가능하면 `RuleDecision`.
        """


class IOutputStateAccess(ABC):
    """! @brief AIF-006: 직전 출력/시스템 상태 접근 계약(SWD-001 §4.6 보완 시그니처)."""

    @abstractmethod
    def getPrevious(self) -> PreviousOutputSnapshot:
        """! @brief 직전 평가주기의 출력/상태 스냅샷을 반환한다(최초 호출은 안전 초기값)."""

    @abstractmethod
    def update(self, result: ArbitrationResult, state: SystemState) -> None:
        """!
        @brief 이번 평가주기의 결과로 직전 출력/상태를 갱신한다.
        @param result 이번 평가주기의 `ArbitrationResult`.
        @param state `StateReasonComposer`가 계산한 `SystemState`.
        """


class IRuleStateStore(ABC):
    """! @brief AIF-013: 규칙별 독립 스크래치 상태 저장 계약(ISP, Phase2 타이머형 규칙 대비)."""

    @abstractmethod
    def get(self, ruleKey: str) -> Any:
        """! @brief `ruleKey`에 저장된 값을 반환한다(없으면 None)."""

    @abstractmethod
    def set(self, ruleKey: str, value: Any) -> None:
        """! @brief `ruleKey`에 값을 저장한다(이후 `get`이 이 값을 반환)."""


class IRulePriorityRegistry(ABC):
    """! @brief AIF-014: 등록된 규칙의 고정 순회 순서 제공 계약."""

    @abstractmethod
    def getOrderedRules(self) -> List[IPriorityRule]:
        """! @brief 항상 동일 순서의 규칙 목록(방어적 복사본)을 반환한다."""
