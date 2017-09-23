import json


class FileStream:
    def __init__(self, file_name):
        self.file_name = file_name

    def overwrite(self, data):
        with open(self.file_name, 'w') as data_file:
            json.dump(list(data), data_file)
            data_file.truncate()

    def to_set(self) -> set:
        with open(self.file_name, 'r') as data_file:
            data_object = json.load(data_file)
        return set(data_object)

    def to_dict(self) -> dict:
        with open(self.file_name, 'r') as data_file:
            data_object = json.load(data_file)
        return dict(data_object)
