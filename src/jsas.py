import sys
import argparse
from Applications import Applications
from Computers import Computers
from Schedulers import Schedulers
from Users import Users

class jsas(object):
    def __init__(self):
        self.settings = {'apps':Applications(),
                         'cmps':Computers(),
                         'schs':Schedulers(),
                         'usrs':Users()
        }
        for sets in self.settings:
            self.settings[sets].registerFromJson()
        
        parser = argparse.ArgumentParser(description='JSAS Arguments')
        
        usrsTemp = self.settings['usrs'].settingList
        usrsNames = list()
        for u in usrsTemp:
            usrsNames.append(u['userName'])
        parser.add_argument('-U','--User', action='store', choices=usrsNames, required=True, help='User Name. You need to prepare data/user/yourname.json.')
        
        cmpsTemp = self.settings['cmps'].settingList
        cmpsNames = list()
        for c in cmpsTemp:
            cmpsNames.append(c['system'])
        parser.add_argument('-C','--Computer', action='store', choices=cmpsNames, required=True, help='Computer Name. You need to prepare data/computer/yourcomputer.json.')

        appsTemp = self.settings['apps'].settingList
        appsNames = list()
        for a in appsTemp:
            appsNames.append(a['name'])
        parser.add_argument('-A','--Application', action='store', choices=appsNames, required=True, help='Application Name. You need to preapare data/application/yourapplication.json')
        
        parser.add_argument('-t','--threads', action='store', default='1',help='Number of threads per process. Usually this parameter is passed to OMP_NUM_THREADS(OpenMP).')
        parser.add_argument('-p','--processes', action='store', default='1',help='Number of processes per node. Usually this parameter is passed to Job Scheduler or MPI.')
        parser.add_argument('-n','--nodes', action='store', default='1', help='Number of nodes. Usually this parameter is passed to Job Scheduler or MPI.')
        parser.add_argument('-e','--elapse', action='store', default='1', help='Elapse time. Following formats are accepted. hh:mm:ss, mm:ss, ss .')
        parser.add_argument('-q','--queue', action='store', required=True, help='Queue.')
        parser.add_argument('-g','--group', action='store',help='Group.')
        parser.add_argument('-m','--memories', action='store',default='1',help='Memories. Unit is GB.')
        
        parser.add_argument('-a','--AA','--ApplicationArguments', action='store', nargs='*', required=False, default={}, help='Application Arguments.')
        parser.add_argument('-o','--outfile', action='store', help='outfile name.')
        parser.add_argument('--no-mpi', action='store_true',default=False, help='turn mpi off.')
        parser.add_argument('--no-openmp', action='store_true',default=False, help='turn openmp off.')
   
        self.parsedOptions = vars(parser.parse_args())
        self.parsedOptions['AA'] = tuple(self.parsedOptions['AA'])
        #print self.parsedOptions

        self.allOptions = {}
        self.allOptions.update(self.parsedOptions)
        
        for u in usrsTemp:
            if u['userName'] == self.allOptions['User']:
                tempDict = {'User' : u}
                self.allOptions.update(tempDict)
        
        
        for c in cmpsTemp:
            if c['system'] == self.allOptions['Computer']:
                for cc in self.allOptions['User']['properties']:
                    if cc['computerName'] == c['system']:
                        tempDict = {'Computer' : c}
                        self.allOptions.update(tempDict)
        if isinstance(self.allOptions['Computer'], str):
            print 'You can\'t use %s computer !' % (self.allOptions['Computer'])
            sys.exit(1)

        for a in appsTemp:
            if a['name'] == self.allOptions['Application']:
                for aa in self.allOptions['User']['properties']:
                    if aa['computerName'] == self.allOptions['Computer']['system']:
                        for aaa in aa['applications']:
                            if aaa == a['name']:
                                tempDict = {'Application' : a}
                                self.allOptions.update(tempDict)
        if isinstance(self.allOptions['Application'],str):
            print 'You can\'t use %s application !' % (self.allOptions['Application'])

        schsTemp = self.settings['schs'].settingList
        for s in schsTemp:
            if s['jobScheduler'] == self.allOptions['Computer']['jobScheduler']:
                tempDict = {'Scheduler' : s}
                self.allOptions.update(tempDict)
        if isinstance(self.allOptions['Scheduler'],str):
            print 'No setting for %s scheduler !' % (self.allOptions['Scheduler'])
        
        #print ''
        #print self.allOptions
        #print ''
    
    def printJobScript(self):
        if not hasattr(self, 'allOptions'):
            sys.exit(1)
        if not hasattr(self, 'optionsChecked'):
            sys.exit(1)
        
        execute = self.allOptions['Scheduler']['mpiexec']+' '
        if self.allOptions['no_mpi']:
            execute = self.allOptions['Scheduler']['exec']+' '
            self.allOptions['Scheduler']['process'] = ''
        
        if self.allOptions['no_openmp']:
            self.allOptions['Scheduler']['thread'] = ''
        
        self.allOptions.update({'prefix':self.allOptions['Scheduler']['prefix']})

        self.allOptions.update(self.splitTime(self.allOptions['elapse']))
        
        jobScriptList = list()

        jobScriptList.append('#!/bin/sh')
        jobScriptList.append(self.allOptions['Scheduler']['err2stdout'] % self.allOptions)
        jobScriptList.append(self.allOptions['Scheduler']['queue'] % self.allOptions)
        if self.allOptions['group'] != None:
            jobScriptList.append(self.allOptions['Scheduler']['group'] % self.allOptions)
        jobScriptList.append(self.allOptions['Scheduler']['elapse'] % self.allOptions)
        jobScriptList.append(self.allOptions['Scheduler']['node'] % self.allOptions)
        jobScriptList.append(self.allOptions['Scheduler']['process'] % self.allOptions)
        jobScriptList.append(self.allOptions['Scheduler']['thread'] % self.allOptions)
        jobScriptList.append(execute + self.allOptions['Application']['path'] + (self.allOptions['Application']['exec'] % self.allOptions['AA']))

        if self.allOptions['outfile'] == None:
            for l in jobScriptList:
                print l
        else:
            f = open(self.allOptions['outfile'],'w')
            for l in jobScriptList:
                f.write(l+'\n')
            f.close()
        
    def checkOptions(self):
        if hasattr(self, 'allOptions'):
            self.checkOptionsQueue()
            self.optionsChecked = True
            
    def checkOptionsQueue(self):
        optNodes = self.allOptions['nodes']
        optTime = self.allOptions['elapse']

        for q in self.allOptions['Computer']['queues']:
            if q['queueName'] == self.allOptions['queue']:
                for u in self.allOptions['User']['properties']:
                    if u['computerName']==self.allOptions['Computer']['system']:
                        for uu in u['availableQueues']:
                            if q['queueName']==uu:
                                maxNodes = int(q['maxNodes'])
                                minNodes = int(q['minNodes'])
                                maxTime = q['maxTime']
        if not 'maxNodes' in locals():
            print 'You can\'t use %s queue !' % (self.allOptions['queue'])
            sys.exit(1)

        optNodes = optNodes.split('x')
        optNodes = map(int,optNodes)
        optNodesAll = 1
        for n in optNodes:
            optNodesAll *= n
        if (optNodesAll > maxNodes or optNodesAll < minNodes):
            print 'You can\'t allocate %d nodes ! (%d < nodes < %d)' % (optNodesAll, minNodes, maxNodes)
            sys.exit(1)
        
        maxTimeSeconds = self.timeToSeconds(maxTime)
        elapseTimeSeconds = self.timeToSeconds(optTime)
       
        if elapseTimeSeconds > maxTimeSeconds:
            print 'You can\'t allocate elapse tiem (%d seconds) ! (elapse < %d) ' % (elapseTimeSeconds, maxTimeSeconds)
            sys.exit(1)

    def timeToSeconds(self,time):
        ttime = time.split(':')
        ttime = map(int,ttime)

        if len(ttime) == 1:
            return ttime[0]
        elif len(ttime) == 2:
            return ttime[0]*60 + ttime[1]
        elif len(ttime) == 3:
            return ttime[0]*3600 + ttime[1]*60 + ttime[2]

    def splitTime(self, time):
        ttime = time.split(':')

        if len(ttime) == 1:
            return {'hh':'00','mm':'00','ss':ttime[0]}
        elif len(ttime) == 2:
            return {'hh':'00','mm':ttime[0],'ss':ttime[1]}
        elif len(ttime) == 3:
            return {'hh':ttime[0],'mm':ttime[1], 'ss':ttime[2]}
            

if __name__ == '__main__':
    j = jsas()
    #d = {"thread"       : "export OMP_NUM_THREADS=%(threads)s\nexport PARALLEL=%(threads)s"}
    #print j.parsedOptions
    #print d['thread'] % j.parsedOptions
    j.checkOptions()
    j.printJobScript()
