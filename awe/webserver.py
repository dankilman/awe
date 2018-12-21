import os
import threading

import bottle


class WebServer(object):

    def __init__(self, page, port):
        self._port = port
        self._page = page
        self._content_root = os.path.join(os.path.dirname(__file__), 'resources', 'client', 'awe', 'build')
        self._app = bottle.Bottle()
        self._app.route('/')(self._index)
        self._app.route('/initial-state')(self._page.get_initial_state)
        self._app.route('/static/<path:path>')(self._get_static_file)
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True

    def start(self):
        self._thread.start()

    def run(self):
        bottle.run(self._app, port=self._port)

    def _index(self):
        return self._get_static_file('index.html')

    def _get_static_file(self, path):
        return bottle.static_file(path, self._content_root)
