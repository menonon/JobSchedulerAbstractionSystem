import os
import fnmatch
import json
import fileinput

class JobSchedulerAbstractionSystem:
    def __init__(self, scheduler='', shell='/bin/sh', err2stdout=True, \
                 queue='', group='', elapse='00:15:00', \
                 MPI=True, node='1', process='1', \
                 OMP=True, thread='0', run='a.out'):
        self.scheduler = scheduler
        self.shell = shell
        self.err2stdout = err2stdout
        self.queue = queue
        self.group = group
        self.elapse = elapse
        
        self.MPI = MPI
        self.node = node
        self.process = process
        
        self.OMP = OMP
        self.thread = thread
        
        self.run = run

class JobSchedulerDatabase:
    def __init__(self):
        schdlSetting = ''
        self.schdl = list()
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, 'schdl_*.json'):
                schdlSetting=''
                for line in fileinput.input(file):
                    schdlSetting += line
                print schdlSetting
                self.schdl.append(json.loads(schdlSetting))
