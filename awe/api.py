from bottle import request

_endpoints = {}


def _route(method, path):
    def decorator(fn):
        _endpoints.setdefault(method, {})[path] = fn.__name__
        return fn
    return decorator


get = (lambda path: _route('GET', path))
post = (lambda path: _route('POST', path))
put = (lambda path: _route('PUT', path))
delete = (lambda path: _route('DELETE', path))


class API(object):

    def __init__(self, registry, encoder, message_handler):
        self._prefix = '/api'
        self._registry = registry
        self._encoder = encoder
        self._message_handler = message_handler

    def _callback_wrapper(self, callback):
        def wrapper(*args, **kwargs):
            request.content_type = 'application/json'
            result = callback(*args, **kwargs)
            return self._encoder.to_json(result)
        return wrapper

    def register(self, app):
        for method, method_endpoints in _endpoints.items():
            for endpoint, fn_name in method_endpoints.items():
                endpoint = '{}{}'.format(self._prefix, endpoint)
                app.route(endpoint, method=method, callback=self._callback_wrapper(getattr(self, fn_name)))

    @get('/status')
    def _status(self):
        return {'status': 'alive'}

    @get('/elements')
    def _get_elements(self):
        query = request.query
        include_data = query.get('include_data', '').lower() == 'true'
        include_props = query.get('include_props', '').lower() == 'true'
        return {
            'elements': {
                eid: self._get_element(eid, include_data=include_data, include_props=include_props)
                for eid in self._registry.elements
            }
        }

    @get('/elements/<element_id>')
    def _get_element(self, element_id, include_data=True, include_props=True):
        e = self._registry.elements[element_id]
        result = {
            'id': e.id,
            'root_id': e.root_id,
            'element_type': e.element_type,
            'parent_id': e.parent.id if e.parent else None,
            'index': e.index,
            'children_ids': [c.id for c in e.children],
            'prop_children': e._prop_children
        }
        if include_data:
            result['data'] = e.data
        if include_props:
            result['props'] = e.props
        return result

    @post('/elements')
    @put('/elements/<element_id>')
    def _new_element(self, element_id=None):
        body = request.json
        root_id = body.get('root_id')
        parent_id = body.get('parent_id')
        new_root = body.get('new_root')
        obj = body.get('obj')
        params = body.get('params') or {}
        assert obj
        assert not (root_id and parent_id)
        assert not (root_id and new_root)
        if parent_id:
            parent = self._registry.elements[parent_id]
        elif new_root:
            parent = self._registry.roots['root']._new_root()
        else:
            parent = self._registry.roots[root_id or 'root']
        element = parent.new(obj, id=element_id, **params)
        return self._get_element(element.id)

    @delete('/elements/<element_id>')
    def _remove_element(self, element_id):
        element = self._registry.elements[element_id]
        element.remove()
        return {'id': element_id, 'status': 'success'}

    @put('/elements/<element_id>/prop/<prop_name>')
    def _new_prop(self, element_id, prop_name):
        element = self._registry.elements[element_id]
        result = element.new_prop(prop_name)
        return {
            'name': prop_name,
            'id': result.id
        }

    @put('/elements/<element_id>/data')
    def _update_data(self, element_id):
        element = self._registry.elements[element_id]
        body = request.json
        data = body.get('data')
        assert data
        element.update_data(data)
        return {'id': element_id, 'status': 'success'}

    @put('/elements/<element_id>/props')
    def _update_props(self, element_id):
        element = self._registry.elements[element_id]
        body = request.json
        props = body.get('props')
        prop_path = body.get('path')
        prop_value = body.get('value')
        assert props or (prop_path and prop_value)
        assert not (props and (prop_path or prop_value))
        if props:
            element.update_props(props)
        else:
            element.update_prop(prop_path, prop_value)
        return {'id': element_id, 'status': 'success'}

    @post('/elements/<element_id>/call/<method>')
    def _call_method(self, element_id, method):
        element = self._registry.elements[element_id]
        body = request.json
        kwargs = body.get('kwargs') or {}
        if method.startswith('_'):
            raise RuntimeError('cannot call private methods')
        assert hasattr(element, method)
        fn = getattr(element, method)
        fn(**kwargs)
        return {'id': element_id, 'status': 'success'}

    @get('/variables')
    def _get_variables(self):
        return {'variables': self._registry.get_variables()}

    @get('/variables/<variable_id>')
    def _get_variable(self, variable_id):
        return self._registry.variables[variable_id].get_variable()

    @post('/variables')
    @put('/variables/<variable_id>')
    def _new_variable(self, variable_id=None):
        body = request.json
        value = body.get('value')
        assert value
        result = self._registry.roots['root']._new_variable(value, variable_id)
        return result.get_variable()

    @post('/variables/<variable_id>')
    def _update_variable(self, variable_id):
        body = request.json
        value = body.get('value')
        assert variable_id in self._registry.variables
        assert value
        self._message_handler.handle({
            'type': 'updateVariable',
            'variableId': variable_id,
            'value': value
        })
        return {'id': variable_id, 'status': 'success'}

    @post('/functions/<function_id>')
    def _call_function(self, function_id):
        body = request.json
        kwargs = body.get('kwargs') or {}
        assert function_id in self._registry.functions
        self._message_handler.handle({
            'type': 'call',
            'functionId': function_id,
            'kwargs': kwargs
        })
        return {'id': function_id, 'status': 'success'}
