import os
import fnmatch
import json
import fileinput
from jsonschema import validate

class Settings(object):
    def __init__(self):
        self.settingList = list()
        self.path = "."
        self.validator = ""

    def loadJson(self, absoluteFilePath):
        settingLines=[]
        for line in fileinput.input(absoluteFilePath):
            settingLines.append(line)
        return json.loads("".join(settingLines))

    def registerFromJson(self):
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        schema = self.loadJson(self.validator)
        for file in os.listdir(self.path):
            if fnmatch.fnmatch(file, '*.json'):
                absoluteFilePath = self.path + file
                inputData = self.loadJson(absoluteFilePath)
                validate(inputData,schema)
                self.settingList.append(inputData)
                #print inputData
