from scheduler.Schedule import Schedule
from taskset import TaskSet
from job import Job
from math import inf
from task import RUNNING

# schedule the current task set for the following time step:
# suspend if necessary
class NP_EDF(Schedule):

    def __init__(self) -> None:
        pass
        
    # decide for the current task_set
    # output must be only the next running task or None.
    # 
    def schedule(self, task_set: TaskSet, cpu_time: int) -> Job:
        task_set.update_jobs(cpu_time)
        min_deadline = inf
        selected_job = None

        for job in task_set.remaining_jobs:
            if job.state == RUNNING:
                selected_job = job
                break
            if job.is_deadline_missed(cpu_time):
                task_set.set_unfeasible()
                continue

            if selected_job == None:
                selected_job = job
                min_deadline = job.ADeadline
            else:
                if min_deadline < job.ADeadline:
                    continue
                elif min_deadline > job.ADeadline:
                    min_deadline = job.ADeadline
                    selected_job = job
                else:
                    # select high priority
                    if selected_job.get_priority() > job.get_priority():
                        selected_job = job
                        min_deadline = job.ADeadline

        return selected_job
