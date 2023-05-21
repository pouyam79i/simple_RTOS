from scheduler.Schedule import Schedule

# schedule the current task set for the following time step:
# suspend if necessary
class RM(Schedule):

    def __init__(self) -> None:
        pass
        
    # decide for the current task_set
    # output must be only the next running task or None.
    def schedule(self, task_set):
        pass