class Variable(object):

    def __init__(self, value, variable_id=None):
        self.id = variable_id or str(id(self))
        self.value = value
        self.version = 0

    def update(self, value):
        self.version += 1
        self.value = value

    def get_variable(self):
        return {
            'value': self.value,
            'id': self.id,
            'version': self.version
        }
