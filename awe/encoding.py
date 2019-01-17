import collections
import json


class JSONEncoder(json.JSONEncoder):

    def __init__(self, serializers):
        super(JSONEncoder, self).__init__(separators=(',', ':'))
        self.serializers = serializers

    def default(self, o):
        for cls, serializer in self.serializers.items():
            if isinstance(o, cls):
                return serializer(o)
        return super(JSONEncoder, self).default(o)


def element_serializer(element):
    return {'_awe_root_': element.root_id}


class Encoder(object):

    def __init__(self, element_cls, serializers):
        serializers = serializers or {}
        serializers.setdefault(collections.deque, list)
        serializers.setdefault(element_cls, element_serializer)
        self._json_encoder = JSONEncoder(serializers)

    def to_json(self, obj):
        return self._json_encoder.encode(obj)

    @staticmethod
    def from_json(obj):
        return json.loads(obj)
