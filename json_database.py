import configparser
import json


class JsonDatabase:
    def __init__(self, db_filename, write_freq=1):
        """
        Constructor
        :param db_filename: database file location and name
        :param write_freq: how often to re-write the database file with updated entries (Redundant since __del__
        won't work
        """
        self._db_filename = db_filename
        self._data = self._read(self._db_filename)
        self._write_freq = write_freq
        self._num_writes = 0
        self._config_file_name = "database_config.ini"
        self._last_used_pk = self._get_pk_from_config()
        self._primary_key_name = "id"

    def _get_pk_from_config(self):
        """
        read config file and get last used primary key, very poor implementation but ok for proof of concept.
        :return: int
        """
        config = configparser.ConfigParser()
        config.read(self._config_file_name)
        return int(config['primary key']['last_used_pk'])

    @staticmethod
    def _add_key_to_dict(key, value, dict_):
        dict_[key] = value
        return dict_

    def _add_pk(self, dict_):
        """
        add a primary key field to dict_
        :param dict_: dictionary to which a primary key field will be added to.
        :return: updated dictionary
        """
        self._last_used_pk += 1
        dict_ = self._add_key_to_dict(self._primary_key_name, self._last_used_pk, dict_)
        self._update_config_file("primary key", {"last_used_pk": self._last_used_pk})
        return dict_

    def _update_config_file(self, header_name, dict_):
        config = configparser.ConfigParser()
        config[header_name] = dict_
        config.write(open(self._config_file_name, 'w'))

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
            obj = self._add_pk(obj)
            self._data.append(obj)
            if self._num_writes % self._write_freq == 0:
                self._update_db_file()

    def _update_db_file(self):
        """
        Write contents of self._data to database file
        :return:
        """
        print(self._data)
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

    # R.I.P :(
    '''
    def __del__(self):
        """Write self._data contents to database file upon object destruction"""
        self._update_db_file()
    '''
