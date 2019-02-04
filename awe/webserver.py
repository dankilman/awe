import os
import threading
import traceback

import bottle


class WebServer(object):

    def __init__(self, exporter, host, port, websocket_port, custom_component, encoder, api):
        self._api = api
        self._host = host
        self._port = port
        self._websocket_port = websocket_port
        self._exporter = exporter
        self._custom_component = custom_component
        self._encoder = encoder
        self._get_initial_state = exporter.get_initial_state
        self._client_root = exporter.client_root
        self._content_root = os.path.join(os.path.dirname(__file__), 'resources', self._client_root)
        self._app = bottle.Bottle()
        self._app.get('/', callback=self._index)
        self._app.get('/initial-state', callback=self._initial_state)
        self._app.get('/export', callback=self._export)
        self._app.get('/static/<path:path>', callback=self._get_static_file)
        self._app.get('/custom-components', callback=self._components)
        self._api.register(self._app)
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True

    def start(self):
        self._thread.start()

    def _run(self):
        bottle.run(self._app, host=self._host, port=self._port)

    def _index(self):
        bottle.response.content_type = 'text/html'
        return self._exporter.get_index_html(websocket_port=self._websocket_port)

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
