def inject(variables=None, elements=None):
    def wrapper(fn):
        fn.inject = {
            'variables': variables or [],
            'elements': elements or []
        }
        return fn
    return wrapper
