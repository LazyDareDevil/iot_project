import xml.etree.ElementTree as ET
import os


class SystemInfo:

    def __init__(self):
        cwd = os.getcwd()
        self.xml_path = os.path.join(os.path.join(os.path.join(cwd, "Devices"), "Sensitive"), "devices.xml")
        self.xmlTree = ET.parse(self.xml_path)
        self.xmlTreeRoot = self.xmlTree.getroot()
        rpi = self.xmlTreeRoot.find("RPI")
        self.devices = self.xmlTreeRoot.find("DEVICES")
        data_path = os.path.join(os.path.join(os.path.join(cwd, "Devices"), "Sensitive"), "rpi.txt")
        f = open(data_path, "r")
        tmp = f.readline()[:-1]
        if tmp == "uid:":
            tmp = f.readline()[:-1]
            if tmp[:3] == "010":
                rpi.set("uid", tmp)
        self.xmlTree.write(self.xml_path)

    def add_device(self, uid):
        if uid[:3] == "001" or uid[:3] == "002":
            tmp = self.devices.find("device[@uid='{}']".format(uid))
            if tmp is None:
                b = ET.SubElement(self.devices, "device")
                b.set("uid", uid)
                b.set("type", uid[2])
                self.xmlTree.write(self.xml_path)
                return 1
        return 0
