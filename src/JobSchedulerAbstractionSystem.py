class JobSchedulerAbstractionSystem:
    def __init__(self, scheduler='', prefix='', shell='/bin/sh', queue='', group='', elapse='00:15:00', MPI=True, node='1', process='1', OMP=True, thread='0', run='a.out'):
        self.scheduler = scheduler
        self.prefix = prefix
        self.shell = shell
        self.queue = queue
        self.group = group
        self.elapse = elapse
        
        self.MPI = MPI
        self.node = node
        self.process = process
        
        self.OMP = OMP
        self.thread = thread
        
        self.run = run

    def readFormat():
    
    def outputScript():
    
