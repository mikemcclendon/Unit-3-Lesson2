import pandas as pd
import sqlite3 as lite
from dateutil.parser import parse
import collections
import sqlite3 as lite
import pandas as pd
import datetime
import requests
from pandas.io.json import json_normalize
import operator
import csv

cities = { "Washington,DC": '38.904103,-77.017229',
            "New York,NY":'40.663619,-73.938589',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }
con = lite.connect('weather.db')
cur = con.cursor()
key = '7552949fcab691f43cc8a0bc2313e770'
start_date = datetime.datetime.now() - datetime.timedelta(days=30)
now = datetime.datetime.now() 
startstr = str(start_date.date())+'T'+str(start_date.time()).split('.', 1)[0]
nowstr = str(now.date())+'T'+str(now.time()).split('.', 1)[0]
 

with con:
    cur.execute("DROP TABLE IF EXISTS weather;")
    cur.execute('CREATE TABLE weather (date STR PRIMARY KEY, city STR, tempstart FLOAT)')


for k, v in cities.iteritems():
	dict = {}
	for i in range(30):	
		start_date = datetime.datetime.now() - datetime.timedelta(days=i)
		startstr = str(start_date.date())+'T'+str(start_date.time()).split('.', 1)[0]
		startr = requests.get('https://api.forecast.io/forecast/'+key+'/'+str(v)+','+startstr)
		dict[start_date] = startr.json()['daily']['data'][0]['temperatureMax']
	#max = (str(max(dict.iteritems(), key=operator.itemgetter(1))[0]), k, (max(dict.values())))
	with con:
		cur.execute('INSERT INTO weather VALUES (?,?,?)', (str(max(dict.iteritems(), key=operator.itemgetter(1))[0]), k, (max(dict.values())),))
		con.commit()
	df = pd.read_sql_query("SELECT * from weather", con)
print(df)


		
		
		
	

