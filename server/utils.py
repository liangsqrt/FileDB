from flask import jsonify


def add_url_include(app, model, url_head=None, namespace=""):
    for url_end, cls_value, name in model:
        url_one = url_head + url_end
        as_view_name = namespace + name
        app.add_url_rule(url_one, view_func=cls_value.as_view(as_view_name))


def res_json(error_code, data=None, msg=None,**kwargs):
    """
    use for return json response with formatted res/code/data
    :param error_code: formatted res_code
    :param data: return data
    :param msg: a specialized tips msg
    :return: response
    """
    if not isinstance(error_code, dict):
        return jsonify(code=100103, msg="Not Satisfied Type")
    res_code = error_code.get('code')
    res_msg = error_code.get('msg')
    if msg:
        res_msg = msg
    if res_code is None or not res_msg:
        return jsonify(code=100104, msg="None Params")
    if data is None:
        return jsonify(code=res_code, msg=res_msg,**kwargs)
    return jsonify(code=res_code, msg=res_msg, data=data,**kwargs)
