from task import *

# a job is an instance of a task
class Job:

    def __init__(self, task: Task, act_time: int) -> None:
        self.uuid = uuid.uuid4() # job unique id
        self.task = task # task info
        self.act_time = act_time # absolute act time
        self.ADeadline = task.deadline + act_time # absolute
        self.deadline = task.deadline # relative
        self.wcet = task.wcet # worst case execution time
        # uptime is used to find how much of a task has been executed
        self.uptime = 0
        self.state = task.state

    # increase on step of time on this task
    def increase_uptime(self):
        if self.state != RUNNING:
            return -1 # suspended or ready
        if self.uptime < self.wcet:
            self.uptime += 1
            if self.uptime == self.wcet:
                self.state = COMPLETED
            return 0
        else:
            return 1 # completed
        
    # returns state of task
    def get_state(self):
        return self.state
    
    # set state of task
    def set_state(self, new_state):
        if self.state == COMPLETED:
            return -1
        else:
            self.state = new_state
            return 0

    # return state of task
    def is_complete(self):
        if self.state == COMPLETED:
            return True
        return False

    # tells if a deadline is missed
    def is_deadline_missed(self, cpu_time):
        if self.state != COMPLETED and cpu_time >= self.ADeadline:
            return True
        return False 

    # return name of task
    def get_name(self):
        return self.task.name
    
    # return priority of task
    def get_priority(self):
        return self.task.priority
    