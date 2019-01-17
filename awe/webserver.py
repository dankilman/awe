import os
import threading
import traceback

import bottle


class WebServer(object):

    def __init__(self, exporter, port, custom_component, encoder):
        self._port = port
        self._exporter = exporter
        self._custom_component = custom_component
        self._encoder = encoder
        self._get_initial_state = exporter.get_initial_state
        self._client_root = exporter.client_root
        self._content_root = os.path.join(os.path.dirname(__file__), 'resources', self._client_root)
        self._app = bottle.Bottle()
        self._app.route('/')(self._index)
        self._app.route('/initial-state')(self._initial_state)
        self._app.route('/export')(self._export)
        self._app.route('/static/<path:path>')(self._get_static_file)
        self._app.route('/custom-components')(self._components)
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True

    def start(self):
        self._thread.start()

    def _run(self):
        bottle.run(self._app, port=self._port)

    def _index(self):
        return self._get_static_file('index.html')

    def _get_static_file(self, path):
        return bottle.static_file(path, self._content_root)

    def _initial_state(self):
        bottle.response.content_type = 'application/json'
        return self._encoder.to_json(self._get_initial_state())

    def _export(self):
        try:
            result = self._exporter.export()
            if not isinstance(result, dict):
                bottle.response.content_type = 'application/octet-stream'
            return result
        except Exception:
            bottle.response.status = 400
            return {'error': traceback.format_exc()}

    def _components(self):
        bottle.response.content_type = 'text/javascript'
        return self._custom_component.combined_script()
