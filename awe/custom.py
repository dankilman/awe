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
        scripts = set()
        element_types = self.registry.element_types
        for element_type in element_types.values():
            scripts |= set(element_type._scripts)
        for script in scripts:
            result.write('Awe.addScript("{}");\n'.format(script))
        for name, element_type in element_types.items():
            js = element_type._js()
            result.write('Awe.onScriptsLoaded(() => ((register) => {{{}}})((fn) => Awe.register("{}", fn)));\n'
                         .format(js, name))
        if element_types:
            result.write('Awe.scriptSetupDone();\n')
        return result.getvalue()
