from scheduler.EDF import EDF
from scheduler.NP_EDF import NP_EDF
from scheduler.DM import DM
from scheduler.RM import RM
from scheduler.Schedule import Schedule
from taskset import TaskSet
from task import RUNNING, COMPLETED, READY, SUSPENDED

class RTOS:

    # GIVEN and algorithm 
    def __init__(self, task_set: TaskSet, scheduler_kind: str) -> None:

        # it show clock time of cpu (here we have time step as int)
        self.cpu_time = 0

        self.task_set = task_set
        self.executing_job = None

        # duration list shows which task was running at what time! - only print it in debug mode
        self.task_duration_list = []
        self.total_executing_time = 0

        # set scheduler
        if scheduler_kind == 'NP_EDF':
            self.scheduler = NP_EDF()
        elif scheduler_kind == 'RM':
            self.scheduler = RM()
        elif scheduler_kind == 'DM':
            self.scheduler = DM()
        else:
            # Default scheduler
            self.scheduler = EDF()

    # TODO: check the non increasing over job.increase_uptime() - if it returns non zero - must split duration
    # append latest executing task duration to this list for simulation purposes
    def append_task_duration(self, name: str, start: int, stop: int):
        self.task_duration_list.append({name: (start, stop)})

    # TODO: complete here
    def run(self, duration=100):

        latest_activation = 0

        for i in range(duration):
            # get a job to execute
            job = self.scheduler.schedule(self.task_set, self.cpu_time)

            if job == None:
                # preempt job if one is executing
                if self.executing_job != None:
                    if self.executing_job.state == RUNNING:
                        self.executing_job.state = READY
                    self.append_task_duration(self.executing_job.get_name(), latest_activation, self.cpu_time)
                    self.executing_job = None
                latest_activation = self.cpu_time
            else:
                # new job is being exec
                if self.executing_job == None:
                    if job.state == READY:
                        latest_activation = self.cpu_time
                        job.state = RUNNING
                        if job.increase_uptime() == 0:
                            self.total_executing_time += 1
                        self.executing_job = job
                # no changes to previous job - continue executing
                elif job.uuid == self.executing_job.uuid:
                    if job.increase_uptime() == 0:
                        self.total_executing_time += 1
                # preempt previous job and make set given job to executioner
                else:
                    self.executing_job.set_state(READY)
                    self.append_task_duration(self.executing_job.get_name(), latest_activation, self.cpu_time)
                    latest_activation = self.cpu_time
                    self.executing_job = job
                    self.executing_job.set_state(RUNNING)
                    if job.increase_uptime() == 0:
                        self.total_executing_time += 1

                # debug
                # if self.executing_job != None:
                #     print("Job info-> uuid: {}, name: {}, uptime: {}, state: {}, ADeadline: {}, cpu_time: {}".format(self.executing_job.uuid, self.executing_job.get_name(), self.executing_job.uptime, self.executing_job.state, self.executing_job.ADeadline, self.cpu_time))

            # go to next clock
            self.cpu_time += 1

        if self.executing_job != None:
            self.append_task_duration(self.executing_job.get_name(), latest_activation, self.cpu_time)
    
    def print_result(self):

        print("Utilization: {}".format(self.total_executing_time/self.cpu_time))
        print("Feasibility: {}".format(str(self.task_set.feasible)))
        print("Task Durations:")
        for item in self.task_duration_list:
            print(item)
