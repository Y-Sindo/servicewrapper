from __future__ import unicode_literals
import pymysql
import json
import time
import requests

class MYSQL:
    def __init__(self, MYSQL_PATH, MYSQL_USER, MYSQL_PW, MYSQL_DB):

        self.db = pymysql.connect(MYSQL_PATH, MYSQL_USER, MYSQL_PW, MYSQL_DB) # 打开数据库连接
        self.cursor = self.db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor

        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = self.cursor.fetchone()

        print("Database version : %s " % data)

    def execute(self, sql):
        try:
            self.cursor.execute(sql)  # 执行SQL语句
            self.results = self.cursor.fetchall()  # 获取所有记录列表
            return self.results
        except:
            return None

    def refreshRoute(self):
        try:
            repo = requests.get('http://api.cheosgrid.org:8077/refreshRoute')
            print(repo)
        except:
            pass

    def deleteOneToGrid_API(self, service):
        # SQL 删除语句
        sql = "DELETE FROM grid_api WHERE mark='%s'" % ('package_' + str(service.api_id))
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交修改
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        self.refreshRoute()

    def insertOneToGrid_API(self, service, update=False):
        arguments = service.api_request_parameters_candidate
        arguments_upload = []
        for argument in arguments:
            must = "否"
            if argument["required"]:
                must = "是"
            arguments_upload_one = {
                "名称": argument["query_name"],
                "类型": argument["type"],
                "必填": must,
                "示例值": argument["example"],
                "描述": argument["description"]
            }
            arguments_upload.append(arguments_upload_one)
        arguments_upload = json.dumps(arguments_upload, ensure_ascii=False).replace("'","\\'")     ## arguments

        result_argument_ = service.candidate[service.main_sec_id]
        result_arguments = []
        for result_o in result_argument_:
            if result_o["select"] == 1:
                result_argument = {
                    "名称":result_o["name"],
                    "类型":result_o["type"],
                    "示例值":result_o["example"],
                    "描述":result_o["description"]
                }
                result_arguments.append(result_argument)

        result_arguments = json.dumps(result_arguments, ensure_ascii=False).replace("'","\\'")    ## result_argument

        result_ex = {
            "status": 200,
            "msg": "请求成功，共处理1页.",
            'data': service.api_result_example
        }
        result = json.dumps(result_ex, ensure_ascii=False).replace("'","\\'")   ## result
        error_code = [{'错误码': 200, '说明': '请求成功,共处理x页,其中第a,b页处理失败. 或者 请求成功,共处理x页'}, \
        {'错误码': 201, '说明': '缺失api_crawl_rules_link文件或candidate项，无法处理网页'}, \
        {'错误码': 403, '说明': '请求失败，服务器请求爬虫规则失败'}, \
        {'错误码': 410, '说明': '爬虫失败，超时或请求错误'}, \
        {'错误码': 411, '说明': '解析失败，网页信息错误'}, \
        {'错误码': 425, '说明': '爬虫超时'}, \
        {'错误码': 426, '说明': '缺少必须的参数'}]
        error_code = json.dumps(error_code, ensure_ascii=False).replace("'","\\'")   ## error_code
        if not update:  #直接上传的
            sql = "INSERT INTO grid_api("  \
                  "name, mark, api_address, path,"  \
                  "strip_prefix, description, api_call_way, api_introduction, "  \
                  "status, service_id, checked, arguments, "  \
                  "result_arguments, error_code, result, return_style," \
                  "call_example, create_time) "  \
                  "VALUES ('%s', '%s', '%s', '%s', "  \
                  "1, '%s', 'HTTP GET', '%s',"  \
                  "1,  124, 1, '%s',"  \
                  "'%s', '%s', '%s', '%s'," \
                  "'%s', '%s')" % \
                  (service.api_name, 'package_'+str(service.api_id), service.url, '/package_'+str(service.api_id),
                   service.api_name, service.api_description,
                   arguments_upload,
                   result_arguments, error_code, result, "JSON",
                   "http://api.cheosgrid.org:8077/package_"+str(service.api_id)+"?__max_page=1",
                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:      # 修改的
            sql = "UPDATE grid_api SET name='%s', mark='%s', api_address='%s', path='%s', " \
                  "description='%s', api_introduction='%s'," \
                  "arguments='%s', " \
                  "result_arguments='%s', error_code='%s', result='%s', return_style='%s'," \
                  "call_example='%s', update_time='%s'  WHERE mark='%s'"  % \
                  (service.api_name, 'package_' + str(service.api_id), service.url, '/package_' + str(service.api_id),
                   service.api_name, service.api_description,
                   arguments_upload,
                   result_arguments, error_code, result, "JSON",
                   "http://api.cheosgrid.org:8077/package_" + str(service.api_id) + "?__max_page=1",
                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'package_' + str(service.api_id))
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交修改
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            print("错误回滚:")
            print(e)
            self.db.rollback()
        self.refreshRoute()

    def close(self):
        try:
            self.db.close()  # 关闭数据库连接
        except:
            pass

# mysql = MYSQL(setting.MYSQL_PATH, setting.MYSQL_USER, setting.MYSQL_PW, setting.MYSQL_DB)
# mysql.close()