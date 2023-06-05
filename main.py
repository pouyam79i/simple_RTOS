import sys, getopt
from RTOS import RTOS
from taskset import TaskSet

DEFAULT_DURATION = 100      # 100 time steps as default
DEFAULT_SCHEDULER = 'EDF'   
DEFAULT_TASKSET = 'tasks1'  
DEFAULT_CHART = 'OFF'

def main(opts, argv):
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
      filename = argv[2] + '.csv'
   if len(argv) > 3:
      if argv[3] == 'ON':
         chart_mode = 'ON'

   for opt, arg in opts:
      if opt in ("d", "duration"):
         if args > 10:
            try:
               duration = int(argv[0])
            except:
               duration = DEFAULT_DURATION
      elif opt in ("s", "scheduler"):
         scheduler_kind = arg
      elif opt in ("j", "json"):
         filename = arg + '.json'
      elif opt in ("t", "taskset"):
         filename = arg + '.csv'
      elif opt in ("c", "chart"):
         if arg.upper() == 'ON':
            chart_mode = 'ON'

   print("Running main app with duration: {} and scheduler kind: {} and filename: {}".format(duration, scheduler_kind, filename))

   # TODO: load task set
   task_set = TaskSet()
   task_set.read_tasks_from_csv('tasks/' + filename)
   # build os kernel :DDDDDD
   rtos = RTOS(task_set, scheduler_kind)
   # run tasks with given duration(max cpu time)
   rtos.run(duration)
   rtos.print_result(chart_mode)

# Run app main
if __name__ == "__main__":
   args = sys.argv[1:]
   opt, argv = getopt.getopt(args,"d:s:j:t:c",["duration=","scheduler=","json=","taskset=","chart="])
   main(opts, argv)