RUNNING   = 0   # Currently executing on the processor
READY     = 1   # Ready to run but task of higher or equal priority is currently running
BLOCKED   = 2   # Task is waiting for some condition to be met to move to READY state
SUSPENDED = 3   # Task is waiting for some other task to unsuspend
COMPLETED = 4   # when a task is done

INTERRUPT = 0  # Task type is interrupt
PERIODIC  = 1  # Task type is periodic
APERIODIC = 2  # Task type is aperiodic
SPORADIC  = 3  # Task type is sporadic

import uuid

# basic info about task
class Task:

    def __init__(self,priority=255,name=None,state=SUSPENDED,type=None,act_time=0,period=0,wcet=0,deadline=1000):
        # used to identify task
        self.uuid = uuid.uuid4()
        # main props:
        self.priority = priority
        self.name = name
        self.state = state
        self.type = type
        self.act_time = act_time
        self.period = period
        self.wcet = wcet
        self.deadline = deadline

    def set_completed(self): 
        self.state = COMPLETED

    # change priority of task
    def change_priority(self, new_priority):
        self.priority = new_priority
