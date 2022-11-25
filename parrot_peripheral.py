import struct
import warnings

from bluepy.btle import Peripheral


class ParrotPeripheral(Peripheral):
    def set_val_int8(self, service_uuid: str, characteristic_uuid: str, value: int):
        self.getServiceByUUID(service_uuid).getCharacteristics(characteristic_uuid)[
            0
        ].write(struct.pack("B", value))

    def set_val_int16(self, service_uuid: str, characteristic_uuid: str, value: int):
        warnings.warn(struct.pack("<H", value))
        self.getServiceByUUID(service_uuid).getCharacteristics(characteristic_uuid)[
            0
        ].write(struct.pack("<H", value))

    def set_val_int32(self, service_uuid: str, characteristic_uuid: str, value: int):
        self.getServiceByUUID(service_uuid).getCharacteristics(characteristic_uuid)[
            0
        ].write(struct.pack("<I", value))

    def get_val_f32(self, service_uuid: str, characteristic_uuid: str) -> float:
        characteristics = self.getServiceByUUID(service_uuid).getCharacteristics(
            characteristic_uuid
        )
        value = characteristics[0].read()
        return float(struct.unpack("f", value)[0])

    def get_val_int(self, service_uuid: str, characteristic_uuid: str) -> int:
        characteristics = self.getServiceByUUID(service_uuid).getCharacteristics(
            characteristic_uuid
        )
        value = characteristics[0].read()
        return struct.unpack(
            "<B" if len(value) == 1 else "<H" if len(value) == 2 else "<I",
            value,
        )[0]
