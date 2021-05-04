import xml.etree.ElementTree as ET
import os
from .device import Device
from .system import SystemInfo


class SystemShapshot:
    rpi = None
    devices = []
    system_info = None

    def __init__(self, sys_info: SystemInfo):
        self.system_info = sys_info
        self.update_system()

    def update_system(self):
        self.system_info.update_system()
        if "uid" in self.system_info.rpi.attrib:
            self.rpi = self.system_info.rpi.attrib["uid"]
        else:
            print("Add info about rpi indo devices.xml")
        for dev in self.system_info.devices:
            if "uid" in dev:
                uid = dev.attrib["uid"]
                is_exist = False
                for device in self.devices:
                    if device.uid == uid:
                        is_exist = True
                        break
                if not is_exist:
                    self.devices.append(Device(uid))
            else:
                print("Incorrect data in devices.xml")

    def to_dict(self):
        res = {"rpi": self.rpi, "devices": []}
        for device in self.devices:
            res["devices"].append(device.to_dict())
