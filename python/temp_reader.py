from bluepy.btle import BTLEException, UUID, Scanner, Peripheral
import struct

SVC_ENVIRONMENT_SENSING = UUID(0x181A)
ATTR_TEMPERATURE = UUID(0x2A6E)
LOCAL_NAME = 9


class TempReader:
    def __init__(self, device_name):
        self.p = None
        self.temp_char = None
        self.device_name = device_name

    def _connect(self):
        addr = find_device(self.device_name)
        if addr:
            self.p = Peripheral(addr)
            print("Connected")
            self.temp_char = self.p.getCharacteristics(uuid=ATTR_TEMPERATURE)[0]
            return True

    def read_temperature(self):
        try:
            if not self.p:
                if not self._connect():
                    return None
            print("Connected to", self.p.addr)
            val = self.temp_char.read()
            temp = struct.unpack_from("<f", val)
            return temp[0]
        except BTLEException as x:
            print("BL Error: ", x)
            if self.p:
                self.p.disconnect()
                self.p = None
            return None


def find_device(name):
    scanner = Scanner()
    devices = scanner.scan(1.0)

    for dev in devices:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        if dev.getValueText(LOCAL_NAME) == name:
            return dev.addr


# def read_temperature(device_address):
#     try:
#         print("Using address", device_address)
#         p = Peripheral(device_address)
#         print("Connected")
#         p.getServices()  # needed for next call
#         svc = p.getServiceByUUID(SVC_ENVIRONMENT_SENSING)
#         print("Got svc", svc.uuid)
#         for char in svc.getCharacteristics(ATTR_TEMPERATURE):
#             print("Got char", char.uuid)
#             # print("Char %s (%d)" % (char.uuid, char.getHandle()))
#             val = char.read()
#             temp = struct.unpack_from("<f", val)
#             return temp[0]
#     except BTLEException as x:
#         print("Error connecting to Bluetooth", x)
#     finally:
#         try:
#             p.disconnect()
#         except Exception:
#             pass
#     return None
