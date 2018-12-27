import json
import re

BASE_STATIC_URL = 'https://s3.amazonaws.com/awe-static-files/dist'


def resource_regex_pattern(extension, prefix):
    regex = r'/static/(static/{extension}/{prefix}\.[0-9a-f]{{8}}\.chunk\.{extension})'.format(
        extension=extension,
        prefix=prefix
    )
    return re.compile(regex)


frozen_state_format = 'window.frozenState={}'.format
favicon = '/static/favicon.ico'
resource_patterns = {
    'vendor.css': resource_regex_pattern('css', '1'),
    'main.css': resource_regex_pattern('css', 'main'),
    'vendor.js': resource_regex_pattern('js', '1'),
    'main.js': resource_regex_pattern('js', 'main'),
}


class Exporter(object):

    def __init__(self, export_fn):
        self.export_fn = export_fn or self.default_export_fn

    def export(self, index, state):
        from . import __version__
        base_url = '{}/{}'.format(BASE_STATIC_URL, __version__)
        index = index.replace(favicon, '{}/{}'.format(base_url, 'favicon.ico'), 1)
        for key, pattern in resource_patterns.items():
            index = pattern.sub('{}/{}'.format(base_url, r'\1'), index, 1)
        json_state = json.dumps(state, separators=(',', ':'))
        index = index.replace(frozen_state_format('null'), frozen_state_format(json_state), 1)
        return self.export_fn(index)

    @staticmethod
    def default_export_fn(index_html):
        return index_html
