import os
import time
import webbrowser

from . import messages
from . import registry
from . import view
from . import webserver
from . import websocket


class Page(view.Element):

    def __init__(self, title='Awe', port=8080, ws_port=9000, width=None, style=None):
        super(Page, self).__init__(parent=None, element_id='', props=None, style=None)
        self._port = port
        self._title = title
        self._style = self._set_default_style(style, width)
        self._registry = registry.Registry()
        self._message_handler = messages.MessageHandler(self._registry, self._dispatch)
        self._server = webserver.WebServer(self._get_initial_state, port=port)
        self._ws_server = websocket.WebSocketServer(self._message_handler, port=ws_port)
        self._started = False
        self._version = 0

    def start(self, block=False, open_browser=True, develop=False):
        """
        Start the page services

        :param block: Should the method invocation block (default: False)
        :param open_browser: Should a new tab be opened in a browser pointing to the started page (default: True)
        :param develop: During development, changes to port for open browser to 3000 (due to npm start, default False)
        """
        self._message_handler.start()
        self._server.start()
        self._ws_server.start()
        self._started = True
        if open_browser:
            port = 3000 if (develop or os.environ.get('AWE_DEVELOP')) else self._port
            webbrowser.open_new_tab('http://localhost:{}'.format(port))
        if block:
            self.block()

    def _get_initial_state(self):
        return {
            'children': [t._get_view() for t in self.children],
            'variables': self._registry.get_variables(),
            'version': self._version,
            'style': self._style,
            'title': self._title,
        }

    def _increase_version(self):
        self._version += 1

    def _register(self, obj, obj_id=None):
        self._registry.register(obj, obj_id)

    def _dispatch(self, action, client_id=None):
        self._increase_version()
        if not self._started:
            return
        action['version'] = self._version
        self._ws_server.dispatch_from_thread(action, client_id)

    @staticmethod
    def _set_default_style(style, width):
        style = style or {}
        defaults = {
            'width': width or 1200,
            'paddingTop': '6px',
            'paddingBottom': '6px'
        }
        for key, default in defaults.items():
            style.setdefault(key, default)
        return style

    @staticmethod
    def block():
        """
        Utility method to block after page has been started
        """
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
