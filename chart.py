import altair as alt
import pandas as pd

class Chart:

    def __init__(self, duration: list) -> None:
        self.duration_list = duration
        self.task_names = set()
        self.colormapping = dict()
        self.cats = dict()
        for item in duration:
            self.task_names.add(item['name'])
        self.color = 0
        for item in self.task_names:
            self.color += 1
            self.colormapping[item] = 'C' + str(self.color-1)
            self.cats[item] = self.color
        
        self.frm = []
        self.to = []
        self.activity = []
        for item in duration:
            self.frm.append(item['duration'][0])
            self.to.append(item['duration'][1])
            self.activity.append(item['name'])

        self.data = pd.DataFrame()
        self.data['from'] = self.frm
        self.data['to'] = self.to
        self.data['task'] = self.activity


    def draw(self):
        alt.renderers.enable('altair_viewer')
        chart = alt.Chart(self.data).mark_bar().encode(
            x='from',
            x2='to',
            y='task',
            color=alt.Color('task', scale=alt.Scale(scheme='dark2')))
        chart.show()