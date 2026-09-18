"""!
@brief UNIT-007 `VehicleSignalGateway`(DES-001, SWD-001 §5.1/§6.1)의 계약을 검증한다.
"""
import unittest

from childlock.acquisition.vehicleSignalGateway import VehicleSignalGateway


class TestAcquireBeforeIngest(unittest.TestCase):
    ## @brief ingest 미호출 상태에서 acquire가 전 필드 None인 안전 기본값을 반환하는지 검증한다.
    # @technique 경계값 분석(안전 열화 기본값)
    # @case Positive
    def test_returnsAllNoneSnapshotWhenNeverIngested(self):
        gateway = VehicleSignalGateway()
        snapshot = gateway.acquire()
        self.assertIsNone(snapshot.vehicleSpeedKph)
        self.assertIsNone(snapshot.ignitionOn)
        self.assertIsNone(snapshot.sourceTimestampS)


class TestIngestMapping(unittest.TestCase):
    ## @brief 전체 필드가 채워진 payload를 ingest하면 camelCase 필드로 정확히 매핑되는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning) — 정상 입력 클래스
    # @case Positive
    def test_mapsAllExternalKeysToInternalFields(self):
        gateway = VehicleSignalGateway()
        payload = {
            "vehicle_speed_kph": 12.5,
            "gear": "D",
            "source_timestamp_s": 100.0,
            "crash_status": "NONE",
            "rear_left_approach_risk": False,
            "rear_right_approach_risk": True,
            "fire_detected": False,
            "overtemperature_detected": False,
            "adult_present": True,
            "isofix_left": True,
            "isofix_right": False,
            "ignition_on": True,
            "sensor_fault": False,
        }
        gateway.ingest(payload)
        snapshot = gateway.acquire()
        self.assertEqual(snapshot.vehicleSpeedKph, 12.5)
        self.assertEqual(snapshot.gear, "D")
        self.assertEqual(snapshot.sourceTimestampS, 100.0)
        self.assertEqual(snapshot.crashStatus, "NONE")
        self.assertFalse(snapshot.rearLeftApproachRisk)
        self.assertTrue(snapshot.rearRightApproachRisk)
        self.assertTrue(snapshot.adultPresent)
        self.assertTrue(snapshot.isofixLeft)
        self.assertFalse(snapshot.isofixRight)
        self.assertTrue(snapshot.ignitionOn)
        self.assertFalse(snapshot.sensorFault)

    ## @brief 일부 키가 누락된 payload를 ingest하면 누락 필드가 None으로 채워지는지 검증한다.
    # @technique 동등분할(Equivalence Partitioning) — 누락 입력 클래스
    # @case Negative
    def test_missingKeysBecomeNone(self):
        gateway = VehicleSignalGateway()
        gateway.ingest({"vehicle_speed_kph": 5.0})
        snapshot = gateway.acquire()
        self.assertEqual(snapshot.vehicleSpeedKph, 5.0)
        self.assertIsNone(snapshot.gear)
        self.assertIsNone(snapshot.ignitionOn)

    ## @brief payload가 None이어도 예외 없이 전 필드 None 스냅샷이 생성되는지 검증한다.
    # @technique 경험 기반 테스트(널 입력 방어)
    # @case Negative
    def test_ingestAcceptsNonePayloadWithoutError(self):
        gateway = VehicleSignalGateway()
        gateway.ingest(None)
        snapshot = gateway.acquire()
        self.assertIsNone(snapshot.vehicleSpeedKph)

    ## @brief 두 번째 ingest가 첫 번째 결과를 완전히 대체(최신값만 유지)하는지 검증한다.
    # @technique 상태 전이 테스트(최신값 갱신)
    # @case Positive
    def test_secondIngestReplacesFirst(self):
        gateway = VehicleSignalGateway()
        gateway.ingest({"vehicle_speed_kph": 1.0})
        gateway.ingest({"vehicle_speed_kph": 2.0})
        self.assertEqual(gateway.acquire().vehicleSpeedKph, 2.0)


if __name__ == "__main__":
    unittest.main()
