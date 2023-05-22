import sys
from RTOS import RTOS
from taskset import TaskSet

DEFAULT_DURATION = 100      # 100 time steps as default
DEFAULT_SCHEDULER = 'EDF'   
DEFAULT_TASKSET = 'tasks1'  
DEFAULT_CHART = 'OFF'

def main(argv):
   duration = DEFAULT_DURATION
   scheduler_kind = DEFAULT_SCHEDULER
   filename = DEFAULT_TASKSET
   chart_mode = DEFAULT_CHART
   if len(argv) > 0:
      try:
         duration = int(argv[0])
      except:
         duration = DEFAULT_DURATION
   if len(argv) > 1:
      scheduler_kind = argv[1]
   if len(argv) > 2:
      filename = argv[2]
   if len(argv) > 3:
      if argv[3] == 'ON':
         chart_mode = 'ON'

   print("Running main app with duration: {} and scheduler kind: {} and filename: {}".format(duration, scheduler_kind, filename))

   # TODO: load task set
   task_set = TaskSet()
   task_set.read_tasks_from_csv('tasks/' + filename + '.csv')
   # build os kernel :DDDDDD
   rtos = RTOS(task_set, scheduler_kind)
   # run tasks with given duration(max cpu time)
   rtos.run(duration)
   rtos.print_result(chart_mode)

# Run app main
if __name__ == "__main__":
   main(sys.argv[1:])