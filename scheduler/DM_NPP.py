from scheduler.Schedule import Schedule
from taskset import TaskSet
from job import Job
from math import inf
from task import COMPLETED

# schedule the current task set for the following time step:
# suspend if necessary
class DM_NPP(Schedule):

    def __init__(self) -> None:
        # use semaphore lock to lock preemption
        self.semaphore_lock = False
        self.locked_by_job = None
        pass
        
    # decide for the current task_set
    # output must be only the next running task or None.
    def schedule(self, task_set: TaskSet, cpu_time: int) -> Job:
        task_set.update_jobs(cpu_time)
        selected_job = None
        
        # Used DM to find a task
        for job in task_set.remaining_jobs:
            if job.is_deadline_missed(cpu_time):
                task_set.set_unfeasible()
            
            if selected_job == None:
                selected_job = job
            else:
                if job.deadline < selected_job.deadline:
                    selected_job = job
                elif job.deadline == selected_job.deadline and selected_job.priority > job.priority:
                    selected_job = job
                elif job.deadline == selected_job.deadline and selected_job.priority == job.priority and job.act_time < selected_job.act_time:
                    selected_job = job
                    
        # check lock
        if self.semaphore_lock:
            if self.locked_by_job.state != COMPLETED:
                return self.locked_by_job
            else:
                self.semaphore_lock = False
                self.locked_by_job = None
        
        # set lock if needed
        if selected_job != None:
            section_ID = selected_job.get_section()
            if section_ID > 0:
                self.semaphore_lock = True
                self.locked_by_job = selected_job

        return selected_job
