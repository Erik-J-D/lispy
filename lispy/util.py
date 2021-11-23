from collections import ChainMap
from functools import reduce


class DeepChainMap(ChainMap):
    '''Variant of ChainMap that allows direct updates to inner scopes'''

    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)


def reduce_min_args(op, min_args=2, name=None):
    def fun(*args):
        if len(args) < min_args:
            human_name = name or op.__name__
            raise Exception(
                f"{human_name} expected {min_args} arguments, "
                f"got {len(args)}")
        return reduce(op, args)
    return fun
