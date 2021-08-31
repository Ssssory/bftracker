class Status():
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    READY = "READY"
    COMPLETE = "COMPLETE"
    CANCELED = "CANCELED"
    CANCELED_TIMEOUT = "CANCELED_TIMEOUT"
    TEST = "TEST"
    ARCHIVED = "ARCHIVED"
    def as_json(self):
        return dict(
            NEW=self.NEW,
            IN_PROGRESS=self.IN_PROGRESS,
            READY=self.READY,
            COMPLETE=self.COMPLETE,
            CANCELED=self.CANCELED,
            CANCELED_TIMEOUT=self.CANCELED_TIMEOUT,
            TEST=self.TEST,
            ARCHIVED=self.ARCHIVED)
