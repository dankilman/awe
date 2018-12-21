import json
import sys
import threading

import twisted.python.log
import twisted.internet.reactor
from autobahn.twisted import websocket


class Connection(websocket.WebSocketServerProtocol):

    def on_open(self):
        self.factory.open_connections[id(self)] = self

    def on_message(self, payload, _):
        message = json.loads(payload)
        self.factory.message_handler.handle(message)

    def on_close(self, *_):
        self.factory.open_connections.pop(id(self))

    def dispatch(self, action):
        self.sendMessage(json.dumps(action))

    onOpen = on_open
    onMessage = on_message
    onClose = on_close


class WebSocketServer(websocket.WebSocketServerFactory):

    def __init__(self, message_handler, host='127.0.0.1', port=9000):
        super(WebSocketServer, self).__init__('ws://{}:{}'.format(host, port))
        self.protocol = Connection
        self.config = {'host': host, 'port': port}
        self.open_connections = {}
        self.message_handler = message_handler
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def run(self):
        twisted.python.log.startLogging(sys.stdout)
        twisted.internet.reactor.listenTCP(self.config['port'], self)
        twisted.internet.reactor.run(installSignalHandlers=False)

    def dispatch(self, action):
        for connection in self.open_connections.values():
            connection.dispatch(action)

    def dispatch_from_thread(self, action):
        twisted.internet.reactor.callFromThread(self.dispatch, action)
