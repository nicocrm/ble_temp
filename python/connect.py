from bluepy.btle import UUID, Scanner, Peripheral, BTLEException
import struct

SVC_ENVIRONMENT_SENSING = UUID(0x181a)
ATTR_TEMPERATURE = UUID(0x2a6e)
LOCAL_NAME = 9


def find_device(name):
    scanner = Scanner()
    devices = scanner.scan(1.0)

    for dev in devices:
        print("Device %s (%s) %s, RSSI=%d dB" % (dev.addr, dev.addrType, dev.getValueText(LOCAL_NAME), dev.rssi))
        if dev.getValueText(LOCAL_NAME) == name:
            return dev

def read_temperature(device_address):
    try:
        print("Using address", device_address)
        p = Peripheral(device_address)
        print("Connected")
        if not p.getServices():
            return None
        svc = p.getServiceByUUID(SVC_ENVIRONMENT_SENSING)
        print("Got svc", svc.uuid)
        for char in svc.getCharacteristics(ATTR_TEMPERATURE):
            print("Got char", char.uuid)
            # print("Char %s (%d)" % (char.uuid, char.getHandle()))
            val = char.read()
            temp = struct.unpack_from("<f", val)
            return temp[0]
    except BTLEException as x:
        print("Error connecting to Bluetooth", x)
    return None

def connect(address):
    p = Peripheral(address)
    for svc in p.getServices():
        print(svc.uuid)
    svc = p.getServiceByUUID(SVC_ENVIRONMENT_SENSING)
    for char in svc.getCharacteristics(ATTR_TEMPERATURE):
        print("Char %s (%d)" % (char.uuid, char.getHandle()))
        val = char.read()
        temp = struct.unpack_from('<f', val)
        print(temp)
    # print(svc.uuid)


dev = find_device("TempBureau")
if dev:
    # connect(dev.addr)
    print(read_temperature(dev.addr))
