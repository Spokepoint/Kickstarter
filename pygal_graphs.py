
import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import pandas.io.sql as psql
import scipy.stats as stats
import MySQLdb

import pygal
from pygal.style import Style
custom_style = Style(
  background='transparent',
  plot_background='transparent',
  foreground='#666666',
  foreground_light='#000000',
  foreground_dark='#111111',
  opacity='.9',
  opacity_hover='.6',
  transition='400ms ease-in',
  colors=('#4c1066', '#666666', '#E95355', '#E87653', '#E89B53'))

column_list = ["id","url",'name','backers','parentCat','category','duration', 'date_end','goal','raised','lat','lon','about','faqs','comments','finished','date_scanned', 'success']
cols_to_keep = ['success', 'duration', 'goal']
average_goals = []
success_goals = []
fail_goals = []

average_length = []
success_length = []
fail_length = []


def get_average_goal(df, category):
  goal = 0.0
  i = 0.0
  f_goal = 0.0
  f = 0.0
  suc_goal = 0.0
  s = 0.0
  for count, row in df.iterrows():
    if row['success'] == 1:
      s += 1
      suc_goal += row['goal']
    if row['success'] == 0:
      f_goal += row['goal']
      f += 1
    goal+= row['goal']
    i += 1
  average_goals.append(goal/i)
  success_goals.append(suc_goal/s)
  fail_goals.append(f_goal/f)
  create_pie_chart((s/i), category)

def length_success_rate(df):
  last_dur = 0
  for dur in range(5, 65, 5):
    success = 0.0
    total = 0.0
    for count, row in df.iterrows():
      cur_dur = row['duration']
      if cur_dur <= dur and cur_dur > last_dur:
        if row['success'] == 1:
          success += 1
        total += 1
    last_dur = dur
    if success > 0:
      average_length.append(100 * success/total)
  #success_length.append(s_length/s)
  #fail_length.append(f_length/f)


def show_graph():
  bar_chart = pygal.Bar(show_legend=False, spacing=0, width=1300, style=custom_style, title_font_size=20, label_font_size=16, x_title='Category', y_title='Goal of Campaign')
  bar_chart.title = 'Average Goal for Category'
  bar_chart.x_labels = ('All', 'Art', 'Comics', 'Dance', 'Design', 'Fashion', 'Video', 'Food', 'Games', 'Journalism', 'Music', 'Photography', 'Publishing', 'Technology', 'Theater')
  bar_chart.add('success', np.around(success_goals,  decimals=2))
  bar_chart.add('failure', np.around(fail_goals,  decimals=2))
  bar_chart.render_to_file("Goals.svg")

  bar_chart = pygal.Bar(show_legend=False, spacing=0, height=750, width=1300, style=custom_style,title_font_size=24, label_font_size=14, x_title='Category', y_title='Goal of Campaign', range=(0, 30000))
  bar_chart.title = 'Average Goal for Category'
  bar_chart.x_labels = ('All', 'Art', 'Comics', 'Dance', 'Design', 'Fashion', 'Video', 'Food', 'Games', 'Journalism', 'Music', 'Photography', 'Publishing', 'Technology', 'Theater')
  bar_chart.add('success', np.around(average_goals,  decimals=2))
  bar_chart.render_to_file("TotalGoals.svg")

  len_chart = pygal.Line(show_legend=False, spacing=0, width=1300, style=custom_style,title_font_size=24, label_font_size=17, x_title='Duration of Campaign', y_title='Percent Successful', fill=True, range=(30, 70))
  len_chart.title = 'Average Success Rate based on Duration'
  len_chart.x_labels = map(str, range(5, 65, 5))
  len_chart.Xtitle = "Length"
  len_chart.Ytitle = "Duration of Campaign"
  len_chart.add('ratio', np.around(average_length,  decimals=2))
  #bar_chart.add('total', average_goals)
  len_chart.render_to_file("Duration.svg")

def create_pie_chart(rate, category):
  pie_chart = pygal.Pie(style=custom_style, title_font_size=18)
  pie_chart.title = 'Success Rate of ' + category
  pie_chart.add('success', rate)
  pie_chart.add('failure', (1-rate))
  pie_chart.render_to_file(category + ".svg")


def logit_fit(sql, category):
  #create dataframe
  df = psql.read_sql(sql, con)
  #dataframe columns
  data = df[cols_to_keep]
  data = data[data['duration'] < 61]
  data = data[data['goal'] < stats.scoreatpercentile(data['goal'], 99)]
  get_average_goal(data, category)
  #train_cols = data.columns[1:]
  #logit = sm.Logit(data['success'], data[train_cols])
  #fit the model
  #result = logit.fit()
  #print category + ' result summary'
  #print result.summary()
  #print result.conf_int()

# read the data in
#df = pd.read_csv("output2.csv")
#Establish a connection to the MySQL database
con = MySQLdb.connect(host= 'localhost',
  port=3306,
  user='root',
  passwd='',
  db='test')
sql = """
SELECT * FROM test.crawler_project;
"""
logit_fit(sql, 'All data')
length_success_rate(psql.read_sql(sql, con)[cols_to_keep])

############
#Art
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Art';
"""
logit_fit(sql, 'Art')

############
#Comics
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Comics';
"""
logit_fit(sql, 'Comics')


############
#Dance
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Dance';
"""
logit_fit(sql, 'Dance')


############
#Design
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Design';
"""
logit_fit(sql, 'Design')


############
#Fashion
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Fashion';
"""
logit_fit(sql, 'Fashion')

############
#Film & Video
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Film & Video';
"""
logit_fit(sql, 'Film & Video')


############
#Food
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Food';
"""
logit_fit(sql, 'Food')

############
#Games
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Games';
"""
logit_fit(sql, 'Games')

############
#Journalism
sql = """
SELECT * FROM test.crawler_project WHERE category = 'Journalism';
"""
logit_fit(sql, 'Journalism')

############
#Music
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Music';
"""
logit_fit(sql, 'Music')

############
#Photography
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Photography';
"""
logit_fit(sql, 'Photography')

############
#Publishing
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Publishing';
"""
logit_fit(sql, 'Publishing')


############
#Technology
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Technology';
"""
logit_fit(sql, 'Technology')


############
#Theater
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Theater';
"""
logit_fit(sql, 'Theater')

show_graph()


