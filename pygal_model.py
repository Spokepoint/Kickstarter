
import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import pandas.io.sql as psql
import MySQLdb

import pygal


def get_average_goal(df, category):
  goal = 0.0
  i = 0
  f_goal = 0.0
  f = 0
  suc_goal = 0.0
  s = 0
  for count, row in df.iterrows():
    if row['success'] == 1:
      s += 1
      suc_goal += row['goal']
    if row['success'] == 0:
      f_goal += row['goal']
      f += 1
    goal+= row['goal']
    i += 1
  print category + ': '
  print 'total: ' + str(goal/i) + ' success: ' + str(suc_goal/s) + ' fail: ' + str(f_goal/f) 
  print ''



column_list = ["id","url",'name','backers','parentCat','category','duration', 'date_end','goal','raised','lat','lon','about','faqs','comments','finished','date_scanned', 'success']
cols_to_keep = ['success', 'duration', 'goal']
def logit_fit(sql, category):
  #create dataframe
  df = psql.read_sql(sql, con)
  #dataframe columns
  data = df[cols_to_keep]
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


############
#Art
sql = """
SELECT * FROM test.crawler_project WHERE parentCat = 'Art';
"""
logit_fit(sql, 'Comics')

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


