import hashlib


class vk_user(object):
    def __init__(self, url: str):
        self.url = url
        self.times = []

        h = hashlib.md5()
        h.update(self.url.encode('utf-8'))
        self.user_file = h.hexdigest()

        self.clear_times()
        self.name = ''
        self.id = -1
        return

    def clear_times(self):
        self.times = []
        for i in range(0, 1440):
            self.times.append(0)
        return
