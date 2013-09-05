import Settings

class Computers(Settings.Settings):
    def __init__(self):
        Settings.Settings.__init__(self)
        self.path = '../data/computer/'
        self.validator = '../data/schema/Computer.json'
