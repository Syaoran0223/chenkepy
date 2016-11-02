#coding: utf-8

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
from app import create_app

enable_pretty_logging()

app = create_app('development')
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)  #flask默认的端口
IOLoop.instance().start()
