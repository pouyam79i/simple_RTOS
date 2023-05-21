from abc import abstractmethod, ABC

class Schedule(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def schedule(self, task_set):
        pass
