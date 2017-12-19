class Channel:
    def __init__(self, service_time):
        self._service_time = service_time  # время обслуживания
        self.N = 0  # кол-во обработанных заявок
        self._release_time = None
        self._is_empty = True
        self.queue = []

    @property
    def release_time(self):
        return self._release_time

    def get_queue_count(self):
        return len(self.queue) - 1 if len(self.queue) > 0 else 0

    def set_service_time(self, service_time):
        self._service_time = service_time

    def _get(self):
        item = self.queue.pop(0)
        return item

    def work(self, time):
        item = None
        if self.release_time == time:
            item = self._get()
            item += (self.release_time,)
            self.N += 1
            self._is_empty = True

        if self.is_empty and self.queue:
            self._is_empty = False
            self._release_time = time + self._service_time  # начинает работать в тот же момент
        return item

    @property
    def is_empty(self):
        return self._is_empty

    def add(self, item):
        self.queue.append(item)
        if self.is_empty:
            item_time = item[-1]
            self._is_empty = False
            self._release_time = item_time + self._service_time
