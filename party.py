class Party:
    def __init__(self, attrib_dict):
        self._attribute_dict = attrib_dict

    def __getattr__(self, item):
        if item not in self._attribute_dict:
            raise AttributeError
        else:
            return self._attribute_dict[item]
