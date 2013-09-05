import Settings

class Schedulers(Settings.Settings):
    def __init__(self):
        Settings.Settings.__init__(self)
        self.path = '../data/scheduler/'
        self.validator = '../data/schema/Scheduler.json'
