import json

from six import StringIO


class CustomComponentHandler(object):

    def __init__(self, registry):
        self.registry = registry

    def combined_script_with_script_tag(self):
        result = StringIO()
        result.write('<script type="text/babel">\n')
        result.write(self.combined_script())
        result.write('</script>\n')
        return result.getvalue()

    def combined_script(self):
        result = StringIO()
        scripts = {}
        element_types = self.registry.element_types
        for element_type in element_types.values():
            for script in element_type._scripts:
                script = self._get_script_def(script)
                scripts[script['src']] = script
        for script in scripts.values():
            result.write('Awe.addScript({});\n'.format(json.dumps(script, separators=(',', ':'))))
        for name, element_type in element_types.items():
            result.write('Awe.onScriptsLoaded(() => ((register) => {{{}}})((fn) => Awe.register("{}", fn)));\n'
                         .format(element_type._js(), name))
        if element_types:
            result.write('Awe.scriptSetupDone();\n')
        return result.getvalue()

    @staticmethod
    def _get_script_def(script):
        if isinstance(script, str):
            script = {'src': script}
        if 'type' not in script:
            script['type'] = 'text/javascript'
        return script
