from six import StringIO, string_types


class CustomComponentHandler(object):

    def __init__(self, registry, encoder):
        self.registry = registry
        self.encoder = encoder

    def combined_script_with_script_tag(self):
        result = StringIO()
        result.write('<script type="text/babel">\n')
        result.write(self.combined_script())
        result.write('</script>\n')
        return result.getvalue()

    def combined_script(self):
        result = StringIO()
        scripts = {}
        styles = {}
        element_types = self.registry.element_types
        for element_type in element_types.values():
            for style in element_type._styles:
                style = self._get_style_def(style)
                styles[style['href']] = style
            for script in element_type._scripts:
                script = self._get_script_def(script)
                scripts[script['src']] = script
        for style in styles.values():
            result.write('Awe.addStyle({});\n'.format(self.encoder.to_json(style)))
        for script in scripts.values():
            result.write('Awe.addScript({});\n'.format(self.encoder.to_json(script)))
        for name, element_type in element_types.items():
            result.write('Awe.onScriptsLoaded(() => ((register) => {{{}}})((fn) => Awe.register("{}", fn)));\n'
                         .format(element_type._js(), name))
        if element_types:
            result.write('Awe.scriptSetupDone();\n')
        return result.getvalue()

    @staticmethod
    def _get_style_def(style):
        if isinstance(style, string_types):
            style = {'href': style}
        style.setdefault('rel', 'stylesheet')
        return style

    @staticmethod
    def _get_script_def(script):
        if isinstance(script, string_types):
            script = {'src': script}
        script.setdefault('type', 'text/javascript')
        return script
