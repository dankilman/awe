import os
import threading
import traceback

import bottle

from . import resources


class WebServer(object):

    def __init__(self, get_initial_state, exporter, port):
        self._port = port
        self._get_initial_state = get_initial_state
        self._exporter = exporter
        self._client_root = 'client/awe/build'
        self._content_root = os.path.join(os.path.dirname(__file__), 'resources', self._client_root)
        self._app = bottle.Bottle()
        self._app.route('/')(self._index)
        self._app.route('/initial-state')(self._get_initial_state)
        self._app.route('/export')(self._export)
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

    def _export(self):
        index = resources.get(os.path.join(self._client_root, 'index.html'))
        state = self._get_initial_state()
        try:
            result = self._exporter.export(index=index, state=state)
            if not isinstance(result, dict):
                bottle.response.content_type = 'application/octet-stream'
            return result
        except Exception:
            bottle.response.status = 400
            return {'error': traceback.format_exc()}
