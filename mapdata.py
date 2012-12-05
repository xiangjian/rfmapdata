#coding=utf-8
"""
$ pip install tornado
$ python livemap.py --port=8888

Open http://localhost:8888 in one window


Written with tornado==2.3
"""

import os
import json
import logging

import tornado.ioloop
import tornado.web
import sqlite3
from tornado.options import define, options


log = logging.getLogger(__name__)
dbPath = 'data.db'
def _query_db(query, args=(), one=False):
    connection = sqlite3.connect(dbPath)
    cur = connection.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r
def _execute_db(sql,args=(),one=False):
    connection = sqlite3.connect(dbPath)
    cur = connection.cursor()
    cur.execute(sql, args)
    cur.connection.commit()
    cur.connection.close()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        log.debug("open root")
        self.render("index.html")


class DataHandler(tornado.web.RequestHandler):
    """docstring for DataHandler"""
    def get(self):
        """get method"""
        # ajax no cache
        self.set_header('Cache-Control', 'no-cache, must-revalidate')
        self.set_header('Expires', '0')
        dic= _query_db("select * from gis")
        self.write(json.dumps(dic,ensure_ascii=False))
    def post(self):
        """ post  for gis env"""
        dep = self.get_argument("dep")
        id  = self.get_argument("id")
        name= self.get_argument("name")
        lon = self.get_argument("lon")
        lat = self.get_argument("lat")
        # query for only one 
        _execute_db("insert or replace into gis (id,dep,name,lon,lat) values(?,?,?,?,?)",(id,dep,name,lon,lat))
        self.write("OK")

settings = {
    'template_path':os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
}
print settings

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/mapdata", DataHandler),
        ],
    **settings)


if __name__ == "__main__":
    define("port", default=8888, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
