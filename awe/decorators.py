def inject(variables=None, elements=None):
    """
    Used with elements that accept function callbacks.

    :param variables: Variables that will be injected to the function arguments by name.
    :param elements: Elements that will be injected to the function arguments by name.
    """
    def wrapper(fn):
        fn.inject = {
            'variables': variables or [],
            'elements': elements or []
        }
        return fn
    return wrapper
