
import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import scipy.stats as stats
import pandas.io.sql as psql
import MySQLdb

import matplotlib.pyplot as plt
import pygal
from pygal.style import Style
custom_style = Style(
  background='transparent',
  plot_background='transparent',
  foreground='#111111',
  foreground_light='#000000',
  foreground_dark='#111111',
  opacity='.9',
  opacity_hover='.6',
  transition='400ms ease-in',
  colors=('#444444', '#4c1066', '#E95355', '#E87653', '#E89B53'))

column_list = ["id","url",'name','backers','parentCat','category','duration', 'date_end','goal','raised','lat','lon','about','faqs','comments','finished','date_scanned', 'success']
cols_to_graph = ['url', 'success', 'duration', 'goal']
cols_to_keep = ['success', 'duration', 'goal']

def cartesian(arrays, out=None): 
    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype
 
    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)
 
    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out


def show_graph(fail, success, category):
  xy_chart = pygal.XY(stroke=False, show_legend=False, spacing=0, width=1500, style=custom_style, title_font_size=20, major_label_font_size=16, label_font_size=14, x_title='Duration', y_title='Goal of Campaign')
  #xy_chart.title = category
  xy_chart.add('fail', fail)
  xy_chart.add('success', success)
  xy_chart.render_to_file(str(category + ".svg")) 


def seperate_data(df, category):
  fail = []
  success = []
  max_success = 0
  for count, row in df.iterrows():
    if row['success'] == 0:
      fail.append({'value': (row['duration'], row['goal']), 'xlink': row['url']})
    else:
      success.append({'value': (row['duration'], row['goal']), 'xlink': row['url']})
      if row['duration'] < 11 and row['goal'] > max_success:
        max_success = row['goal']
  show_graph(fail, success, category)
  print category + ": " + str(max_success)

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

  
def logit_fit(sql, category, intercept):
  #create dataframe
  df = psql.read_sql(sql, con)
  #dataframe columns
  data = df[cols_to_graph]
  data = data[data['duration'] < 61]
  data = data[data['goal'] < stats.scoreatpercentile(data['goal'], 99)]
  seperate_data(data, category)
  data = data[cols_to_keep]
  #print category
  #print stats.scoreatpercentile(data['goal'], 99)
  data['intercept'] = intercept
  train_cols = data.columns[1:]
  logit = sm.Logit(data['success'], data[train_cols])
  #fit the model
  result = logit.fit()
  print category
  print result.summary()
  r = result.params
  print r
  return data
  #print r
  #goal = np.linspace(data['goal'].min(), data['goal'].max(), 10)
  #dur = np.linspace(data['duration'].min(), data['duration'].max(), 10)
  #combos = pd.DataFrame(cartesian([goal, dur]))
  #combos.columns = ['goal', 'duration']
  #combos['success'] = result.predict(combos)
  #seperate_data(data, category)
  #return logit


category = logit_fit(sql, 'category', .44)

############
#Art
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Art';
      """
art = logit_fit(sql, 'Art', .44)

def bar_chart():
  bar_chart = pygal.Bar()
  bar_chart.x_labels = map(str, range(0, 5))
  print np.histogram(art['goal'], range(0, 10000, 1000))
  bar_chart.add("rate", np.histogram(category['goal'], range(0, 100000, 50))[0])
  bar_chart.render_to_file("test.svg")

############
#Comics
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Comics';
      """
comic = logit_fit(sql, 'Comics', .44)


############
#Dance
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Dance';
      """
dance = logit_fit(sql, 'Dance', .44)


############
#Design
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Design';
      """
design = logit_fit(sql, 'Design', .44)


############
#Fashion
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Fashion';
      """
fashion = logit_fit(sql, 'Fashion', .44)

############
#Film & Video
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Film & Video';
      """
film = logit_fit(sql, 'Film & Video', .44)


############
#Food
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Food';
      """
food = logit_fit(sql, 'Food', .44)

############
#Games
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Games';
      """
games = logit_fit(sql, 'Games', .44)

############
#Journalism
sql = """
        SELECT * FROM test.crawler_project WHERE category = 'Journalism';
      """
journalism = logit_fit(sql, 'Journalism', .44)

############
#Music
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Music';
      """
music = logit_fit(sql, 'Music', .44)

############
#Photography
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Photography';
      """
photography = logit_fit(sql, 'Photography', .44)

############
#Publishing
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Publishing';
      """
publishing = logit_fit(sql, 'Publishing', .44)


############
#Technology
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Technology';
      """
tech = logit_fit(sql, 'Technology', .44)


############
#Theater
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Theater';
      """
theater = logit_fit(sql, 'Theater', .44)

if __name__ == '__main__':
  cont = False
  while(cont):
    #goal = int(raw_input("Please enter amount: "))
    #duration = int(raw_input("Please enter time: "))
    category = str(raw_input("Please enter category: "))
    intercept = float(raw_input("category intercept: "))
    sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = '""" + category + """';"""
    result = logit_fit(sql, category, intercept) 
    #print result.fit().predict([(duration, goal, intercept)])
    #exog = (duration, goal, intercept)
    #print result.cdf(np.dot(exog, result.fit().params))
    #print result.fit().params
    cont = bool(raw_input("Enter True or False to continue:"))




