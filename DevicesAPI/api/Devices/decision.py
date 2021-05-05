from .device import Device
from .status import SystemSnapshot


class DecisionBlock:
    system_snapshot = None
    devices_to_change = []
    outside_light = 0
    high_normal = []
    low_normal = []
    windows = []

    def __init__(self, snapshot: SystemSnapshot):
        self.system_snapshot = snapshot

    def analyse(self):
        outside_count = 0
        for device in self.system_snapshot.devices:
            if device.type == 2:
                self.outside_light += device.lighter
                outside_count += 1
                self.windows.append(device.copy())
            if device.type == 1:
                if device.lighter <= 25:
                    self.low_normal.append(device.copy())
                if device.lighter >= 40:
                    self.high_normal.append(device.copy())
        if outside_count > 0:
            self.outside_light /= outside_count

    def decision(self):
        if self.outside_light > 40:
            for device in self.high_normal:
                if device.lighter[0] > 20 and device.lighter[1] > 20 and device.lighter[2] > 20:
                    device.lighter = [0, 0, 0]
                    self.devices_to_change.append(device)
            for device in self.low_normal:
                if device.lighter[0] < 200 and device.lighter[1] < 200 and device.lighter[2] < 200:
                    device.lighter = [300, 300, 300]
                    self.devices_to_change.append(device)
            for device in self.windows:
                if device.light > 50:
                    if device.motor == 2:
                        device.motor = 1
                        self.devices_to_change.append(device)
                else:
                    if device.motor == 1:
                        device.motor = 2
                        self.devices_to_change.append(device)
        else:
            for device in self.high_normal:
                if device.lighter[0] > 200 and device.lighter[1] > 200 and device.lighter[2] > 200:
                    device.lighter = [100, 100, 100]
                    self.devices_to_change.append(device)
            for device in self.low_normal:
                if device.lighter[0] < 500 and device.lighter[1] < 500 and device.lighter[2] < 500:
                    device.lighter = [600, 600, 600]
                    self.devices_to_change.append(device)
            for device in self.windows:
                if device.motor == 1:
                    device.motor = 2
                    self.devices_to_change.append(device)
