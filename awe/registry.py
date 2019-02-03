from typing import Dict, ClassVar, Callable  # noqa

from . import view
from . import variables


class Registry(object):

    def __init__(self):
        self.elements = {}  # type: Dict[str, view.Element]
        self.element_types = {}  # type: Dict[str, ClassVar[view.Element]]
        self.functions = {}  # type: Dict[str, Callable]
        self.variables = {}  # type: Dict[str, variables.Variable]
        self.roots = {}  # type: Dict[str, view.Root]

    def register(self, obj, obj_id=None):
        obj_id, store = self._get_id_and_store(obj, obj_id)
        store[obj_id] = obj

    def unregister(self, obj, obj_id=None):
        obj_id, store = self._get_id_and_store(obj, obj_id)
        del store[obj_id]

    def get_variables(self):
        return {k: var.get_variable() for k, var in self.variables.items()}

    def get_roots(self):
        return {k: root._get_view() for k, root in self.roots.items()}

    def _get_id_and_store(self, obj, obj_id):
        obj_id = obj_id or getattr(obj, 'id', str(id(obj)))
        if isinstance(obj, view.Root):
            store = self.roots
        elif isinstance(obj, view.Element):
            store = self.elements
        elif isinstance(obj, type) and issubclass(obj, view.CustomElement):
            store = self.element_types
        elif isinstance(obj, variables.Variable):
            store = self.variables
        elif callable(obj):
            store = self.functions
        else:
            raise RuntimeError('No registry is defined for objects of type {}'.format(type(obj).__name__))
        return obj_id, store
