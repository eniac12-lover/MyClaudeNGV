"""!
@brief UNIT-013 `IgnitionOffRule`(DES-007, SWD-001 §5.7/§7-1 순번1, SWR-020).
"""
from typing import Optional

from childlock.common.dataTypes import (
    LockState,
    REASON_IGNITION_OFF,
    RuleDecision,
    RuleEvaluationContext,
    SignalValidity,
)
from childlock.interfaces.decisionInterfaces import IPriorityRule


class IgnitionOffRule(IPriorityRule):
    """! @brief ignition-off 시 좌/우 RELEASE·OFF를 결정한다(최우선순위, §7-1 순번1)."""

    def evaluate(self, context: RuleEvaluationContext) -> Optional[RuleDecision]:
        """!
        @brief ignitionOn이 검증된 FALSE이면 좌/우 모두 RELEASE를 결정한다.
        @param context 이번 평가주기의 불변 컨텍스트.
        @return 조건 미충족/검증 실패/미결정이면 `None`(직전 상태 유지에 위임, UC-03 E1).
        """
        validity = context.validityReport.perSignal["ignitionOn"]
        ignitionOn = context.validatedSnapshot.ignitionOn
        if validity != SignalValidity.NORMAL or ignitionOn is None or ignitionOn:
            return None
        return RuleDecision(
            left=LockState.RELEASE, right=LockState.RELEASE,
            reasonCode=REASON_IGNITION_OFF, priorityReason=REASON_IGNITION_OFF,
        )
