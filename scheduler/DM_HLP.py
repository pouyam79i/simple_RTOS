from scheduler.Schedule import Schedule
from taskset import TaskSet
from job import Job
from math import inf
from task import PERIODIC


# schedule the current task set for the following time step:
# suspend if necessary
class DM_HLP(Schedule):

    def __init__(self) -> None:
        pass
        
    # decide for the current task_set
    # output must be only the next running task or None.
    def schedule(self, task_set: TaskSet, cpu_time: int) -> Job:
        task_set.update_jobs(cpu_time)
        min_deadline = inf
        selected_job = None

        for job in task_set.remaining_jobs:
            # abort job on miss
            if job.is_deadline_missed(cpu_time):
                task_set.set_unfeasible()
                continue

            if selected_job == None:
                selected_job = job
                min_deadline = selected_job.deadline
            else:
                if job.deadline < selected_job.deadline:
                    selected_job = job
                    min_deadline = selected_job.deadline
                elif job.deadline == selected_job.deadline and selected_job.priority > job.priority:
                    selected_job = job
                    min_deadline = selected_job.deadline


        return selected_job
    