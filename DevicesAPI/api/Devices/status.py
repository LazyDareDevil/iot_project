import xml.etree.ElementTree as ET
import os
from .device import Device


class SystemShapshot:
    rpi = None
    devices = []

    def update_info(self):
        cwd = os.getcwd()
        xml_path = os.path.join(os.path.join(os.path.join(cwd, "Devices"), "Sensitive"), "devices.xml")
        xmlTree = ET.parse(xml_path)
        xmlTreeRoot = xmlTree.getroot()
        rpi_elem = xmlTreeRoot.find("RPI")
        devices_elem = xmlTreeRoot.find("DEVICES")
        self.rpi = rpi_elem.get("uid")
        for element in devices_elem.iter('device'):
            self.devices.append(Device(element.get("uid")))

