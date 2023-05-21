from abc import abstractmethod, ABC
from taskset import TaskSet
from job import Job

class Schedule(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def schedule(self, task_set: TaskSet) -> Job:
        pass
