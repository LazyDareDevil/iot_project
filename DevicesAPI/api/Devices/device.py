from datetime import datetime


class Device:
    type = 0
    status = -1
    light = -1
    lighter = [-1, -1, -1]
    motor = -1

    def __init__(self, uid):
        self.uid = uid
        self.status = 0
        self.timestamp = datetime.timestamp(datetime.now())
        tmp = uid[:3]
        if tmp == "001":
            self.type = 1
            self.light = 0
            self.lighter = [0, 0, 0]
            self.motor = -1
        if tmp == "002":
            self.type = 2
            self.light = 0
            self.motor = 0

    def info(self):
        return [self.status, self.uid, self.light, self.lighter, self.motor]

    def change_to_inactive(self):
        self.light = -1
        self.lighter = [-1, -1, -1]
        self.motor = -1

    def change(self, status, light, lighter, motor):
        self.status = status
        if status == 1:
            self.light = light
            self.lighter = lighter
            self.motor = motor
            self.timestamp = datetime.timestamp(datetime.now())
        if status == 0:
            self.change_to_inactive()

    def to_dict(self):
        if self.type == 1:
            return {"uid": self.uid, "light": self.light, "lighter": self.lighter}
        if self.type == 2:
            return {"uid": self.uid, "light": self.light, "motor": self.motor}

    def to_dict_full(self):
        return {"uid": self.uid, "timestamp": self.timestamp,
                "light": self.light, "lighter": self.lighter, "motor": self.motor}

    def to_dict_change(self):
        if self.type == 1:
            return {"uid": self.uid, "lighter": self.lighter}
        if self.type == 2:
            return {"uid": self.uid, "motor": self.motor}

    def copy(self):
        res = Device(self.uid)
        res.type = self.type
        res.light = self.light
        res.lighter = self.lighter
        res.motor = self.motor
        res.status = 0
        return res
