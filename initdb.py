#coding=utf-8
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE gis
             (id text UNIQUE, name text, dep text, lon real, lat real)''')

# Insert a row of data
c.execute("INSERT INTO gis VALUES ('xiangjian','项建','数据技术部',116.490956, 39.988563)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
