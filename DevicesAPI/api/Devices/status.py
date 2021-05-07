import xml.etree.ElementTree as ET
import os
from .device import Device
from .system import SystemInfo


class SystemSnapshot:
    rpi = None
    devices = []
    system_info = None
    auto_decision = True

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
            if "uid" in dev.attrib:
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

    def update_info(self, data: dict):
        uid = data["uid"]
        elem = None
        for element in self.devices:
            if element.uid == uid:
                elem = element
                element.change(1, data["light"], data["lighter"], data["motor"])
        return elem

    def to_dict(self):
        res = {"rpi": self.rpi, "devices": []}
        if self.auto_decision:
            res["auto"] = 1
        else:
            res["auto"] = 2
        for device in self.devices:
            res["devices"].append(device.to_dict_full())
        return res
