"""!
@brief UNIT-008 `DriverCommandGateway`(DES-002, SWD-001 §5.2/§6.2).
"""
import queue
from collections import deque
from typing import Optional, Tuple

from childlock.common.dataTypes import (
    CommandRejection,
    CommandSource,
    LockState,
    RawDriverCommand,
    Side,
    ValidatedCommand,
)
from childlock.interfaces.acquisitionInterfaces import IDriverCommandAcquisition

## @brief OEM-IF-004 side 값 → 내부 Side 매핑(SWD-001 §6.2).
SIDE_MAP = {"left": Side.LEFT, "right": Side.RIGHT, "all": Side.ALL}
## @brief OEM-IF-004 action 값 → 내부 LockState 매핑(SWD-001 §6.2).
ACTION_MAP = {"lock": LockState.LOCK, "unlock": LockState.RELEASE}
## @brief OEM-IF-004 source 값 → 내부 CommandSource 매핑(SWD-001 §6.2).
SOURCE_MAP = {
    "physical_button": CommandSource.PHYSICAL_BUTTON,
    "avn": CommandSource.AVN,
    "voice": CommandSource.VOICE,
    "mobile_app": CommandSource.MOBILE_APP,
}
## @brief 거절 로그 순환 보존 상한(진단 편의, AIF-002 계약 외).
REJECTION_LOG_CAPACITY = 100


class DriverCommandGateway(IDriverCommandAcquisition):
    """! @brief 4-source 명령을 큐잉·필드검증하여 `ValidatedCommand`/거절을 산출한다."""

    def __init__(self) -> None:
        """! @brief 스레드 안전 큐와 순환 거절 로그를 초기화한다."""
        ## @brief 미결(未決) 명령 큐. 여러 채널이 동시에 submit해도 안전하다(queue.Queue).
        self.commandQueue: "queue.Queue[RawDriverCommand]" = queue.Queue()
        ## @brief 진단 전용 거절 이력(최대 100건 순환, AIF-002 계약 외 편의 기능).
        self.rejectionLog: deque = deque(maxlen=REJECTION_LOG_CAPACITY)

    def submit(self, payload: dict) -> None:
        """! @brief payload를 `RawDriverCommand`로 어댑팅해 큐에 적재한다."""
        source = payload if payload is not None else {}
        raw = RawDriverCommand(
            side=source.get("side"),
            action=source.get("action"),
            source=source.get("source"),
            timestampS=source.get("timestamp_s"),
        )
        self.commandQueue.put(raw)

    def acquireNext(self) -> Optional[ValidatedCommand]:
        """!
        @brief 큐에서 1건을 꺼내 필드검증 후 반환한다.
        @return 유효하면 `ValidatedCommand`, 큐가 비었거나 무효하면 `None`
        (무효 시 `rejectionLog`에 기록).
        """
        if self.commandQueue.empty():
            return None
        raw = self.commandQueue.get()
        validated = self.validateCommandFields(raw)
        if validated is None:
            self.rejectionLog.append(CommandRejection(raw=raw))
        return validated

    def validateCommandFields(self, raw: RawDriverCommand) -> Optional[ValidatedCommand]:
        """!
        @brief 내부 전용(모듈 밖 호출 금지): side/action/source/timestampS 필드를 검증한다.
        @param raw 원시 명령.
        @return 유효하면 `ValidatedCommand`, 하나라도 무효/누락이면 `None`.
        """
        if (
            raw.side not in SIDE_MAP
            or raw.action not in ACTION_MAP
            or raw.source not in SOURCE_MAP
            or raw.timestampS is None
        ):
            return None
        return ValidatedCommand(
            side=SIDE_MAP[raw.side],
            action=ACTION_MAP[raw.action],
            source=SOURCE_MAP[raw.source],
            timestampS=raw.timestampS,
        )

    def getRejectionLog(self) -> Tuple[CommandRejection, ...]:
        """! @brief 거절 로그의 읽기 전용 스냅샷을 반환한다(테스트 편의, AIF-002 계약 외)."""
        return tuple(self.rejectionLog)
