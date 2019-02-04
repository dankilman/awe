import os
import re

from . import resources

BASE_STATIC_URL = 'https://s3.amazonaws.com/awe-static-files/dist'
BASE_URL = os.environ.get('AWE_EXPORT_BASE_URL')


def resource_regex_pattern(prefix, extension):
    regex = r'/static/(static/{extension}/{prefix}\.[0-9a-f]{{8}}\.chunk\.{extension})'.format(
        prefix=prefix,
        extension=extension
    )
    return re.compile(regex)


frozen_state_format = 'window.frozenState={}'.format
awe_websocket_port_format = 'window.aweWebsocketPort={}'.format
favicon = '/static/favicon.ico'
index_resources = [
    ('1', 'css'),
    ('main', 'css'),
    ('1', 'js'),
    ('main', 'js')
]
resource_patterns = [resource_regex_pattern(*args) for args in index_resources]


class Exporter(object):

    def __init__(self, export_fn, get_initial_state, custom_component, encoder):
        from . import __version__
        self.client_root = 'client/awe/build'
        self.export_fn = export_fn or self.default_export_fn
        self.get_initial_state = get_initial_state
        self.custom_component = custom_component
        self.encoder = encoder
        self.index = resources.get(os.path.join(self.client_root, 'index.html'))
        self.base_url = BASE_URL or '{}/{}'.format(BASE_STATIC_URL, __version__)

    def export(self, export_fn=None):
        export_fn = export_fn or self.export_fn
        index = self.index.replace(favicon, '{}/{}'.format(self.base_url, 'favicon.ico'), 1)
        for pattern in resource_patterns:
            index = pattern.sub('{}/{}'.format(self.base_url, r'\1'), index, 1)
        state = self.get_initial_state()
        json_state = self.encoder.to_json(state)
        index = index.replace(frozen_state_format('null'), frozen_state_format(json_state), 1)
        index = index.replace(
            '<script type="text/babel" src="/custom-components"></script>',
            self.custom_component.combined_script_with_script_tag(), 1)
        return export_fn(index)

    def get_index_html(self, websocket_port):
        return self.index.replace(
            awe_websocket_port_format('null'),
            awe_websocket_port_format(websocket_port)
        )

    @staticmethod
    def default_export_fn(index_html):
        return index_html
