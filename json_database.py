import json


class JsonDatabase:
    def __init__(self, db_filename):
        self._db_filename = db_filename
        self._data = self._read(self._db_filename)

    @property
    def db_filename(self):
        return self._db_filename

    @property
    def size(self):
        return len(self._data)

    def select(self, key, value):
        return list(filter(lambda x: x[key] == x[value], self._data))

    def insert(self, obj):
        # TODO Call Write every x inserts and when object is destructed __del__
        try:
            assert isinstance(obj, dict)
        except AssertionError:
            raise TypeError
        else:
            # TODO Write function to return File object for json database file
            with open(self._db_filename, 'w') as w_file:
                json.dump(obj, w_file)
            self._data.append(obj)

    def delete(self):
        pass

    @staticmethod
    def _read(filename):
        with open(filename, 'r') as f:
            json_data = json.load(f)
        return json_data
