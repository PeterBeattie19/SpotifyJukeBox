import json


class JsonDatabase:
    def __init__(self, db_filename, write_freq=5):
        """
        Constructor
        :param db_filename: database file location and name
        :param write_freq: how often to re-write the database file with updated entries
        """
        self._db_filename = db_filename
        self._data = self._read(self._db_filename)
        self._write_freq = write_freq
        self._num_writes = 0

    @property
    def db_filename(self):
        return self._db_filename

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return len(self._data)

    def select(self, key, value):
        """
        Select all entries where entry[key] == value
        :param key: Hashable object
        :param value: Object
        :return: list
        """
        return list(filter(lambda x: key in x and x[key] == value, self._data))

    def insert(self, obj):
        """
        Inserts entry into Database
        :param obj: object to insert (dictionary)
        :return: None
        """
        try:
            assert isinstance(obj, dict)
        except AssertionError:
            raise TypeError
        else:
            self._num_writes += 1
            self._data.append(obj)
            if self._num_writes % self._write_freq == 0:
                self._update_db_file()

    def _update_db_file(self):
        """
        Write contents of self._data to database file
        :return:
        """
        with open(self._db_filename, 'w') as w_file:
            json.dump(self._data, w_file)

    def delete(self, key, value):
        """
        Delete all entries where entry[key] == value
        :param key: Hashable Object
        :param value: Object
        :return: None
        """
        res = []
        for dict_ in self._data:
            if key in dict_ and dict_[key] == value:
                continue
            res.append(dict_)
        self._data = res
        self._update_db_file()

    @staticmethod
    def _read(filename):
        """
        Read json file
        :param filename: JSON file location and name
        :return: list representing the JSON data
        """
        with open(filename, 'r') as f:
            json_data = json.load(f)
        return json_data

    def __del__(self):
        """Write self._data contents to database file upon object destruction"""
        self._update_db_file()
