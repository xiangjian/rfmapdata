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

from tornado.options import define, options


log = logging.getLogger(__name__)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        log.debug("open root")
        self.redirect("/static/index.html")




settings = {
    # FIXME: Should really move maps.html into static/, and change the last
    # empty quotes to "static" (it's in same dir for gist)
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
}
print settings

application = tornado.web.Application([
        (r"/", MainHandler),
        ],
    **settings)


if __name__ == "__main__":
    define("port", default=8888, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
