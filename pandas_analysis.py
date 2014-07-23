
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
  foreground='#53A0E8',
  foreground_light='#53A0E8',
  foreground_dark='#53A0E8',
  opacity='.6',
  opacity_hover='.9',
  transition='400ms ease-in',
  colors=('#DC143C', '#00FF00', '#E95355', '#E87653', '#E89B53'))

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
  xy_chart = pygal.XY(stroke=False, style=custom_style)
  xy_chart.title = category
  xy_chart.Xtitle = "Days of Campaign"
  xy_chart.Ytitle = "Goal of Campaign"
  xy_chart.add('fail', fail)
  xy_chart.add('success', success)
  xy_chart.render_to_file(str(category + ".svg")) 


def seperate_data(df, category):
  fail = []
  success = []
  for count, row in df.iterrows():
    if row['success'] == 0:
      fail.append({'value': (row['duration'], row['goal']), 'xlink': row['url']})
    else:
      success.append({'value': (row['duration'], row['goal']), 'xlink': row['url']})
  show_graph(fail, success, category)

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
  #data = data[data['duration'] < 61]
  #data = data[data['goal'] < 100000]
  #seperate_data(data, category)
  data = data[cols_to_keep]
  #print category
  #print stats.scoreatpercentile(data['goal'], 98)
  data['intercept'] = intercept
  train_cols = data.columns[1:]
  logit = sm.Logit(data['success'], data[train_cols])
  #fit the model
  result = logit.fit()
  r = result.params
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
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
# example data
category = category[category['goal'] < 100000]
mu = 8800 # mean of distribution
sigma = 6000 # standard deviation of distribution
x = mu + sigma * category['goal']

num_bins = 10
# the histogram of the data
n, bins, patches = plt.hist(x, num_bins)
plt.setp(patches, 'facecolor', 'g')
# add a 'best fit' line
y = mlab.normpdf(bins, mu, sigma)
plt.plot(bins, y, 'r--')
plt.show()

############
#Art
sql = """
        SELECT * FROM test.crawler_project WHERE parentCat = 'Art';
      """
art = logit_fit(sql, 'Art', .44)

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
  cont = True
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




