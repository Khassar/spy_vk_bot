from datetime import datetime


class timeout_helper(object):
    def __init__(self, process_time_out: int):
        self.process_time_out = process_time_out
        self.last_process_time = datetime.now()

    def will_process(self) -> bool:
        cur = datetime.now()

        dif = cur - self.last_process_time

        if dif.seconds < self.process_time_out:
            return False

        self.last_process_time = cur
        return True

    def force_update(self):
        self.last_process_time=datetime.now()
        return
