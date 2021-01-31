from flask.views import MethodView
from flask import request
from server.utils import res_json
from server.api.zip.service import *


__doc__ = "这里就是写视图函数的地方"


class ZipFileView(MethodView):
    def post(self):
        """
        :return:
        """
        data = request.get_json()
        zip_service = SomeService()

        return res_json(code=200, msg="ok")

    def get(self):
        data = request.args.get("xxx")
        return res_json(code=200, msg="ok")


class ZipConfigView(MethodView):
    def post(self):
        """
        zip内部的文件解压到哪，需要一个配置文件。这个文件就是一个json文件
        :return:
        """
        return res_json(200, msg="ok")

    def get(self):
        """
        下载zip解压的配置文件
        :return:
        """
        print("下载json文件")
        return res_json(200, msg="ok")
