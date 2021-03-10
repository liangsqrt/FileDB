import configparser

config = configparser.ConfigParser()
print(type(config))
config["default"] = {
    'port':80,
    'ip':'192.168.1.1',
    'status':"unconnected",
    "data": {
        "data2": [1,2,3]
    }
}
config["baidu.org"] = {}
config["baidu.org"]["members"] = '999'
config["youku.org"] = {}
top_section = config["youku.org"]
top_section["verion"] = "1.9.3"

with open("example.ini", "w", encoding="utf-8") as f:
    config.write(f)

config.read("example.ini")
print(config.sections()) #拿配置文件的首块，DEFAULT是默认不拿的
print("baidu.org" in config) # True
print(config["baidu.org"]["members"]) # 999
print(config["default"]["data"]["data2"])
#
# for k in config["baidu.org"]:
#     print(k) #先打印"baidu.org"下的所有属性，接着打钱DEFAULT的属性

# print(config["baidu.org"]["port"]) # 结果是：80  DEFAULT下的所有属性都是每个首块共有的
# print(config["youku.org"]["port"]) # 结果是：80  DEFAULT下的所有属性都是每个首块共有的