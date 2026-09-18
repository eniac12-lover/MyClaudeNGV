"""!
@brief UNIT-007 `VehicleSignalGateway`(DES-001, SWD-001 §5.1/§6.1).
"""
from typing import Optional

from childlock.common.dataTypes import RawVehicleSnapshot
from childlock.interfaces.acquisitionInterfaces import IVehicleSignalAcquisition

## @brief 외부 snake_case 키 → 내부 camelCase 필드 매핑표(SWD-001 §6.1). 분기 없이 순회만 사용.
FIELD_MAP = {
    "vehicle_speed_kph": "vehicleSpeedKph",
    "gear": "gear",
    "source_timestamp_s": "sourceTimestampS",
    "crash_status": "crashStatus",
    "rear_left_approach_risk": "rearLeftApproachRisk",
    "rear_right_approach_risk": "rearRightApproachRisk",
    "fire_detected": "fireDetected",
    "overtemperature_detected": "overtemperatureDetected",
    "adult_present": "adultPresent",
    "isofix_left": "isofixLeft",
    "isofix_right": "isofixRight",
    "ignition_on": "ignitionOn",
    "sensor_fault": "sensorFault",
}


class VehicleSignalGateway(IVehicleSignalAcquisition):
    """! @brief Vehicle 원시 신호(외부 계약)를 내부 `RawVehicleSnapshot`으로 어댑팅한다."""

    def __init__(self) -> None:
        """! @brief 최신 스냅샷을 보관할 내부 상태를 초기화한다(아직 수집 없음)."""
        self.latestSnapshot: Optional[RawVehicleSnapshot] = None

    def ingest(self, payload: dict) -> None:
        """! @brief payload를 매핑해 최신 스냅샷으로 갱신한다(이전 값 폐기)."""
        self.latestSnapshot = self.mapRawPayloadToSnapshot(payload)

    def acquire(self) -> RawVehicleSnapshot:
        """!
        @brief 가장 최근 스냅샷을 반환한다.
        @return `ingest`가 1회 이상 호출됐으면 그 결과, 없으면 전 필드 None인 기본 스냅샷.
        """
        if self.latestSnapshot is None:
            return self.mapRawPayloadToSnapshot({})
        return self.latestSnapshot

    def mapRawPayloadToSnapshot(self, payload: Optional[dict]) -> RawVehicleSnapshot:
        """!
        @brief 내부 전용(모듈 밖 호출 금지): 외부 payload를 `RawVehicleSnapshot`으로 변환한다.
        @param payload 외부 snake_case 키 딕셔너리(None 허용).
        @return 누락/타입 불일치 키는 None으로 채워진 `RawVehicleSnapshot`(판단 로직 없음).
        """
        source = payload if payload is not None else {}
        values = {}
        for externalKey, internalName in FIELD_MAP.items():
            values[internalName] = source.get(externalKey)
        return RawVehicleSnapshot(**values)
