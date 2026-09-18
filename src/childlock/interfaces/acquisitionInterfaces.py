"""!
@brief UNIT-002 입력수집 계층 인터페이스(AIF-001/002/003, SWD-001 §4.5).

@details 입력수집 계층의 계약(ABC)만 정의한다. 구현체는 `childlock.acquisition`
패키지에 위치하며(UNIT-007~009), 이 모듈은 판단 로직을 포함하지 않는다.
"""
from abc import ABC, abstractmethod
from typing import Optional

from childlock.common.dataTypes import RawVehicleSnapshot, ValidatedCommand, ValidityReport


class IVehicleSignalAcquisition(ABC):
    """! @brief AIF-001: Vehicle 원시 신호 수집 계약."""

    @abstractmethod
    def ingest(self, payload: dict) -> None:
        """!
        @brief 외부 payload를 수신해 최신 스냅샷 상태를 갱신한다.
        @param payload 외부 snake_case 키를 갖는 원시 딕셔너리(None 허용).
        """

    @abstractmethod
    def acquire(self) -> RawVehicleSnapshot:
        """!
        @brief 가장 최근에 수집된 스냅샷을 반환한다.
        @return `RawVehicleSnapshot`. `ingest`가 호출된 적 없으면 전 필드 None.
        """


class IDriverCommandAcquisition(ABC):
    """! @brief AIF-002: 4-source 운전자 명령 수집 계약."""

    @abstractmethod
    def submit(self, payload: dict) -> None:
        """!
        @brief 외부 명령 payload를 큐에 적재한다(여러 채널 동시 호출 허용).
        @param payload 외부 snake_case 키를 갖는 원시 명령 딕셔너리.
        """

    @abstractmethod
    def acquireNext(self) -> Optional[ValidatedCommand]:
        """!
        @brief 큐에서 명령 1건을 꺼내 필드검증 후 반환한다.
        @return 유효하면 `ValidatedCommand`, 큐가 비었거나 무효하면 `None`.
        """


class IInputValidityEvaluation(ABC):
    """! @brief AIF-003: 입력 형식/범위/freshness 재검증 계약(ASIL B, DES-003)."""

    @abstractmethod
    def evaluate(
        self, snapshot: RawVehicleSnapshot, nowSeconds: float
    ) -> ValidityReport:
        """!
        @brief 대상 12개 신호의 유효성을 무상태로 재계산한다.
        @param snapshot 검증 대상 원시 스냅샷.
        @param nowSeconds `IClockSource.now()`의 단조 증가 값.
        @return `ValidityReport`. 어떤 입력 조합에도 예외를 던지지 않는다(설계 불변).
        """
