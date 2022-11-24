import time
import warnings
from typing import Optional
from enum import Enum
from parrot_peripheral import ParrotPeripheral


class Convert:
    @staticmethod
    def sunlight(raw_value: int) -> float:
        sunlight = (
            0.08640000000000001
            * (192773.17000000001 * pow(float(raw_value), -1.0606619))
            if (raw_value > 0.1)
            else 0.0
        )
        return sunlight

    @staticmethod
    def water_level(raw_value: int) -> float:
        # TODO
        return float(raw_value)

    @staticmethod
    def soil_electrical_conductivity(raw_value: int) -> float:
        # TODO: convert raw (0 - 1771) to 0 to 10 (mS/cm)
        soil_electrical_conductivity = float(raw_value)
        return soil_electrical_conductivity

    @staticmethod
    def temperature(raw_value: int) -> float:
        raw_value = float(raw_value)
        temperature = (
            0.00000003044 * pow(raw_value, 3.0)
            - 0.00008038 * pow(raw_value, 2.0)
            + raw_value * 0.1149
            - 30.449999999999999
        )
        return min(max(-10.0, temperature), 55.0)

    @staticmethod
    def soil_moisture(raw_value: int) -> float:
        float(raw_value)
        soil_moisture = 11.4293 + (
            0.0000000010698 * pow(raw_value, 4.0)
            - 0.00000152538 * pow(raw_value, 3.0)
            + 0.000866976 * pow(raw_value, 2.0)
            - 0.169422 * raw_value
        )
        soil_moisture = 100.0 * (
            0.0000045 * pow(soil_moisture, 3.0)
            - 0.00055 * pow(soil_moisture, 2.0)
            + 0.0292 * soil_moisture
            - 0.053
        )
        return min(max(0.0, soil_moisture), 100.0)


class Service(str, Enum):
    """Services UUIDs"""

    Live = "39e1FA00-84a8-11e2-afba-0002a5d5c51b"
    Clock = "39e1FD00-84a8-11e2-afba-0002a5d5c51b"
    Watering = "39e1f900-84a8-11e2-afba-0002a5d5c51b"


class Characteristic(str, Enum):
    """Characteristic UUIDs"""

    # In Live Service
    NOTIFICATIONS_TIMER = "39E1fa06-84a8-11e2-afba-0002a5d5c51b"

    SUNLIGHT = "39e1fa01-84a8-11e2-afba-0002a5d5c51b"
    SOIL_EC = "39e1fa02-84a8-11e2-afba-0002a5d5c51b"
    SOIL_TEMPERATURE = "39e1fa03-84a8-11e2-afba-0002a5d5c51b"
    AIR_TEMPERATURE = "39e1fa04-84a8-11e2-afba-0002a5d5c51b"
    SOIL_MOISTURE = "39e1fa05-84a8-11e2-afba-0002a5d5c51b"

    LED = "39e1fa07-84a8-11e2-afba-0002a5d5c51b"

    CALIBRATED_SOIL_MOISTURE = "39e1fa09-84a8-11e2-afba-0002a5d5c51b"
    CALIBRATED_AIR_TEMPERATURE = "39e1fa0a-84a8-11e2-afba-0002a5d5c51b"
    CALIBRATED_DLI = "39e1fa0b-84a8-11e2-afba-0002a5d5c51b"
    CALIBRATED_EA = "39e1fa0c-84a8-11e2-afba-0002a5d5c51b"
    CALIBRATED_ECB = "39e1fa0d-84a8-11e2-afba-0002a5d5c51b"
    CALIBRATED_EC_POROUS = "39e1fa0e-84a8-11e2-afba-0002a5d5c51b"

    # In Clock Service
    CURRENT_TIME = "39e1fd01-84a8-11e2-afba-0002a5d5c51b"

    # In Watering Service
    WAT_CMD = "39e1f906-84a8-11e2-afba-0002a5d5c51b"
    WAT_LVL = "39e1f907-84a8-11e2-afba-0002a5d5c51b"


class ParrotPot:
    def __init__(self, address="a0:14:3d:cd:c4:61"):
        self.peripheral: Optional[ParrotPeripheral] = None
        self._address = address
        self._is_live = False

    def disconnect(self):
        if self.peripheral is not None:
            self.peripheral.disconnect()
        self.peripheral = None

    def connect(self) -> bool:
        print(f"Connecting {self._address}...")
        self.peripheral = None
        for _ in range(10):
            try:
                self.peripheral = ParrotPeripheral(self._address)
                break
            except Exception as e:
                print(str(e))
                time.sleep(0.5)
                self.peripheral = None
        print("Connected!")
        return self.is_connected

    @property
    def is_connected(self) -> bool:
        return self.peripheral is not None

    @property
    def live(self) -> bool:
        return self._is_live

    @live.setter
    def live(self, value: bool):
        self.set_val_int8(Service.Live, Characteristic.NOTIFICATIONS_TIMER, value)
        self._is_live = value

    @property
    def current_time(self) -> int:
        return self.get_val_int(Service.Clock, Characteristic.CURRENT_TIME)

    @property
    def air_temperature(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.AIR_TEMPERATURE)
        return Convert.temperature(val)

    @property
    def soil_temperature(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.SOIL_TEMPERATURE)
        return Convert.temperature(val)

    @property
    def soil_electrical_conductivity(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.SOIL_EC)
        return Convert.soil_electrical_conductivity(val)

    @property
    def soil_moisture(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.SOIL_MOISTURE)
        return Convert.soil_moisture(val)

    @property
    def sunlight(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.SUNLIGHT)
        return Convert.sunlight(val)

    @property
    def calibrated_dli(self) -> float:
        return 1e3 * self.get_val_f32(Service.Live, Characteristic.CALIBRATED_DLI)

    @property
    def calibrated_soil_moisture(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.CALIBRATED_SOIL_MOISTURE)

    @property
    def calibrated_air_temperature(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.CALIBRATED_AIR_TEMPERATURE)

    @property
    def calibrated_ea(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.CALIBRATED_EA)

    @property
    def calibrated_ecb(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.CALIBRATED_ECB)

    @property
    def calibrated_ec_porous(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.CALIBRATED_EC_POROUS)

    @property
    def water_level(self) -> float:
        val = self.get_val_int(Service.Watering, Characteristic.WAT_LVL)
        return Convert.water_level(val)

    def led(self, state=1):
        self.set_val_int8(Service.Live, Characteristic.LED, state)

    def water(self, seconds: int):
        if seconds > 20:
            warnings.warn("Watering is limited to 20 seconds")
            seconds = 20
        self.set_val_int16(Service.Watering, Characteristic.WAT_LVL, seconds)

    def set_val_int8(self, service: Service, characteristic: Characteristic, value: int):
        self.peripheral.set_val_int8(service.value, characteristic.value, value)

    def set_val_int16(self, service: Service, characteristic: Characteristic, value: int):
        self.peripheral.set_val_int16(service.value, characteristic.value, value)

    def set_val_int32(self, service: Service, characteristic: Characteristic, value: int):
        self.peripheral.set_val_int32(service.value, characteristic.value, value)

    def get_val_f32(self, service: Service, characteristic: Characteristic) -> float:
        return self.peripheral.get_val_f32(service.value, characteristic.value)

    def get_val_int(self, service: Service, characteristic: Characteristic) -> int:
        return self.peripheral.get_val_int(service.value, characteristic.value)