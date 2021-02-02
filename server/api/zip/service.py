from datetime import datetime
from  zipfile import ZipFile
import os

class SomeService(object):
    def __init__(self, config_data, zipfile):
        self.config_data = config_data
        self.filenamelist = self.config_data.keys()
        self.filepathlist = self.config_data.values()

        self.zipfile = zipfile
        self.not_exists = []
        self.uncompress_failed = []

    def uncompress_file(self):
        # 1, 首先判断 config.json 中的定义的文件是否都在zip文件中，如果有些不存在则返回 不存在的文件列表
        # 2. 如果都存在，则开始解压。解压过程中，如果出错，则返回解压出错的文件列表

        with ZipFile(self.zipfile, 'r') as zipObject:
            zip_filelist = zipObject.namelist()
            for elem in self.filenamelist:
                if elem in zip_filelist:
                    continue
                else:
                    self.not_exists.append(elem)
            if self.not_exists:
                print('Some file not in config josn not include in zip, exit! ')
                return {'code': 500, 'msg': 'zip文件中的列表不全，缺失的文件列表在data中', 'data':self.not_exists}

            for filename, filepath in self.config_data.items():
                try:
                    # zipObject.extract(filename, filepath)
                    with open(filepath, 'wb+') as f:
                        f.write(zipObject.read(filename))
                    
                except Exception as e:
                    print('Uncompress {} to {} failed! Reason: {}'.format(filename, filepath, e))
                    self.uncompress_failed.append({'filename':filename, 'reason':str(e)})
            if self.uncompress_failed:
                return {'code': 500, 'msg': '解压zip文件中的出错，出错的文件列表在data中', 'data': self.uncompress_failed}
            else:
                print('zip 文件解压成功')
                return {'code': 200, 'msg': '解压成功', 'data':''}


    def compress_file(self):
        # 判断filepathlist中的文件是否在服务器上都存在，如果有不存在的放入到 not_exists 列表中并返回。如果都存在，则开始创建zip文件
        for filepath in self.filepathlist:
            if os.path.exists(filepath) and os.path.isfile(filepath):
                continue
            else:
                self.not_exists.append(filepath)
        if self.not_exists:
            return self.not_exists

        with ZipFile(self.zipfile, 'w') as zipObj:
            for filepath in self.filepathlist:
                try:
                    zipObj.write(filepath)
                except Exception as e:
                    print('zip failed for {} - {}'.format(filepath, e))
        return self.not_exists
