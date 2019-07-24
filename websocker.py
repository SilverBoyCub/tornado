# -*- coding: utf-8 -*-

import random
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import parse_command_line


class Client:
    def __init__(self, clientId, connection):
        self.id = clientId
        self.connection = connection


clients = []


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("client.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args):
        self.id = self.get_argument("kind")
        newclient = True

        mililitros = 0

        if self.id == "caña":
            mililitros = random.randint(200, 300)
        elif self.id == "doble":
            mililitros = random.randint(200, 300)
        else:
            mililitros = 500

        for client in clients:
            if client.id == self.id:
                client.connection.write_message("Marchando %s de %s mililitros!" % (self.id, mililitros))
                newclient = False
                break
        if newclient:
            clientRef = Client(self.id, self)
            clients.append(clientRef)

    def on_message(self, message):
        for client in clients:
            if client.id == self.id:
                print ("Mensaje del cliente recibido : %s" % (message))

    def on_close(self):
        for client in clients:
            if self.id == client.id:
                clients.remove(client)
                break


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
