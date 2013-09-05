import Settings

class Applications(Settings.Settings):
    def __init__(self):
        Settings.Settings.__init__(self)
        self.path = '../data/application/'
        self.validator = '../data/schema/Application.json'
