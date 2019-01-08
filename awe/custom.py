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
        for name, element_type in self.registry.element_types.items():
            result.write('((register) => {{{}}})((fn) => Awe.register("{}", fn));\n'
                         .format(element_type._js(), name))
        result.write('Awe.store.dispatch({type: "reload"})\n')
        return result.getvalue()
