class Device:
    type = 0
    light = -1
    lighter = -1
    motor = -1

    def __init__(self, uid):
        self.uid = uid
        tmp = uid[:3]
        if tmp == "001":
            self.type = 1
            self.light = 0
            self.lighter = [0, 0, 0]
        if tmp == "002":
            self.type = 2
            self.light = 0
            self.motor = 0

    def status(self):
        # TODO: POST from device, last data changes info
        res = [self.uid, self.light, 0]
        if self.type == 1:
            res[2] = self.lighter
        if self.type == 2:
            res[2] = self.motor
        return res

    def change(self, light, lighter, motor):
        self.light = light
        self.lighter = lighter
        self.motor = motor

