# from filedb.interface.fileservice import FileServiceInterface
import os
import json
from ruamel.yaml import YAML
from filedb.interface.fileservice import FileService


class JsonFileService(FileService):
    def read(self):
        return self._read(self.file_path)

    def save(self, data):
        self._write_file(self.file_path, data)

    @staticmethod
    def _write_file(file_path, data):
        with open(file_path, 'w+', encoding="utf-8") as w_f:
            w_f.write(json.dumps(data, indent=4, ensure_ascii=False))

    @staticmethod
    def _read(file_path):
        with open(file_path, 'r', encoding="utf-8") as r_f:
            file_data = json.load(r_f)
            return file_data

    def from_config(self, config):
        self.config = config

    def is_existed(self):
        if not os.path.exists(self.file_path):
            raise FileExistsError(self.file_path)


class YAMLFileService(FileService):
    @staticmethod
    def _read_file(file_path):
        ryaml = YAML(pure=True)
        ryaml.allow_unicode = True
        with open(file_path, 'r', encoding="utf-8") as r_f:
            file_data = r_f.read()
            file_data = ryaml.load(file_data)
            return file_data

    @staticmethod
    def _write_file(file_path, data):
        ryaml = YAML(pure=True)
        ryaml.allow_unicode = True
        with open(file_path, 'w+',
                  encoding="utf-8") as w_f:
            ryaml.dump(data, w_f)

    def read(self):
        self._read_file(self.file_path)

    def save(self, data):
        self._write_file(data)

    def from_config(self, Config):
        print("from config")

    def is_existed(self):
        if not os.path.exists(self.file_path):
            raise FileExistsError(self.file_path)


fileservice_map = {
    "json": JsonFileService,
    'yaml': YAMLFileService,
    "xml": None
}