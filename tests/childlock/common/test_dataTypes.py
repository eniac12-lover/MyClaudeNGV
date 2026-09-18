"""!
@brief UNIT-001 공통 DTO/열거형(`childlock.common.dataTypes`)의 불변성과 스키마를 검증한다.
"""
import dataclasses
import unittest

from childlock.common import dataTypes


class TestEnumMembers(unittest.TestCase):
    ## @brief Side 열거형이 SWD-001 §4.2가 정의한 3개 값을 그대로 갖는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning)
    # @case Positive
    def test_sideHasLeftRightAllMembers(self):
        names = {member.name for member in dataTypes.Side}
        self.assertEqual(names, {"LEFT", "RIGHT", "ALL"})

    ## @brief LockState 열거형이 LOCK/RELEASE 두 값만 갖는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning)
    # @case Positive
    def test_lockStateHasLockAndReleaseMembers(self):
        names = {member.name for member in dataTypes.LockState}
        self.assertEqual(names, {"LOCK", "RELEASE"})

    ## @brief CommandSource 열거형이 4-source를 모두 포함하는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning)
    # @case Positive
    def test_commandSourceHasFourSources(self):
        names = {member.name for member in dataTypes.CommandSource}
        self.assertEqual(
            names, {"PHYSICAL_BUTTON", "AVN", "VOICE", "MOBILE_APP"}
        )

    ## @brief SignalValidity 열거형이 NORMAL/DEGRADED/INVALID 세 값을 갖는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning)
    # @case Positive
    def test_signalValidityHasThreeLevels(self):
        names = {member.name for member in dataTypes.SignalValidity}
        self.assertEqual(names, {"NORMAL", "DEGRADED", "INVALID"})

    ## @brief SystemState 열거형이 NORMAL/DEGRADED/OFF/FAULT 네 값을 갖는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning)
    # @case Positive
    def test_systemStateHasFourStates(self):
        names = {member.name for member in dataTypes.SystemState}
        self.assertEqual(names, {"NORMAL", "DEGRADED", "OFF", "FAULT"})


class TestImmutability(unittest.TestCase):
    ## @brief RawVehicleSnapshot이 frozen dataclass라 필드 재할당 시 예외가 발생하는지 검증한다.
    # @technique 경험 기반 테스트(불변 DTO 계약 위반 시도)
    # @case Negative
    # @pre RawVehicleSnapshot 인스턴스가 생성되어 있다.
    # @post 필드 재할당 시 dataclasses.FrozenInstanceError가 발생한다.
    def test_rawVehicleSnapshotRejectsFieldMutation(self):
        snapshot = dataTypes.RawVehicleSnapshot(
            vehicleSpeedKph=None, gear=None, crashStatus=None,
            rearLeftApproachRisk=None, rearRightApproachRisk=None,
            fireDetected=None, overtemperatureDetected=None,
            adultPresent=None, isofixLeft=None, isofixRight=None,
            ignitionOn=None, sensorFault=None, sourceTimestampS=None,
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            snapshot.vehicleSpeedKph = 10.0

    ## @brief RawVehicleSnapshot을 필드 지정 없이 생성하면 전 필드가 None인지 검증한다.
    # @technique 경계값 분석(초기 안전 열화 기본값)
    # @case Positive
    # @post 모든 필드가 None으로 채워진 안전한 기본 스냅샷이 생성된다.
    def test_rawVehicleSnapshotAllFieldsDefaultToNone(self):
        snapshot = dataTypes.RawVehicleSnapshot(
            vehicleSpeedKph=None, gear=None, crashStatus=None,
            rearLeftApproachRisk=None, rearRightApproachRisk=None,
            fireDetected=None, overtemperatureDetected=None,
            adultPresent=None, isofixLeft=None, isofixRight=None,
            ignitionOn=None, sensorFault=None, sourceTimestampS=None,
        )
        values = dataclasses.astuple(snapshot)
        self.assertTrue(all(value is None for value in values))


class TestEventRecordSchema(unittest.TestCase):
    ## @brief EventRecord가 SWR-011 허용 필드 화이트리스트와 정확히 일치하는 7개 필드만 갖는지 검증한다.
    # @technique 체크리스트 기반 테스트(SWR-011 허용 필드 스키마)
    # @case Positive
    # @post dataclasses.fields(EventRecord)의 개수가 정확히 7이고 이름 집합이 허용 목록과 같다.
    def test_eventRecordHasExactlySevenAllowedFields(self):
        fieldNames = {field.name for field in dataclasses.fields(dataTypes.EventRecord)}
        self.assertEqual(len(fieldNames), 7)
        self.assertEqual(
            fieldNames,
            {
                "eventId", "timestampS", "lockLeft", "lockRight",
                "state", "reasonCode", "inputValidity",
            },
        )


class TestRuleDecisionInvariant(unittest.TestCase):
    ## @brief 좌측만 결정된 RuleDecision이 정상 생성되는지 검증한다(불변조건 충족).
    # @technique 경계값 분석(최소 한 쪽 non-None 불변조건의 경계)
    # @case Positive
    def test_ruleDecisionAllowsLeftOnlyDecision(self):
        decision = dataTypes.RuleDecision(
            left=dataTypes.LockState.LOCK, right=None,
            reasonCode="AUTO_LOCK_SPEED", priorityReason="auto_lock_active",
        )
        self.assertEqual(decision.left, dataTypes.LockState.LOCK)
        self.assertIsNone(decision.right)

    ## @brief 좌우 모두 None인 RuleDecision 생성 시도가 불변조건 위반으로 거부되는지 검증한다.
    # @technique 경계값 분석(불변조건 위반 경계)
    # @case Negative
    # @pre left, right가 모두 None으로 주어진다.
    # @post ValueError가 발생한다.
    def test_ruleDecisionRejectsBothSidesNone(self):
        with self.assertRaises(ValueError):
            dataTypes.RuleDecision(
                left=None, right=None,
                reasonCode="HOLD_LAST_OUTPUT", priorityReason="hold_last_output",
            )


class TestReasonCodeConstants(unittest.TestCase):
    ## @brief §4.4 예약된 reasonCode 리터럴 상수가 설계서와 동일한 값을 갖는지 검증한다.
    # @technique 체크리스트 기반 테스트(SWD-001 §4.4 리터럴 표)
    # @case Positive
    def test_reservedReasonCodesMatchDesignLiterals(self):
        self.assertEqual(dataTypes.REASON_IGNITION_OFF, "ignition_off")
        self.assertEqual(dataTypes.REASON_AUTO_LOCK_SPEED, "AUTO_LOCK_SPEED")
        self.assertEqual(
            dataTypes.REASON_RELEASE_BLOCKED_AUTO_LOCK, "RELEASE_BLOCKED_AUTO_LOCK"
        )
        self.assertEqual(
            dataTypes.REASON_DRIVER_COMMAND_APPLIED, "DRIVER_COMMAND_APPLIED"
        )
        self.assertEqual(dataTypes.REASON_HOLD_LAST_OUTPUT, "HOLD_LAST_OUTPUT")
        self.assertEqual(dataTypes.REASON_INVALID_COMMAND, "INVALID_COMMAND")
        self.assertEqual(dataTypes.REASON_STALE_INPUT, "STALE_INPUT")
        self.assertEqual(dataTypes.REASON_INVALID_INPUT, "INVALID_INPUT")
        self.assertEqual(dataTypes.REASON_CYCLE_ERROR, "CYCLE_ERROR")
        self.assertEqual(dataTypes.REASON_RULE_EVAL_ERROR, "RULE_EVAL_ERROR")


if __name__ == "__main__":
    unittest.main()
