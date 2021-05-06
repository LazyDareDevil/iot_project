from .device import Device
from .status import SystemSnapshot


class DecisionBlock:
    system_snapshot = None
    devices_to_change = []
    outside_light = 0
    high_normal = []
    low_normal = []
    normal = []
    windows = []
    got_data = []

    def __init__(self, snapshot: SystemSnapshot):
        self.system_snapshot = snapshot

    def analyse(self):
        outside_count = 0
        for device in self.system_snapshot.devices:
            if device.type == 2:
                self.outside_light += device.light
                outside_count += 1
                self.windows.append(device.copy())
            if device.type == 1:
                if device.light <= 80:
                    self.low_normal.append(device.copy())
                elif device.light >= 110:
                    self.high_normal.append(device.copy())
                else:
                    self.normal.append(device.copy())
        if outside_count > 0:
            self.outside_light /= outside_count

    def decision(self):
        self.devices_to_change = []
        if self.outside_light > 110:
            for device in self.high_normal:
                if device.lighter[0] > 20 and device.lighter[1] > 20 and device.lighter[2] > 20:
                    device.lighter = [0, 0, 0]
                    self.devices_to_change.append(device)
            for device in self.low_normal:
                if device.lighter[0] < 200 and device.lighter[1] < 200 and device.lighter[2] < 200:
                    device.lighter = [300, 300, 300]
                    self.devices_to_change.append(device)
            for device in self.windows:
                if device.light > 120:
                    if device.motor == 2:
                        device.motor = 1
                        self.devices_to_change.append(device)
                else:
                    if device.motor == 1:
                        device.motor = 2
                        self.devices_to_change.append(device)
        else:
            for device in self.high_normal:
                if device.lighter[0] > 300 and device.lighter[1] > 300 and device.lighter[2] > 300:
                    device.lighter = [0, 0, 0]
                    self.devices_to_change.append(device)
            for device in self.low_normal:
                if device.lighter[0] < 400 and device.lighter[1] < 400 and device.lighter[2] < 400:
                    device.lighter = [600, 600, 600]
                    self.devices_to_change.append(device)
            for device in self.windows:
                if device.motor == 1:
                    device.motor = 2
                    self.devices_to_change.append(device)
        for device in self.normal:
            if device.lighter[0] > 100 and device.lighter[1] > 100 and device.lighter[2] > 100:
                device.lighter = [0, 0, 0]
                self.devices_to_change.append(device)

    def parse_change(self):
        self.devices_to_change = []
        for device in self.system_snapshot.devices:
            for elem in self.got_data:
                if elem.uid == device.uid:
                    self.devices_to_change.append()

    def add_change(self, data):
        for element in data:
            if "uid" in element:
                device = Device(element["uid"])
                if device.type == 1:
                    if "lighter" in element:
                        lighter = element["lighter"]
                        if len(lighter) != 3:
                            return 0
                        for i in range(len(lighter)):
                            if lighter[i] > 700:
                                lighter[i] = 700
                            if lighter[i] < 0:
                                lighter[i] = 0
                        device.lighter = lighter
                        self.got_data.append(device)
                        continue
                    else:
                        return 0
                if device.type == 2:
                    if "motor" in element:
                        motor = element["motor"]
                        if motor not in [1, 2]:
                            return 0
                        device.motor = motor
                        self.got_data.append(device)
                        continue
                    else:
                        return 0
            else:
                return 0
        return 1
