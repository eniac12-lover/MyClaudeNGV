"""!
@brief UNIT-004 출력/발행 계층 인터페이스(AIF-007/008/009/010, SWD-001 §4.5).
"""
from abc import ABC, abstractmethod
from typing import List

from childlock.common.dataTypes import (
    Ack,
    ArbitrationResult,
    ControlResultRecord,
    EventRecord,
    LockState,
    ValidityReport,
)


class IActuatorOutputSink(ABC):
    """! @brief AIF-007: 최종 결정을 외부 Actuator model 계약으로 출력하는 계약."""

    @abstractmethod
    def apply(self, left: LockState, right: LockState) -> Ack:
        """!
        @brief 좌/우 잠금 상태를 외부 채널로 출력한다.
        @param left 좌측 최종 결정.
        @param right 우측 최종 결정.
        @return `Ack`(Phase1은 항상 accepted=True).
        """


class IControlResultComposition(ABC):
    """! @brief AIF-008: 공개 제어결과 축약 계약."""

    @abstractmethod
    def compose(
        self, report: ValidityReport, result: ArbitrationResult
    ) -> ControlResultRecord:
        """!
        @brief 유효성 보고서와 판정 결과를 공개 `ControlResultRecord`로 축약한다.
        @param report 이번 평가주기의 `ValidityReport`.
        @param result 이번 평가주기의 `ArbitrationResult`.
        @return `ControlResultRecord`.
        """


class IEventHistoryRecording(ABC):
    """! @brief AIF-009: 제어결정 이력 기록 계약(SWD-001 §4.6 보완 시그니처)."""

    @abstractmethod
    def record(
        self, result: ControlResultRecord, left: LockState, right: LockState
    ) -> int:
        """!
        @brief 제어결정을 이력 저장소에 추가한다.
        @param result 공개 제어결과.
        @param left 좌측 최종 결정(SWR-011 허용 필드 lock_left).
        @param right 우측 최종 결정(SWR-011 허용 필드 lock_right).
        @return 단조 증가하는 `eventId`.
        """


class IEventHistoryQuery(ABC):
    """! @brief AIF-010: 이벤트 이력 조회 계약."""

    @abstractmethod
    def query(self, limit: int) -> List[EventRecord]:
        """!
        @brief 최신순 최대 `limit`건의 이벤트 레코드를 반환한다.
        @param limit 조회 건수 상한(0 이상).
        @return `EventRecord` 리스트(불변 스냅샷 복사본).
        @throws ValueError `limit`이 0 미만이면 발생한다.
        """
