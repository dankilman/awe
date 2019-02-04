import requests


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8080
DEFAULT_WEBSOCKET_PORT = 9000


class APIClient(object):

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        """
        REST API client.

        Can be used to update a running page from an external script.

        :param host: ``awe`` server host.
        :param port: ``awe`` server port.
        """
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self._base_url = 'http://{}:{}/api'.format(self.host, self.port)

    def get_status(self):
        """
        Verify liveness of ``awe``'s server.
        """
        return self._request('GET', '/status')

    def get_elements(self, include_data=False, include_props=False):
        """
        Get all elements currently registered.

        :param include_data: Should element data be included in the response.
        :param include_props: Should element props be included in the response.
        """
        return self._request('GET', '/elements', query={
            'include_data': str(include_data).lower(),
            'include_props': str(include_props).lower()
        })['elements']

    def get_element(self, element_id):
        """
        Get a single registered element.

        :param element_id: The element id.
        """
        return self._request('GET', '/elements/{}'.format(element_id))

    def new_element(self, obj, params=None, element_id=None, root_id=None, parent_id=None, new_root=False):
        """
        Create a new element. Equivalent to calling the ``new()`` method on elements.

        :param obj: The ``obj`` argument as expected by the ``new()`` method.
        :param params: Params to pass on to the ``new()`` method invocation.
        :param element_id: Optionally specify an ``element_id``. (one will be generated otherwise)
        :param root_id: Optionally specify a different root to create the element under.
                        If not specified, and ``parent_id`` is not supplied, the main ``page`` root will be used.
        :param parent_id: Optionally specify the element to call the ``new()`` method on.
        :param new_root: Pass ``True`` to create the element under a new root.
        """
        method = 'PUT' if element_id else 'POST'
        endpoint = '/elements/{}'.format(element_id) if element_id else '/elements'
        return self._request(method, endpoint, body={
            'obj': obj,
            'params': params,
            'root_id': root_id,
            'parent_id': parent_id,
            'new_root': new_root
        })

    def remove_element(self, element_id):
        """
        Remove an element from the page.

        :param element_id: The element id.
        """
        return self._request('DELETE', '/elements/{}'.format(element_id))

    def new_prop(self, element_id, name):
        """
        Create a new prop child. Equivalent to calling ``new_prop()`` on an element.

        :param element_id: The element id to call ``new_prop`` on.
        :param name: The prop name.
        """
        return self._request('PUT', '/elements/{}/prop/{}'.format(element_id, name))

    def update_data(self, element_id, data):
        """
        Update the element data. Equivalent to calling ``update_data()`` on an element.

        :param element_id: The element id to call ``update_data`` on.
        :param data: The data to set on the element.
        """
        return self._request('PUT', '/elements/{}/data'.format(element_id), body={
            'data': data
        })

    def update_props(self, element_id, props):
        """
        Update the element props. Equivalent to calling ``update_props()`` on an element.

        :param element_id: The element id to call ``update_props`` on.
        :param props: The props to set on the element.
        """
        return self._request('PUT', '/elements/{}/props'.format(element_id), body={
            'props': props
        })

    def update_prop(self, element_id, path, value):
        """
        Update an element prop. Equivalent to calling ``update_prop()`` on an element.

        :param element_id: The element id to call ``update_prop`` on.
        :param path: The prop path.
        :param value: The prop value.
        """
        return self._request('PUT', '/elements/{}/props'.format(element_id), body={
            'path': path,
            'value': value
        })

    def call_method(self, element_id, method_name, kwargs=None):
        """
        Call a method on an element. Useful when working with elements such as a table or a chart that expose
        methods to modify their internal state.

        :param element_id: The element id to call the specified method on.
        :param method_name: The method to call.
        :param kwargs: Keyword arguments to pass to the method invocation.
        """
        return self._request('POST', '/elements/{}/call/{}'.format(element_id, method_name), body={
            'kwargs': kwargs
        })

    def get_variables(self):
        """
        Get all variables currently registered.
        """
        return self._request('GET', '/variables')['variables']

    def get_variable(self, variable_id):
        """
        Get a single registered variable.

        :param variable_id: The variable id.
        """
        return self._request('GET', '/variables/{}'.format(variable_id))

    def new_variable(self, value, variable_id=None):
        """
        Create a new variable.

        :param value: The variable's initial value.
        :param variable_id: Optionally, supply a variable id, one will be generated otherwise.
        """
        method = 'PUT' if variable_id else 'POST'
        endpoint = '/variables/{}'.format(variable_id) if variable_id else '/variables'
        return self._request(method, endpoint, body={
            'value': value
        })

    def update_variable(self, variable_id, value):
        """
        Update a variable.

        :param variable_id: The variable id.
        :param value: The new variable value.
        """
        return self._request('POST', '/variables/{}'.format(variable_id), body={
            'value': value
        })

    def call_function(self, function_id, kwargs=None):
        """
        Call a registered function.

        :param function_id: The function id.
        :param kwargs: Additional keyword arguments to pass to the function invocation.
        """
        return self._request('POST', '/functions/{}'.format(function_id), body={
            'kwargs': kwargs
        })

    def _request(self, method, endpoint, body=None, query=None):
        url = '{}{}'.format(self._base_url, endpoint)
        response = requests.request(method, url, params=query, json=body)
        response.raise_for_status()
        return response.json()
