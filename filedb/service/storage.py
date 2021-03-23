import os
import json
from ruamel.yaml import YAML
from filedb.interface.fileservice import FileService


class JsonFileService(FileService):
    def read(self):
        r = self._read(self.file_path)
        if isinstance(r, list):
            return r
        else:
            return [r]

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

    def install_config(self, config):
        if config.type != "json":
            raise Exception("filetype and storage service unmatched!")
        self.config = config
        self.file_path = config.file_path
        self.filename = config.file_path.split("/")[-1]
        self.check_file()

    def is_existed(self):
        if not os.path.exists(self.file_path):
            raise FileExistsError(self.file_path)

    def check_file(self):
        """
        检查文件是否存在
        """
        file_paths = os.path.split(self.file_path,)
        tmp_path = ""
        for _path in file_paths[:-1]:
            tmp_path = os.path.join(tmp_path, _path)
            if not os.path.exists(tmp_path):
                os.mkdir(tmp_path)
                


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

    def install_config(self, config):
        if config.type != "yaml":
            raise Exception("filetype and storage service unmatched!")
        self.config = config
        self.file_path = config.file_path
        self.filename = config.file_path.split("/")[-1]

    def is_existed(self):
        if not os.path.exists(self.file_path):
            raise FileExistsError(self.file_path)


StorageMap = {
    "json": JsonFileService,
    'yaml': YAMLFileService,
    "xml": None
}