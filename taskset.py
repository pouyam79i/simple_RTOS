import csv
import json
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
        
        # test duration information
        self.start_time = -1
        self.end_time = -1
        
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
                # priority,name,state,type,act_time,period,wcet,deadline
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

    # this function reads from json file according to given structure! (only periodic tasks)
    def read_tasks_from_json(self, filename):
        with open(filename, 'r') as jsonfile:
            info = json.load(jsonfile)
            self.start_time = info['startTime']
            self.end_time = info['endTime']
            for item in info['taskset']:
                task = Task(
                    name='task'+item['taskId'],
                    period=item['period'],
                    wcet=item['wcet'],
                    deadline=item['deadline'],
                    act_time=item['offset'],
                    type=PERIODIC,
                    state=READY,
                    priority=1 # 0 for interrupts
                )
                task.section = item['sections']
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

    # adds a new job to the ready queue
    def add_new_job(self, task: Task, cpu_time: int):
        new_job = Job(task, cpu_time)
        new_job.state = READY
        self.remaining_jobs.append(new_job)
        # print("#DEBUG-job creation job name: {}, act_time: {}, ADeadline: {}, WCET: {}".format(new_job.get_name(), new_job.act_time, new_job.ADeadline, new_job.wcet))

    # create instance of jobs in the right time
    def update_jobs(self, cpu_time):
        self.update_completed()
        self.remove_completed_jobs()
        for task in self.tasks:
            if task.type == PERIODIC and task.period > 0:
                if (cpu_time - task.act_time) % task.period == 0:
                    self.add_new_job(task, cpu_time)
            elif task.type != PERIODIC and task.act_time == cpu_time:
                self.add_new_job(task, cpu_time)
        