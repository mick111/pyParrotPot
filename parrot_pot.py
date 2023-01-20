import time
import warnings
from typing import Optional
from parrot_peripheral import ParrotPeripheral
from parrot_uuid import Service, Characteristic


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
        warnings.warn(f"Connecting {self._address}...")
        self.peripheral = None
        for _ in range(10):
            try:
                self.peripheral = ParrotPeripheral(self._address)
                break
            except Exception as e:
                warnings.warn(str(e))
                time.sleep(0.5)
                self.peripheral = None
        warnings.warn("Connected!")
        return self.is_connected

    def connect_if_needed(self) -> bool:
        if not self.is_connected:
            return self.connect()
        return self.is_connected

    @property
    def is_connected(self) -> bool:
        return self.peripheral is not None

    @property
    def live(self) -> bool:
        return self._is_live

    @live.setter
    def live(self, value: bool):
        self.set_val_int8(Service.Live, Characteristic.notifications_timer, value)
        self._is_live = value

    @property
    def current_time(self) -> int:
        return self.get_val_int(Service.Clock, Characteristic.time_start)

    @property
    def air_temperature(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.air_temperature)
        return Convert.temperature(val)

    @property
    def soil_temperature(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.soil_temperature)
        return Convert.temperature(val)

    @property
    def soil_electrical_conductivity(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.soil_ec)
        return Convert.soil_electrical_conductivity(val)

    @property
    def soil_moisture(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.soil_moisture)
        return Convert.soil_moisture(val)

    @property
    def sunlight(self) -> float:
        val = self.get_val_int(Service.Live, Characteristic.sunlight)
        return Convert.sunlight(val)

    @property
    def calibrated_dli(self) -> float:
        return 1e3 * self.get_val_f32(Service.Live, Characteristic.calibrated_dli)

    @property
    def calibrated_soil_moisture(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.calibrated_soil_moisture)

    @property
    def calibrated_air_temperature(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.calibrated_air_temperature)

    @property
    def calibrated_ea(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.calibrated_ea)

    @property
    def calibrated_ecb(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.calibrated_ecb)

    @property
    def calibrated_ec_porous(self) -> float:
        return self.get_val_f32(Service.Live, Characteristic.calibrated_ec_porous)

    @property
    def water_level(self) -> float:
        val = self.get_val_int(Service.Watering, Characteristic.wat_lvl)
        return Convert.water_level(val)

    def led(self, state=1):
        self.set_val_int8(Service.Live, Characteristic.led, state)

    def water(self, seconds: int):
        if seconds > 20:
            warnings.warn("Watering is limited to 20 seconds")
            seconds = 20
        self.set_val_int16(Service.Watering, Characteristic.wat_cmd, seconds)

    def set_val_int8(
        self, service: Service, characteristic: Characteristic, value: int
    ):
        self.connect_if_needed()
        self.peripheral.set_val_int8(service.value, characteristic.value, value)

    def set_val_int16(
        self, service: Service, characteristic: Characteristic, value: int
    ):
        self.connect_if_needed()
        self.peripheral.set_val_int16(service.value, characteristic.value, value)

    def set_val_int32(
        self, service: Service, characteristic: Characteristic, value: int
    ):
        self.connect_if_needed()
        self.peripheral.set_val_int32(service.value, characteristic.value, value)

    def get_val_f32(self, service: Service, characteristic: Characteristic) -> float:
        self.connect_if_needed()
        return self.peripheral.get_val_f32(service.value, characteristic.value)

    def get_val_int(self, service: Service, characteristic: Characteristic) -> int:
        self.connect_if_needed()
        return self.peripheral.get_val_int(service.value, characteristic.value)
