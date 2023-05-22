from scheduler.Schedule import Schedule
from taskset import TaskSet
from job import Job

# schedule the current task set for the following time step:
# suspend if necessary
class RM(Schedule):

    def __init__(self) -> None:
        pass
        
    # decide for the current task_set
    # output must be only the next running task or None.
    def schedule(self, task_set: TaskSet, cpu_time: int) -> Job:
        return None