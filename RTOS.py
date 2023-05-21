from scheduler.EDF import EDF
from scheduler.NP_EDF import NP_EDF
from scheduler.DM import DM
from scheduler.RM import RM
from scheduler.Schedule import Schedule
from taskset import TaskSet

class RTOS:

    # GIVEN and algorithm 
    def __init__(self, task_set: TaskSet, scheduler_kind: str) -> None:

        # it show clock time of cpu (here we have time step as int)
        self.cpu_time = 0

        self.task_set = task_set
        self.executing_task = None

        # duration list shows which task was running at what time! - only print it in debug mode
        self.duration_list = []
        self.total_executing_time = 0

        # set scheduler
        self.scheduler = Schedule()
        if scheduler_kind == 'NP_EDF':
            self.scheduler = NP_EDF()
        elif scheduler_kind == 'RM':
            self.scheduler = RM()
        elif scheduler_kind == 'DM':
            self.scheduler = DM()
        else:
            # Default scheduler
            self.scheduler = EDF()

    # TODO: complete here
    def run(self, duration=100):

        duration = 0
        for i in range(duration):

            task = self.scheduler.schedule(self.task_set)
            if task == None:
                # TODO: preempt task if one is executing
                if self.executing_task != None:
                    pass  
            else:
                if task.uuid == self.executing_task.uuid:
                    duration += 1
                else:
                    # TODO: preempt current and exec new one
                    pass

        # TODO: add duration for last task
        if self.executing_task != None:
                pass
