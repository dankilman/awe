from multiprocessing.pool import ThreadPool

import traceback


class MessageHandler(object):

    def __init__(self, registry, dispatch):
        self.registry = registry
        self.dispatch = dispatch
        self.pool = None
        self.handlers = {
            'call': self.handle_call,
            'updateVariable': self.handle_update_variable
        }

    def start(self):
        self.pool = ThreadPool(1)

    def handle(self, message):
        # messages come from the tornado/asyncio event loop so we
        # process them in a different thread, as it may block
        self.pool.apply_async(self.handler, args=(message,))

    def handler(self, message):
        try:
            message_type = message['type']
            self.handlers[message_type](message)
        except Exception:
            traceback.print_exc()
            client_id = message.get('clientId')
            if client_id:
                self.dispatch({
                    'type': 'displayError',
                    'error': traceback.format_exc()
                }, client_id)

    def handle_call(self, message):
        function = self.registry.functions[message['functionId']]
        inject = getattr(function, 'inject', {'variables': [], 'elements': []})
        variables = {v.id: v.value for v in [self.registry.variables[v] for v in inject['variables']]}
        elements = {e.id: e for e in [self.registry.elements[e] for e in inject['elements']]}
        kwargs = {}
        kwargs.update(elements)
        kwargs.update(variables)
        kwargs.update(message.get('kwargs') or {})
        function(**kwargs)

    def handle_update_variable(self, message):
        variable_id = message['variableId']
        value = message['value']
        variable = self.registry.variables[variable_id]
        variable.update(value)
        self.dispatch({
            'type': 'updateVariable',
            'id': variable_id,
            'value': value,
            'version': variable.version
        })
