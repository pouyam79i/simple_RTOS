from scheduler.Schedule import Schedule
from taskset import TaskSet
from job import Job
from math import inf
from task import COMPLETED


# schedule the current task set for the following time step:
# suspend if necessary
class DM_HLP(Schedule):

    def __init__(self) -> None:
        self.semaphore = dict()
    
    # wait on semaphore
    def wait(self, S: int, job: Job):
        set_sem = False
        if S not in self.semaphore.keys():
            set_sem = True
        elif self.semaphore[S] == None:
            set_sem = True
        if set_sem:
            self.semaphore[S] = job
        return set_sem
    
    # signal on semaphore
    def signal(self, S: int):
        if S in self.semaphore.keys():
            self.semaphore[S] = None
    
    # remove completed tasks + automatic signal for tasks
    def update_semaphores(self):
        new_semaphore = dict()
        for key in self.semaphore:
            if self.semaphore[key] == None:
                continue
            if self.semaphore[key].state != COMPLETED:
                if self.semaphore[key].get_section() == key:
                    new_semaphore[key] = self.semaphore[key]
        self.semaphore = new_semaphore
        
    # decide for the current task_set
    # output must be only the next running task or None.
    def schedule(self, task_set: TaskSet, cpu_time: int) -> Job:
        task_set.update_jobs(cpu_time)
        self.update_semaphores()
        selected_job = None

        # Used DM to find a task
        for job in task_set.remaining_jobs:
            if selected_job == None:
                selected_job = job
            else:
                if job.deadline < selected_job.deadline:
                    selected_job = job
                elif job.deadline == selected_job.deadline and selected_job.priority > job.priority:
                    selected_job = job
                elif job.deadline == selected_job.deadline and selected_job.priority == job.priority and job.act_time < selected_job.act_time:
                    selected_job = job
        
        # check HLP
        if selected_job != None:
            section_ID = selected_job.get_section()
            if section_ID > 0:
                if not self.wait(section_ID, job):
                    selected_job = self.semaphore[section_ID]

        return selected_job
    