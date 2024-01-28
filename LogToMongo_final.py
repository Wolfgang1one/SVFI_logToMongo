import json
import pymongo
import datetime
from flask import Flask

app = Flask(__name__)

# 这里都是一些设置，如果需要重新定向，在这里改就行
server_ip = "150.158.42.193"
mongo_user = ""
mongo_pwd = ""
mongo_database = 'LogToMongo'
mongo_port = 27017
mongo_collection = "test"

# 以下变量是用来模拟之前的request回传的json文件
dir_path = ""
json_name = "standard_task_23-01-18"
json_path = dir_path + json_name + ".json"


def ReplaceJsonString(s):
    s = s.replace('"{', '{', -1)
    s = s.replace('}"', '}', -1)
    s = s.replace('\n', ' ', -1)
    s = s.replace('\"', '"', -1)
    return s


# flask的请求和之前在一起写
@app.route('/SVFILogJson', methods=['POST'])
def json_log():
    # if len(request.get_data()) != 0:
    #     log_json_name = request.values.get("log_json_name")
    #     log_json = request.values.get("log_json")
    #     ip = request.remote_addr
    #     with open(os.path.join(JSON_DIR, log_json_name + ".json"), "w", encoding='utf-8') as w:
    #         log_json_data = json.loads(log_json)
    #         log_json_data['ip'] = ip
    #         log_json = json.dumps(log_json_data)
    #         w.write(log_json)

    # 写在这里，主要是获取之前的名称，json文件
    # json的文件名称就是  上面写过的 os.path.join(JSON_DIR, log_json_name + ".json" ，下面的flag循环，防止服务器有问题没有上传成功

    flag = False
    while not flag:
        if not flag:
            with open(json_path, 'r', encoding='UTF-8') as f:
                data = json.loads(f.read())
                data = ReplaceJsonString(data)
                data = json.loads(data)

                # 加入时间dateTime
                now_time = datetime.datetime.now()
                now_time_string = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
                data['dateTime'] = now_time_string
                json_list = list([data])

                # 与数据库连接
                client = pymongo.MongoClient(host=server_ip, port=mongo_port, username=mongo_user, password=mongo_pwd)
                db = client[mongo_database]
                db[mongo_collection].insert_many(json_list)

                flag = True


    # flag的真假值决定最后return的字符串，后期可以改成代码
    if flag:
        return "Json insert into Mongo success! "
    else:
        return "JsonProcessing is error, insert fail! "

    # return json.dumps({"status": "200"}, ensure_ascii=False)


# 最后的接口会输出成功或失败信息
# 这个是我用flask开启的服务，可以省略
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=23333, debug=True)
