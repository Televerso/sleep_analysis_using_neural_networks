class SleepTime:
    def __init__(self, hour, minute, second):
        self.hour = int(hour)
        self.minute = int(minute)
        self.second = int(second)

        self.in_seconds = int(second + minute*60 + hour*3600)

    def __add__(self, other):
        hour, minute, second, in_seconds = 0,0,0,0
        if type(other) is SleepTime:
            hour = (other.hour + self.hour) % 24
            minute = (other.minute + self.minute) % 60
            second = (other.second + self.second) % 60

        elif type(other) is int or type(other) is float:
            in_seconds = (other + self.in_seconds) % (3600*24)

            hour = (in_seconds // 3600) % 24
            minute = (in_seconds // 60) % 60
            second = (in_seconds % 3600) % 60
        else:
            assert "Wrong datatype!"

        return SleepTime(hour, minute, second)

    def __sub__(self, other):
        hour, minute, second, in_seconds = 0,0,0,0
        if type(other) is SleepTime:
            in_seconds = self.in_seconds - other.in_seconds

            hour = (in_seconds // 3600) % 24
            minute = (in_seconds // 60) % 60
            second = (in_seconds % 3600) % 60

        elif type(other) is int or type(other) is float:
            in_seconds = (self.in_seconds - other) % (3600*24)

            hour = (in_seconds // 3600) % 24
            minute = (in_seconds // 60) % 60
            second = (in_seconds % 3600) % 60
        else:
            assert "Wrong datatype!"

        return SleepTime(hour, minute, second)

    def __str__(self):
        res_str = ''
        res_str += str(self.hour)
        res_str += ':'
        res_str += str(self.minute)
        res_str += ':'
        res_str += str(self.second)

        return res_str

    def to_struct_time(self):
        pass