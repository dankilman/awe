import json
import sys
import threading
import txaio

import six

if six.PY2:
    from twisted.python import log
    from twisted.internet import reactor
    from autobahn.twisted import websocket
    asyncio = None
else:
    log = None
    reactor = None
    from autobahn.asyncio import websocket
    import asyncio


class Connection(websocket.WebSocketServerProtocol):

    def on_open(self):
        client_id = str(id(self))
        self.factory.open_connections[client_id] = self
        self.dispatch({'type': 'setClientId', 'clientId': client_id})

    def on_message(self, payload, _):
        message = json.loads(payload)
        self.factory.message_handler.handle(message)

    def on_close(self, *_):
        self.factory.open_connections.pop(str(id(self)), None)

    def dispatch(self, action):
        message = json.dumps(action)
        if six.PY3:
            message = bytes(message, encoding='utf-8')
        self.sendMessage(message)

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
        self.loop = None

    def start(self):
        self.thread.start()

    def run(self):
        if six.PY2:
            log.startLogging(sys.stdout)
            reactor.listenTCP(self.config['port'], self)
            reactor.run(installSignalHandlers=False)
        else:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            txaio.config.loop = self.loop
            future = self.loop.create_server(self, self.config['host'], self.config['port'])
            self.loop.run_until_complete(future)
            self.loop.run_forever()

    def dispatch(self, action, client_id=None):
        connections = [self.open_connections[client_id]] if client_id else list(self.open_connections.values())
        for connection in connections:
            connection.dispatch(action)

    def dispatch_from_thread(self, action, client_id):
        if six.PY2:
            reactor.callFromThread(self.dispatch, action, client_id)
        else:
            self.loop.call_soon_threadsafe(self.dispatch, action, client_id)
