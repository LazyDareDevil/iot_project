import xml.etree.ElementTree as ET
import os


class SystemInfo:
    xml_path = None
    xmlTree = None
    rpi = None
    devices = None

    def __init__(self):
        cwd = os.getcwd()
        self.xml_path = os.path.join(os.path.join(os.path.join(cwd, "Devices"), "Sensitive"), "devices.xml")
        self.update_system()
        data_path = os.path.join(os.path.join(os.path.join(cwd, "Devices"), "Sensitive"), "rpi.txt")
        f = open(data_path, "r")
        tmp = f.readline()[:-1]
        rpi_uid = ""
        if tmp[:4] == "uid:":
            tmp = f.readline()[:-1]
            if tmp[0] == '0' and tmp[2] == '0':
                rpi_uid = tmp
        print(rpi_uid)
        xmlTreeRoot = self.xmlTree.getroot()
        self.rpi = xmlTreeRoot.find("RPI")    
        self.rpi.set("uid", rpi_uid)
        self.xmlTree.write(self.xml_path)

    def add_device(self, uid):
        if uid[:3] == "001" or uid[:3] == "002":
            tmp = self.devices.find("device[@uid='{}']".format(uid))
            if tmp is None:
                b = ET.SubElement(self.devices, "device")
                b.set("uid", uid)
                b.set("type", uid[2])
                self.xmlTree.write(self.xml_path)
                self.update_system()
                return 0
            else:
                return 2
        return -1

    def update_system(self):
        self.xmlTree = ET.parse(self.xml_path)
        xmlTreeRoot = self.xmlTree.getroot()
        self.devices = xmlTreeRoot.find("DEVICES") 
