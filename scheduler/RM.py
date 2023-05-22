from scheduler.Schedule import Schedule
from taskset import TaskSet
from job import Job
from math import inf
from task import PERIODIC


# schedule the current task set for the following time step:
# suspend if necessary
class RM(Schedule):

    def __init__(self) -> None:
        pass
        
    # decide for the current task_set
    # output must be only the next running task or None.
    def schedule(self, task_set: TaskSet, cpu_time: int) -> Job:
        task_set.update_jobs(cpu_time)
        min_period = inf
        selected_job = None
        selected_job_is_periodic = True

        for job in task_set.remaining_jobs:
            if job.is_deadline_missed(cpu_time):
                task_set.set_unfeasible()
                continue

            if selected_job == None:
                selected_job = job
                if selected_job.type != PERIODIC:
                    selected_job_is_periodic = False
                else:
                    min_period = selected_job.period
            else:
                if job.type != PERIODIC:
                    if not selected_job_is_periodic:
                        if job.priority > selected_job.priority:
                            selected_job = job
                        elif job.priority == selected_job.priority and job.ADeadline < selected_job.ADeadline:
                            selected_job = job
                    else:
                        min_period = inf # no need
                        selected_job_is_periodic = False
                        selected_job = job
                elif selected_job_is_periodic:
                    if job.period < selected_job.period:
                        min_period = job.period
                        selected_job = job
                    elif job.period == selected_job.period:
                        if job.priority < selected_job.priority:
                            min_period = job.period
                            selected_job = job
                        elif job.priority == selected_job.priority and job.ADeadline < selected_job.ADeadline:
                            min_period = job.period
                            selected_job = job

        return selected_job
    