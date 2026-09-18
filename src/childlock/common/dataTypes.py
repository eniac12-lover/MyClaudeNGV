"""!
@brief UNIT-001 공통 DTO/열거형 모듈(SWD-001 §4).

@details 전 컴포넌트가 공유하는 불변 데이터 구조와 열거형만 정의한다(판단 로직 없음,
DES 무관 공통 모듈). 모든 DTO는 `@dataclass(frozen=True)`로 선언해 불변성을 강제한다
(SWD-001 §4.3). `RuleEvaluationContext.ruleState` 필드는 순환 임포트를 피하기 위해
`childlock.interfaces.decisionInterfaces.IRuleStateStore`를 임포트하지 않고 문자열
전방참조(forward reference)로만 타입을 표기한다(SWD-001 §2.1 순환 임포트 방지 원칙 승계).
"""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Mapping, Optional, Tuple


class Side(Enum):
    """! @brief 명령/출력의 대상 side(OEM-IF-004 left/right/all과 매핑, SWD-001 §4.2)."""

    LEFT = auto()
    RIGHT = auto()
    ALL = auto()


class LockState(Enum):
    """! @brief 잠금 상태(OEM-IF-004 lock/unlock, OEM-IF-005 LOCK/RELEASE와 매핑)."""

    LOCK = auto()
    RELEASE = auto()


class CommandSource(Enum):
    """! @brief 4-source 명령 출처(OEM-IF-004 source 값과 매핑)."""

    PHYSICAL_BUTTON = auto()
    AVN = auto()
    VOICE = auto()
    MOBILE_APP = auto()


class SignalValidity(Enum):
    """! @brief 신호 유효성 등급. 우선순위(최악값): INVALID > DEGRADED > NORMAL."""

    NORMAL = auto()
    DEGRADED = auto()
    INVALID = auto()


class SystemState(Enum):
    """!
    @brief 시스템 상태. FAULT는 Phase2(SensorFaultHoldRule) 로직이 채워지기 전까지
    Phase1에서는 결코 산출되지 않는다(스텁이 항상 None을 반환하므로).
    """

    NORMAL = auto()
    DEGRADED = auto()
    OFF = auto()
    FAULT = auto()


## @brief SWR-020 수용기준의 리터럴 reasonCode 값(ignition-off로 인한 강제 해제).
REASON_IGNITION_OFF = "ignition_off"
## @brief SWR-003 수용기준의 리터럴 reasonCode 값(자동 잠금 활성).
REASON_AUTO_LOCK_SPEED = "AUTO_LOCK_SPEED"
## @brief SWR-004 수용기준의 리터럴 reasonCode 값(자동 잠금 중 해제 차단).
REASON_RELEASE_BLOCKED_AUTO_LOCK = "RELEASE_BLOCKED_AUTO_LOCK"
## @brief 유효 운전자 명령 적용 시 reasonCode(SWD-001 §4.4 신설).
REASON_DRIVER_COMMAND_APPLIED = "DRIVER_COMMAND_APPLIED"
## @brief 상위 규칙 미결정으로 직전 출력을 유지할 때의 reasonCode(SWD-001 §4.4 신설).
REASON_HOLD_LAST_OUTPUT = "HOLD_LAST_OUTPUT"
## @brief SWR-001 수용기준의 리터럴 reasonCode 값(명령 필드 유효성 실패).
REASON_INVALID_COMMAND = "INVALID_COMMAND"
## @brief SWR-013a 수용기준의 리터럴 reasonCode 값(대상 입력 freshness 상실).
REASON_STALE_INPUT = "STALE_INPUT"
## @brief SWR-013b 취지를 반영한 reasonCode 값(대상 입력 형식/범위 오류).
REASON_INVALID_INPUT = "INVALID_INPUT"
## @brief 평가주기 파이프라인 내부 예외로 인한 안전 열화 reasonCode(AIF-015 구체화).
REASON_CYCLE_ERROR = "CYCLE_ERROR"
## @brief 개별 규칙 평가 중 예외(진단 전용) reasonCode(AIF-004 구체화).
REASON_RULE_EVAL_ERROR = "RULE_EVAL_ERROR"


@dataclass(frozen=True)
class RawVehicleSnapshot:  # pylint: disable=too-many-instance-attributes
    """!
    @brief Vehicle 원시 신호를 그대로 보관하는 불변 스냅샷(형식 정규화/판단 금지).

    @details OEM-IF-001/002/003/007/008/009 신호 13개를 원시값 그대로 보관한다
    (DES-003 형식/범위 판단 책임과 분리). 13개 필드는 SWD-001 §4.3이 정의한
    데이터 사전 그대로이며, 필드 수 자체가 설계 계약이므로 too-many-instance-attributes
    경고를 임의 리팩터링으로 회피하지 않고 명시적으로 허용한다.
    """

    ## @brief OEM-IF-001, km/h, 유효범위 0.0~300.0(SWR-003/013a/013b 소비).
    vehicleSpeedKph: Optional[float]
    ## @brief OEM-IF-001, {P,N,D,R}. Phase1 미소비(계약만 반영, SWR-001 문서 8.2절).
    gear: Optional[str]
    ## @brief OEM-IF-002, {NONE,PENDING,CONFIRMED}. Phase1은 freshness/형식 계약만 소비.
    crashStatus: Optional[str]
    ## @brief OEM-IF-003, boolean. Phase1은 freshness/형식 계약만 소비.
    rearLeftApproachRisk: Optional[bool]
    ## @brief OEM-IF-003, boolean. Phase1은 freshness/형식 계약만 소비.
    rearRightApproachRisk: Optional[bool]
    ## @brief OEM-IF-007, boolean. Phase1은 freshness/형식 계약만 소비.
    fireDetected: Optional[bool]
    ## @brief OEM-IF-007, boolean. Phase1은 freshness/형식 계약만 소비.
    overtemperatureDetected: Optional[bool]
    ## @brief OEM-IF-007, boolean. Phase1은 freshness/형식 계약만 소비.
    adultPresent: Optional[bool]
    ## @brief OEM-IF-008, boolean. Phase1은 freshness/형식 계약만 소비.
    isofixLeft: Optional[bool]
    ## @brief OEM-IF-008, boolean. Phase1은 freshness/형식 계약만 소비.
    isofixRight: Optional[bool]
    ## @brief OEM-IF-009, boolean. SWR-020(ignition-off 강제 해제)이 직접 소비.
    ignitionOn: Optional[bool]
    ## @brief OEM-IF-009, boolean. Phase1은 freshness/형식 계약만 소비(OEM-SR-004 Phase2).
    sensorFault: Optional[bool]
    ## @brief 스냅샷 단일 공유 타임스탬프(초). 12개 신호의 freshness 판정 기준(SWD-001 §6.3).
    sourceTimestampS: Optional[float]


@dataclass(frozen=True)
class ValidityReport:
    """! @brief `InputValidityMonitor.evaluate()`의 반환 타입(AIF-003)."""

    perSignal: Mapping[str, SignalValidity]
    staleSignalNames: Tuple[str, ...]
    invalidSignalNames: Tuple[str, ...]
    overallValidity: SignalValidity


@dataclass(frozen=True)
class RawDriverCommand:
    """! @brief 검증 전 운전자 명령 원시 문자열(DriverCommandGateway 내부 큐 항목)."""

    side: Optional[str]
    action: Optional[str]
    source: Optional[str]
    timestampS: Optional[float]


@dataclass(frozen=True)
class ValidatedCommand:
    """! @brief 필드검증(§6.2)을 통과한 명령. 생성자 호출 자체가 유효성의 증거다."""

    side: Side
    action: LockState
    source: CommandSource
    timestampS: float


@dataclass(frozen=True)
class CommandRejection:
    """! @brief 필드검증 실패로 거절된 명령 진단 레코드(AIF-002 오류 처리)."""

    raw: RawDriverCommand
    reasonCode: str = REASON_INVALID_COMMAND


@dataclass(frozen=True)
class PreviousOutputSnapshot:
    """! @brief `IOutputStateAccess.getPrevious()`의 반환 타입(AIF-006)."""

    leftState: LockState
    rightState: LockState
    systemState: SystemState


@dataclass(frozen=True)
class RuleDecision:
    """!
    @brief 개별 `IPriorityRule.evaluate()`가 산출하는 결정.

    @throws ValueError left, right가 모두 None이면 발생한다(SWD-001 §4.3 불변조건:
    "완전 무관"은 evaluate()가 None 자체를 반환해야 하며, RuleDecision 인스턴스를
    반환할 때는 최소 한 쪽이 non-None이어야 한다).
    """

    left: Optional[LockState]
    right: Optional[LockState]
    reasonCode: str
    priorityReason: str

    def __post_init__(self) -> None:
        """! @brief 불변조건(최소 한 쪽 non-None)을 검증한다."""
        if self.left is None and self.right is None:
            raise ValueError("RuleDecision requires at least one non-None side")


@dataclass(frozen=True)
class ArbitrationResult:
    """! @brief `ArbitrationOrchestrator.decide()`의 반환 타입(AIF-004). 항상 확정값."""

    left: LockState
    right: LockState
    winningRuleLeft: str
    winningRuleRight: str
    reasonCode: str
    priorityReason: str


@dataclass(frozen=True)
class ControlResultRecord:
    """! @brief 공개 제어결과(OEM-IF-006 데이터 계약과 필드 의미 1:1)."""

    state: SystemState
    priorityReason: str
    reasonCode: str
    inputValidity: SignalValidity


@dataclass(frozen=True)
class EventRecord:
    """! @brief 이벤트 이력 레코드. SWR-011 허용 필드 화이트리스트와 정확히 일치(7개)."""

    eventId: int
    timestampS: float
    lockLeft: LockState
    lockRight: LockState
    state: SystemState
    reasonCode: str
    inputValidity: SignalValidity


@dataclass(frozen=True)
class CycleResult:
    """! @brief `IEvaluationCycleControl.runCycle()`의 반환 타입(AIF-015)."""

    timestampSeconds: float
    controlResult: ControlResultRecord
    eventId: int


@dataclass(frozen=True)
class Ack:
    """! @brief `IActuatorOutputSink.apply()`의 반환 타입. Phase1은 항상 accepted=True."""

    accepted: bool = True


@dataclass(frozen=True)
class RuleEvaluationContext:
    """!
    @brief 모든 규칙에 동일 인스턴스로 전달되는 불변 평가 컨텍스트.

    @details `ruleState` 필드는 `childlock.interfaces.decisionInterfaces.IRuleStateStore`
    타입이나, 순환 임포트를 피하기 위해 문자열 전방참조로만 표기한다(런타임에는 임포트하지
    않음 — 파일 상단 모듈 설명 참고).
    """

    validatedSnapshot: RawVehicleSnapshot
    validityReport: ValidityReport
    command: Optional[ValidatedCommand]
    previousOutput: PreviousOutputSnapshot
    nowSeconds: float
    ruleState: "IRuleStateStore"
