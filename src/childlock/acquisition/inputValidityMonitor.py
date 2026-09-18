"""!
@brief UNIT-009 `InputValidityMonitor`(DES-003, ASIL B, SWD-001 §5.3/§6.3).

@details ASIL B 자체 목표(CCN ≤4~6)를 만족하도록 신호별 검증기를 딕셔너리로
디스패치하여 분기 사슬을 제거한다(SWD-001 §11.1).
"""
from typing import Any, Mapping

from childlock.common.dataTypes import RawVehicleSnapshot, SignalValidity, ValidityReport
from childlock.interfaces.acquisitionInterfaces import IInputValidityEvaluation

## @brief SWR-001 §5 데이터 사전이 정의한 freshness 적용 대상 12개 신호(SWD-001 §6.3 확인필요#2).
MONITORED_SIGNALS = (
    "vehicleSpeedKph", "gear", "crashStatus",
    "rearLeftApproachRisk", "rearRightApproachRisk",
    "fireDetected", "overtemperatureDetected", "adultPresent",
    "isofixLeft", "isofixRight", "ignitionOn", "sensorFault",
)
## @brief freshness 허용 한도(밀리초). 이 값 이하면 신선(SWR-013a).
FRESHNESS_LIMIT_MS = 200.0
## @brief vehicleSpeedKph 유효 범위(km/h, OEM-IF-001).
SPEED_RANGE_KPH = (0.0, 300.0)
## @brief gear 유효 열거값(OEM-IF-001).
VALID_GEAR_VALUES = {"P", "N", "D", "R"}
## @brief crashStatus 유효 열거값(OEM-IF-002).
VALID_CRASH_STATUS_VALUES = {"NONE", "PENDING", "CONFIRMED"}
## @brief 유효성 등급 우선순위(최악값 계산용, 값이 클수록 심각).
VALIDITY_SEVERITY = {
    SignalValidity.NORMAL: 0,
    SignalValidity.DEGRADED: 1,
    SignalValidity.INVALID: 2,
}


def validateSpeedRange(rawValue: Any) -> bool:
    """! @brief 내부 전용: vehicleSpeedKph가 0.0~300.0 범위의 수치인지 검증한다."""
    if isinstance(rawValue, bool) or not isinstance(rawValue, (int, float)):
        return False
    lowerBound, upperBound = SPEED_RANGE_KPH
    return lowerBound <= rawValue <= upperBound


def validateGearEnum(rawValue: Any) -> bool:
    """! @brief 내부 전용: gear가 {P,N,D,R} 중 하나인지 검증한다."""
    return rawValue in VALID_GEAR_VALUES


def validateCrashStatusEnum(rawValue: Any) -> bool:
    """! @brief 내부 전용: crashStatus가 {NONE,PENDING,CONFIRMED} 중 하나인지 검증한다."""
    return rawValue in VALID_CRASH_STATUS_VALUES


def validateBooleanSignal(rawValue: Any) -> bool:
    """! @brief 내부 전용: 신호가 순수 boolean 타입인지 검증한다."""
    return isinstance(rawValue, bool)


## @brief 신호명 → 형식 검증기 디스패치 표(SWD-001 §6.3, if-elif 사슬 제거).
SIGNAL_VALIDATORS = {
    "vehicleSpeedKph": validateSpeedRange,
    "gear": validateGearEnum,
    "crashStatus": validateCrashStatusEnum,
    "rearLeftApproachRisk": validateBooleanSignal,
    "rearRightApproachRisk": validateBooleanSignal,
    "fireDetected": validateBooleanSignal,
    "overtemperatureDetected": validateBooleanSignal,
    "adultPresent": validateBooleanSignal,
    "isofixLeft": validateBooleanSignal,
    "isofixRight": validateBooleanSignal,
    "ignitionOn": validateBooleanSignal,
    "sensorFault": validateBooleanSignal,
}


class InputValidityMonitor(IInputValidityEvaluation):
    """! @brief 대상 입력의 형식/범위/freshness를 무상태로 재검증한다(ASIL B, DES-003)."""

    def evaluate(self, snapshot: RawVehicleSnapshot, nowSeconds: float) -> ValidityReport:
        """!
        @brief 12개 대상 신호 전부에 대해 `SignalValidity`를 산출한다.
        @param snapshot 검증 대상 원시 스냅샷.
        @param nowSeconds `IClockSource.now()`의 단조 증가 값.
        @return `ValidityReport`(어떤 입력 조합에도 예외를 던지지 않음, 설계 불변).
        """
        perSignal = {}
        for signalName in MONITORED_SIGNALS:
            rawValue = getattr(snapshot, signalName)
            perSignal[signalName] = self.evaluateSingleSignal(
                signalName, rawValue, nowSeconds, snapshot.sourceTimestampS
            )
        staleNames = tuple(
            name for name, value in perSignal.items() if value == SignalValidity.DEGRADED
        )
        invalidNames = tuple(
            name for name, value in perSignal.items() if value == SignalValidity.INVALID
        )
        overall = self.computeOverallValidity(perSignal)
        return ValidityReport(perSignal, staleNames, invalidNames, overall)

    def evaluateSingleSignal(
        self, signalName: str, rawValue: Any, nowSeconds: float, sourceTimestampS
    ) -> SignalValidity:
        """! @brief 내부 전용: 신호 1개의 형식→freshness 순으로 등급을 산출한다."""
        if not self.checkSignalFormat(signalName, rawValue):
            return SignalValidity.INVALID
        if self.checkSignalFreshness(nowSeconds, sourceTimestampS):
            return SignalValidity.NORMAL
        return SignalValidity.DEGRADED

    def checkSignalFormat(self, signalName: str, rawValue: Any) -> bool:
        """!
        @brief 내부 전용(모듈 밖 호출 금지): 신호명별 검증기로 형식/범위를 판정한다.
        @param signalName 검증 대상 신호명.
        @param rawValue 검증할 원시값.
        @return 유효하면 True. 검증기 실행 중 예외가 발생해도 False로 흡수한다.
        """
        validator = SIGNAL_VALIDATORS.get(signalName)
        if validator is None:
            return False
        try:
            return bool(validator(rawValue))
        except (TypeError, ValueError):
            return False

    def checkSignalFreshness(self, nowSeconds: float, sourceTimestampS) -> bool:
        """!
        @brief 내부 전용: 스냅샷 공유 타임스탬프 기준 200ms 이내 갱신 여부를 판정한다.
        @param nowSeconds 현재 시각(초).
        @param sourceTimestampS 스냅샷의 공유 타임스탬프(초, None 허용).
        @return `sourceTimestampS`가 None이면 False, 아니면 경과시간<=200ms 여부.
        """
        if sourceTimestampS is None:
            return False
        elapsedMs = (nowSeconds - sourceTimestampS) * 1000.0
        return elapsedMs <= FRESHNESS_LIMIT_MS

    def computeOverallValidity(
        self, perSignal: Mapping[str, SignalValidity]
    ) -> SignalValidity:
        """!
        @brief 내부 전용: INVALID > DEGRADED > NORMAL 우선순위로 최악값을 반환한다.
        @param perSignal 신호별 유효성 등급(12개 키 모두 포함).
        @return 전체 중 가장 심각한 `SignalValidity`.
        """
        worst = SignalValidity.NORMAL
        for value in perSignal.values():
            if VALIDITY_SEVERITY[value] > VALIDITY_SEVERITY[worst]:
                worst = value
        return worst
