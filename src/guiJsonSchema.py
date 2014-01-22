import json
import fileinput
from PyQt4 import QtGui

class guiJsonSchema(object):
    def __init__(self, schemaFileName):
        self.filename = schemaFileName
        self.schema = self.loadJson(self.filename)
        print self.schema
        print ''
        self.structure, self.guiStructure = self.digJson(self.schema)
        print self.structure
        print ''
        print self.guiStructure
        print self.guiStructure.printRequired()
        
    def loadJson(self, absoluteFilePath):
        settingLines=[]
        for line in fileinput.input(absoluteFilePath):
            settingLines.append(line)
        return json.loads("".join(settingLines))

    def constructGUIForm(self):
        print 'stub'

    def digJson(self,upper):
        if upper['type'] == 'object':
            return self.digJsonObject(upper)
        elif upper['type'] == 'array':
            return self.digJsonArray(upper)
        elif upper['type'] == 'string':
            return self.digJsonString(upper)

    def digJsonObject(self,upper):
        #print 'stub:ob'
        upperTemp = upper['properties']
        obdic = dict()
        obdicGui = jsonObject()
        for p in upperTemp:
            #print p
            obdicTemp,obdicGuiTemp = self.digJson(upperTemp[p])
            obdic.update({p:obdicTemp})
            obdicGui.required = upper['required']
            obdicGui.originalData.update({p:obdicGuiTemp})
            obdicGui.data.update({p:obdicGuiTemp})
        return obdic,obdicGui

    def digJsonArray(self,upper):
        #print 'stub:ar'
        upperTemp = upper['items']
        arlist = list()
        arlistGui = jsonArray()
        arlistTemp,arlistGuiTemp  = self.digJson(upperTemp)
        arlist.append(arlistTemp)
        arlistGui.originalData.append(arlistGuiTemp)
        arlistGui.data.append(arlistGuiTemp)
        arlistGui.required = upper['required']
        return arlist,arlistGui

    def digJsonString(self,upper):
        #print 'stub:st'
        stGui = jsonString()
        stGui.required = upper['required']
        return '',stGui

class jsonValue(object):
    def __init__(self):
        self.originalData = None
        self.data = None
        self.required = None
        self.createGui()
        
    def createGui(self):
        self.gui = None

    def __repr__(self):
        return self.data.__repr__()

    def printRequired(self):
        return '%s(%s)' % (self.data.__repr__(), self.required.__repr__())

class jsonObject(jsonValue):
    def __init__(self):
        self.originalData = dict()
        self.data = dict()

    def createGui(self):
        print 'stub'
        #self.gui = 

class jsonArray(jsonValue):
    def __init__(self):
        self.originalData = list()
        self.data = list()
        
    def createGui(self):
        print 'stub'
        #self.gui = 

class jsonString(jsonValue):
    def __init__(self):
        self.originalData = str()
        self.data = str()
        
    def createGui(self):
        print 'stub'
        #self.gui = 

if __name__ == '__main__':
    s = guiJsonSchema('../data/schema/User.json')
