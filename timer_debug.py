import time


class TimerDebug:
    def __init__(self):
        self.current_time = 0
        self.last_time = 0
        self.f = open('test.txt', 'a+')

    def get_current_time(self):
        return self.current_time

    def get_last_time(self):
        return self.last_time

    def set_current_time(self):
        self.current_time = time.time()

    def set_last_time(self):
        self.last_time = time.time()

    def diff(self):
        return self.current_time-self.last_time

    def wtf(self, txt):
        f = open('test.txt', 'a+')
        f.write(txt)
        f.close()

