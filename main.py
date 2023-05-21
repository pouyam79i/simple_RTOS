import sys
import string
from RTOS import RTOS
from taskset import TaskSet

DEFAULT_DURATION = 100 # 100 time steps as default

def main(argv):
   duration = DEFAULT_DURATION
   scheduler_kind = 'EDF'
   filename = 'tasks1.csv'
   if len(argv) > 0:
      try:
         duration = int(argv[0])
      except:
         duration = DEFAULT_DURATION
   if len(argv) > 1:
      scheduler_kind = string.upper(argv[1])
   if len(argv) > 2:
      filename = argv[2]

   print("Running main app with duration: {} and scheduler kind: {} and filename: {}".format(duration, scheduler_kind, filename))
   

   # TODO: load task set
   task_set = TaskSet()
   task_set.read_tasks_from_csv('tasks/' + filename)
   # build os kernel :DDDDDD
   rtos = RTOS(task_set, scheduler_kind)
   # run tasks
   rtos.run(duration)




# Run app main
if __name__ == "__main__":
   main(sys.argv[1:])