from . import view
from . import variables


class Registry(object):

    def __init__(self):
        self.elements = {}
        self.functions = {}
        self.variables = {}

    def register(self, obj, obj_id=None):
        obj_id = obj_id or getattr(obj, 'id', str(id(obj)))
        if isinstance(obj, view.Element):
            self.elements[obj_id] = obj
        elif isinstance(obj, variables.Variable):
            self.variables[obj_id] = obj
        elif callable(obj):
            self.functions[obj_id] = obj
        else:
            raise RuntimeError('No registry is defined for objects of type'.format(type(obj).__name__))

    def get_variables(self):
        return {k: var.get_variable() for k, var in self.variables.items()}
