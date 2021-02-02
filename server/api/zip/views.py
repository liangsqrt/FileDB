from flask.views import MethodView
from flask import request, current_app, send_file
from werkzeug.utils import secure_filename
from server.utils import res_json
from server.api.zip.service import *
import os
import json
import zipfile

__doc__ = "这里就是写视图函数的地方"

## 只允许上传.zip 后缀的文件
ALLOWED_EXTENSIONS = set(['zip'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#判断config.json 文件是否存在 和 是否为空
def check_config_file(config_path):
    if os.path.exists(config_path) and os.path.isfile(config_path):
        with open(config_path) as f:
            conf_data = json.load(f)
            #判断config.json是否为空
            if not conf_data.keys():
                return {'code': 500, 'msg': 'config.json 文件为空!'}
            else:
                return {'code': 200, 'msg': 'config.json 存在', 'conf_data': conf_data}
    return {'code':500, 'msg': 'json文件不存在'}


class ZipFileView(MethodView):
    def post(self):
        """
        :return:
        """
        print("上传zip文件并解压")
        # 接受上传文件并保存
        conf_data = {}
        zip_file = ''
        try:
            config_path = current_app.config.get('CONFIG_PATH')
            result = check_config_file(config_path)
            if result['code'] != 200:
                return res_json(result)
            else:
                conf_data  = result['conf_data']

            f = request.files['zipfile']
            if f and  allowed_file(f.filename):
                fname = secure_filename(f.filename)
                zip_file = os.path.join(current_app.config.get('BASE_DIR'), fname)
                f.save(fname)
                print('zip 文件上传成功')
            else:
                return res_json({'code': 500, 'msg': "上传文件名不正确，只支持.zip 格式，请重试！"})
        except Exception as e:
            print(e)
            return res_json({'code': 500, 'msg': "没发现上传文件，请重试！"})
        
        #开始解压缩文件
        zip_service = SomeService(conf_data, zip_file)
        result = zip_service.uncompress_file()
        
        return res_json(result, data = result['data'])

    def get(self):
        ''' 
        1. 首先判断config.json 文件是否存在和n是否为空
        2. 根据config.json中的路径判断是否开始压缩文件并下载
        '''
        print("下载zip文件")
        conf_data = {}
        config_path = current_app.config.get('CONFIG_PATH')

        ## 下载的文件名称
        zip_filename = 'download_{}.zip'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
        ## 下载的文件全路径
        zip_file = os.path.join(current_app.config.get('BASE_DIR'), zip_filename)

        result = check_config_file(config_path)
        if result['code'] != 200:
            return res_json(result)
        else:
            conf_data = result['conf_data']

        #根据文件列表处理下载
        zip_service = SomeService(conf_data, zip_file)
        not_exists = zip_service.compress_file()

        #如果文件列表有文件不存在，则返回。 data中的列表为不存在的文件
        if not_exists:
            return res_json({'code': 500, 'msg': '压缩文件出错,文件不存在'}, data=not_exists)
        # 如果zip_file创建成功，则下载
        if os.path.exists(zip_file):
            return send_file(zip_file, as_attachment=True)


class ZipConfigView(MethodView):
    def post(self):
        """
        接受客户端发送过来的请求，内容为上传的配置文件。上传过程中会判断文件名是否为config.json。如果是，就保存。否则返回错误
        """
        print("上传json文件")
        config_path = current_app.config.get('CONFIG_PATH')
        try:
            f = request.files['jsonfile']
            if f and f.filename == 'config.json':
                print('filename - {}'.format(f.filename))
                # fname = secure_filename(f.filename)
                f.save(config_path)
                return res_json({'code': 200, 'msg': "上传成功!"})
            else:
                return res_json({'code': 500, 'msg': "上传json文件名不正确，请重试！"})
        except Exception as e:
            return res_json({'code': 500, 'msg': "没发现上传文件，请重试！"})

    def get(self):
        """
        下载zip解压的配置文件
        :return:
        """
        print("下载json文件")
        config_path = current_app.config.get('CONFIG_PATH')
        print(config_path)
        if os.path.exists(config_path) and os.path.isfile(config_path):
            return send_file(config_path, as_attachment=True)
        else:
            return res_json({'code':500, 'msg':"json文件不存在！"})
