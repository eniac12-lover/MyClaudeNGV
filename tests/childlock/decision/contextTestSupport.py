"""!
@brief 규칙/오케스트레이터 테스트 전용 `RuleEvaluationContext` 빌더(프로덕션 코드 아님).

@details 여러 테스트 파일이 동일한 컨텍스트 조립 로직을 반복하면 8줄 이상의 중복
코드가 될 수 있으므로(CLAUDE.md 중복 7라인 기준), 이 모듈로 한 번만 정의해
재사용한다(writing-good-tests.md "테스트에만 필요한 정리 코드는 테스트
유틸리티에 둔다" 원칙).
"""
from childlock.acquisition.inputValidityMonitor import MONITORED_SIGNALS
from childlock.common.dataTypes import (
    PreviousOutputSnapshot,
    RawVehicleSnapshot,
    RuleEvaluationContext,
    SignalValidity,
    SystemState,
    ValidityReport,
    LockState,
)


def buildContext(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    speed=None, speedValidity=SignalValidity.NORMAL,
    ignitionOn=None, ignitionValidity=SignalValidity.NORMAL,
    command=None,
    previousLeft=LockState.RELEASE, previousRight=LockState.RELEASE,
    previousSystemState=SystemState.NORMAL,
    nowSeconds=0.0, ruleState=None,
):
    """!
    @brief 테스트용 `RuleEvaluationContext`를 조립한다(모든 인자는 선택, 안전 기본값 제공).

    @details 규칙 테스트마다 필요한 속성 몇 개만 재정의할 수 있도록 다수의 선택적
    키워드 인자를 노출한다(테스트 가독성을 위한 의도적 설계, too-many-arguments 비활성화).
    """
    snapshot = RawVehicleSnapshot(
        vehicleSpeedKph=speed, gear=None, crashStatus=None,
        rearLeftApproachRisk=None, rearRightApproachRisk=None,
        fireDetected=None, overtemperatureDetected=None, adultPresent=None,
        isofixLeft=None, isofixRight=None, ignitionOn=ignitionOn,
        sensorFault=None, sourceTimestampS=0.0,
    )
    perSignal = {name: SignalValidity.NORMAL for name in MONITORED_SIGNALS}
    perSignal["vehicleSpeedKph"] = speedValidity
    perSignal["ignitionOn"] = ignitionValidity
    report = ValidityReport(perSignal, (), (), SignalValidity.NORMAL)
    previous = PreviousOutputSnapshot(previousLeft, previousRight, previousSystemState)
    return RuleEvaluationContext(snapshot, report, command, previous, nowSeconds, ruleState)
