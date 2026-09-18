"""!
@brief UNIT-014 `AutoLockRule`(DES-008, SWD-001 §5.7/§6.4/§7-2, SWR-003/004).
"""
from typing import Optional

from childlock.common.dataTypes import (
    LockState,
    REASON_AUTO_LOCK_SPEED,
    REASON_RELEASE_BLOCKED_AUTO_LOCK,
    RuleDecision,
    RuleEvaluationContext,
    SignalValidity,
)
from childlock.interfaces.decisionInterfaces import IPriorityRule

## @brief 자동 잠금 활성 임계 속도(km/h, SWR-003). 이 값 이상이면 활성(경계 포함).
AUTO_LOCK_THRESHOLD_KPH = 3.0


class AutoLockRule(IPriorityRule):
    """! @brief 속도≥3km/h 활성 조건에서 좌/우 LOCK을 강제하고 해제를 차단한다."""

    def evaluate(self, context: RuleEvaluationContext) -> Optional[RuleDecision]:
        """!
        @brief 신뢰 가능한 속도가 임계 이상이면 좌/우 LOCK을 결정한다.
        @param context 이번 평가주기의 불변 컨텍스트.
        @return 조건 미충족/검증 실패/미결정이면 `None`(UC-04 E1).
        """
        validity = context.validityReport.perSignal["vehicleSpeedKph"]
        speed = context.validatedSnapshot.vehicleSpeedKph
        if validity != SignalValidity.NORMAL or speed is None:
            return None
        if speed < AUTO_LOCK_THRESHOLD_KPH:
            return None
        reasonCode = self.resolveReasonCode(context)
        return RuleDecision(
            left=LockState.LOCK, right=LockState.LOCK,
            reasonCode=reasonCode, priorityReason="auto_lock_active",
        )

    def resolveReasonCode(self, context: RuleEvaluationContext) -> str:
        """!
        @brief 내부 전용: 해제 시도 여부에 따라 §7-2 결정표의 reasonCode를 선택한다.
        @param context 이번 평가주기의 불변 컨텍스트.
        @return 해제 명령이 있으면 RELEASE_BLOCKED_AUTO_LOCK, 아니면 AUTO_LOCK_SPEED.
        """
        blockingRelease = (
            context.command is not None and context.command.action == LockState.RELEASE
        )
        if blockingRelease:
            return REASON_RELEASE_BLOCKED_AUTO_LOCK
        return REASON_AUTO_LOCK_SPEED
