"""
@author: Hamsavardhini
"""

#Python flask framework is deployed using this Tornado server
#File that starts the server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from neo4j import APP

http_server = HTTPServer(WSGIContainer(APP))
#port - has to be open if Demo url is needed to access from outside network.
http_server.listen(5555)
IOLoop.instance().start()
