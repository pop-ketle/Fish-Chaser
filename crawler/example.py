import os
import sqlite3

'''The sample for SQL code'''


DB_NAME = 'data.db'
DATABASE_PATH = '../datasets/'

con = sqlite3.connect('../datasets/data.db')
c = con.cursor()

sql = f'SELECT * FROM fishery_data ORDER BY 日付 asc'
print([list(x) for x in c.execute(sql)])

c.close()