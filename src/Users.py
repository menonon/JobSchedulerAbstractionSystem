import Settings

class Users(Settings.Settings):
    def __init__(self):
        Settings.Settings.__init__(self)
        self.path = '../data/user/'
        self.validator = '../data/schema/User.json'
