import csv
from task import *
from job import Job

class TaskSet:
    
    def __init__(self) -> None:
        # task info
        self.tasks = []
        self.completed_task = []

        # job info
        self.remaining_jobs = []

        # scheduler feasibility
        self.feasible = True

    # Call when you make sure the set is not feasible with current scheduler
    def set_unfeasible(self):
        self.feasible = False

    # Load Tasks
    def read_tasks_from_csv(self, filename):
        with open(filename, 'r') as csvfile:
            # header in csv file: priority,name,  state, type, act_time, period, wcet, deadline
            taskreader = csv.reader(csvfile, delimiter=',',)
            next(taskreader, None)  # skip the headers
            for row in taskreader:
                # priority,name,  state, type, act_time, period, wcet, deadline = row
                task = Task(
                    priority=int(row[0]),
                    name=row[1],
                    state=int(row[2]),
                    type=int(row[3]),
                    act_time=int(row[4]),
                    period=int(row[5]),
                    wcet=int(row[6]),
                    deadline=int(row[7])
                )
                self.tasks.append(task)

    # remove completed task from task list
    def update_completed(self):
        temp_list = []
        while len(self.tasks) > 0:
            task = self.tasks.pop(0)
            if task.state == COMPLETED:
                self.completed_task.append(task)
            else:
                temp_list.append(task)
        self.tasks = temp_list

    # remove completed jobs
    def remove_completed_jobs(self):
        jobs = []
        while len(self.remaining_jobs) > 0:
            job = self.remaining_jobs.pop(0)
            if job.state != COMPLETED:
                jobs.append(job)
        self.remaining_jobs = jobs

    # create instance of jobs in the right time
    def update_jobs(self, cpu_time):
        self.update_completed()
        self.remove_completed_jobs()
        for task in self.tasks:
            if task.type == PERIODIC and task.period > 0:
                if (cpu_time - task.act_time) % task.period == 0:
                    self.remaining_jobs.append(Job(task, cpu_time))
            elif task.type != PERIODIC and task.act_time == cpu_time:
                self.remaining_jobs.append(Job(task, cpu_time))
            