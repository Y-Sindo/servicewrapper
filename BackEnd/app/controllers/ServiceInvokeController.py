from app import app
from flask_cors import CORS
from flask import jsonify, request
from app.models.api import Api
from app.service.Service import Crawler, image_filter, text_filter, select_result_parameter, iterator_judge
import requests
from urllib.parse import urljoin
from pyquery import PyQuery as pq
from app.service.ConnectMySQL import MYSQL
import app.service.setting  as setting
from app.service.CallService import  CallService
from app.service.Util import shutdown_crawl

CORS(app, resources=r'/*')

# @app.route('/todo/api/v1/device', methods=['GET', 'POST'])
# def device_get():
#     if request.method == 'GET':
#         device_all = Device.objects().all()
#         return jsonify({'device': Device.objects.all()}), 200, {'Content-Type': 'application/json;chaset=utf-8'}
#     elif request.method == 'POST':
#         if not 'devicename' in request.json or not 'macaddr' in request.json:
#             print(request.json)
#             app.logger.debug(request.json)
#             abort(400)
#         device = Device(devicename=request.json['devicename'], macaddr=request.json['macaddr']).save();
#         return jsonify({}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

@app.route('/service', methods=['POST', 'GET', 'PUT', 'DELETE'])
def add_service():
    '''
    POST: JSON
        :parameter  api_name : string
                    api_url : string
                    api_description : string
                    api_crawl_rules_link : string
                    candidate : list
                    main_sec_id: int
                    img_link : string
                    json_link : string
        :example
                    {
                        "api_name":"weather_4",
                        "api_description":"api",
                        "candidate":[
                            {   "id":1,
                                "name":"text_1",
                                "description":"none",
                                "type":"text",
                                "example":"default",
                                "select":0
                            },{
                                "id":3,
                                "name":"text_1",
                                "description":"none",
                                "type":"text",
                                "example":"default",
                                "select":1
                            },{
                                "id":2,
                                "name":"text_1",
                                "description":"none",
                                "type":"text",
                                "example":"default",
                                "select":0
                            }],
                        "api_crawl_rules_link":"http://127.0.0.1:5000/weather1",
                        "img_link":"http://213.ds/com",
                        "json_link":"http://test.com",
                        "api_url":"http://test.cn",      ## url and link 一定要是http://   或者 https://
                    }
    GET:
        :parameter service : string
        :exapmle
            http://service.cheosgrid.org:8089/service?api_name=weather
            http://service.cheosgrid.org:8089/service?api_id=1
    PUT:JSON
        :parameter
                    api_id: 2     ## 一定要有api_id
                    api_name : string
                    api_url : string
                    api_description : string
                    api_crawl_rules_link : string
                    api_parameters : list
                    img_link : string
                    main_sec_id: int
                    json_link : string
        :example
                    {
                        "api_name":"weather_4",
                        "api_description":"api",
                        "api_parameters":[
                            {   "id":1,
                                "name":"text_1",
                                "description":"none",
                                "type":"text",
                                "example":"default",
                                "select":0
                            },{
                                "id":3,
                                "name":"text_1",
                                "description":"none",
                                "type":"text",
                                "example":"default",
                                "select":1
                            },{
                                "id":2,
                                "name":"text_1",
                                "description":"none",
                                "type":"text",
                                "example":"default",
                                "select":0
                            }],
                        "api_crawl_rules_link":"http://127.0.0.1:5000/weather1",
                        "img_link":"http://213.ds/com",
                        "json_link":"http://test.com",
                        "api_url":"http://test.cn",
                        "api_id":5
                    }
    DELETE:
        :parameter api_id : int
        :example
            http://service.cheosgrid.org:8089/service?api_id=1
    :return:
        NORMAL:
                {'status':10000, 'msg':'请求成功', 'data':service},200  GET PUT POST
                {'status':10000, 'msg':'请求成功', 'data':''}, 200  DELETE
                {'status': 400, 'msg': '参数错误', 'data':''}, 200
                {'status': 401, 'msg': '服务不存在', 'data': ''}, 200
                {'status': 402, 'msg': '已有该服务', 'data': ''}, 200
    '''

    if request.method == "POST":
        # try:
        # #####名字重复报错"服务已存在"
        # service_exist = Api.objects(api_name=request.json['api_name']).first()
        # if service_exist:
        #     app.logger.error("service - 已有该服务")
        #     return jsonify({'status': 402, 'msg': '已有该服务', 'data': ''})
        # ##########################

        service = Api(api_name=request.json['api_name'],
                      api_description=request.json['api_description'],
                      candidate=request.json['candidate'],
                      main_sec_id=request.json['main_sec_id'],
                      form_rules_link=request.json['form_rules_link'],
                      api_url=request.json['api_url'],
                      api_crawl_rules_link=request.json['api_crawl_rules_link'],
                      img_link=request.json['img_link'],
                      json_link=request.json['json_link']).save()
        service.update(url="http://service.cheosgrid.org:8089/call_service/"+str(service.api_id))

        candidates = service.candidate
        ## 针对service进行修改，对每个candidate增加query_name 字段
        candidates  = candidate_add_query_name(candidates)
        api_request_parameters_candidate_level2 = get_api_request_parameters_candidate_Level2(candidates, service.main_sec_id)

        service.update(candidate=candidates)

        api_request_parameters_candidate_level0 = [{
            "type": "int",
            "query_name": "__max_page",
            "level": 0,
            "required": False,
            "example": 3,
            "description": "[系统级别参数]: 最大页数限制，默认为5页，请设置较小的页数以避免返回时间过长。"
        }]
        api_request_parameters_candidate_level1 = []
        if service.form_rules_link:
            form_list = requests.get(service.form_rules_link).json()
            if form_list["form_check"] == 1:  # 如果有参数
                input_list = form_list["forms"][form_list["main_form_index"]]["input_list"]
                for input in input_list:  # 模拟表单操作
                    if input["type"] != "hidden":  # hidden一般不要动
                        api_request_parameters_candidate_level1.append({
                            "type": input["type"],
                            "query_name": input["query_name"],
                            "level": 1,
                            "required": input["required"],
                            "example": input["value"],
                            "description": "[查询输入参数]: " + input["description"]
                        })
        api_request_parameters_candidate = api_request_parameters_candidate_level0 + api_request_parameters_candidate_level1 + api_request_parameters_candidate_level2
        service.update(api_request_parameters_candidate=api_request_parameters_candidate)

        service_all = Api.objects(api_id=service.api_id).first()

        #########################
        ## To get the result_example
        callservice = CallService(service_all)
        resp = callservice.call_only_one_page_for_getting_result_demo();
        callservice.shutDown()
        call_result = ""
        if resp.startswith("Error"):
            call_result = ", "+resp

        #########################
        if setting.PRODUCTION:
            mysql = MYSQL(setting.MYSQL_PATH, setting.MYSQL_USER, setting.MYSQL_PW, setting.MYSQL_DB)
            mysql.insertOneToGrid_API(Api.objects(api_id=service.api_id).first())
            mysql.close()

        return jsonify({"status":10000, 'msg': '请求成功'+call_result, 'data': Api.objects(api_id=service.api_id).first()}), 200, {'Content-Type': 'application/json;chaset=utf-8'}
        # except:
        #     app.logger.error("service - 参数错误")
        #     return jsonify({'status': 400, 'msg': '参数错误', 'data': ''})

    elif request.method == "GET":
        if request.args.get('api_name'):
            service_exist = Api.objects(api_name=request.args.get('api_name')).first()
        elif request.args.get('api_id'):
            service_exist = Api.objects(api_id=request.args.get('api_id')).first()
        else:
            app.logger.error("service - 参数错误")
            return jsonify({'status': 400, 'msg': '参数错误', 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}
        return jsonify({'status': 10000, 'msg': '请求成功', 'data': service_exist}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

    elif request.method == "DELETE":
        if request.args.get('api_id'):
            service_exist = Api.objects(api_id=request.args.get('api_id')).first()
            if service_exist:
                if setting.PRODUCTION:
                    mysql = MYSQL(setting.MYSQL_PATH, setting.MYSQL_USER, setting.MYSQL_PW, setting.MYSQL_DB)
                    mysql.deleteOneToGrid_API(service_exist)
                    mysql.close()

                service_exist.delete()

            return jsonify({'status': 10000, 'msg': '请求成功', 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}
        else:
            app.logger.error("service - 参数错误")
            return jsonify({'status': 400, 'msg': '参数错误', 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

    elif request.method == "PUT":
        try:
            service_exist = Api.objects(api_id=request.json['api_id']).first()
            if not service_exist:
                app.logger.error("service - 服务不存在")
                return jsonify({'status': 401, 'msg': '服务不存在', 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}
            else:
                service_exist.update(api_name=request.json['api_name'],
                              api_description=request.json['api_description'],
                              candidate=request.json['candidate'],
                              api_url=request.json['api_url'],
                              form_rules_link=request.json['form_rules_link'],
                              main_sec_id=request.json['main_sec_id'],
                              api_crawl_rules_link=request.json['api_crawl_rules_link'],
                              img_link=request.json['img_link'],
                              json_link=request.json['json_link'])
                candidates = service_exist.candidate
                ## 针对service进行修改，对每个candidate增加query_name 字段
                candidates = candidate_add_query_name(candidates)
                api_request_parameters_candidate_level2 = get_api_request_parameters_candidate_Level2(candidates, service_exist.main_sec_id)

                service_exist.update(candidate=candidates)

                api_request_parameters_candidate_level0 = [{
                    "type": "int",
                    "query_name": "__max_page",
                    "level": 0,
                    "required": False,
                    "example": 3,
                    "description": "[系统级别参数]: 最大页数限制，默认为5页，请设置较小的页数以避免返回时间过长。"
                }]
                api_request_parameters_candidate_level1 = []
                if service_exist.form_rules_link:
                    form_list = requests.get(service_exist.form_rules_link).json()
                    if form_list["form_check"] == 1:  # 如果有参数
                        input_list = form_list["forms"][form_list["main_form_index"]]["input_list"]
                        for input in input_list:  # 模拟表单操作
                            if input["type"] != "hidden":  # hidden一般不要动
                                api_request_parameters_candidate_level1.append({
                                    "type": input["type"],
                                    "query_name": input["query_name"],
                                    "level": 1,
                                    "required": input["required"],
                                    "example": input["value"],
                                    "description": "[查询输入参数]: "+input["description"]
                                })
                api_request_parameters_candidate = api_request_parameters_candidate_level0 + api_request_parameters_candidate_level1 + api_request_parameters_candidate_level2
                service_exist.update(api_request_parameters_candidate=api_request_parameters_candidate)

                service_exist_all = Api.objects(api_id = service_exist.api_id).first()
                #########################
                ## To get the result_example
                callservice = CallService(service_exist_all)
                resp = callservice.call_only_one_page_for_getting_result_demo();
                call_result = ""
                if resp.startswith("Error"):
                    call_result = ", " + resp
                #########################
                if setting.PRODUCTION:
                    mysql = MYSQL(setting.MYSQL_PATH, setting.MYSQL_USER, setting.MYSQL_PW, setting.MYSQL_DB)
                    mysql.insertOneToGrid_API(service_exist_all, True)
                    mysql.close()

                return jsonify({'status': 10000, 'msg': '请求成功'+call_result, 'data': Api.objects(api_id=service_exist.api_id).first()}), 200, {'Content-Type': 'application/json;chaset=utf-8'}
        except:
            app.logger.error("service - 参数错误")
            return jsonify({'status': 400, 'msg': '参数错误', 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

@app.route('/all_service', methods=['GET'])
def get_all_service():
    '''
    获得所有api
    http://service.cheosgrid.org:8089/all_service GET
    :return:
    '''
    service_all = Api.objects().all()
    return jsonify({'status': 10000, 'msg': '请求成功', 'data': service_all}),200, {'Content-Type': 'application/json;chaset=utf-8'}

@app.route('/call_service/<api_id>', methods=['GET'])
def url_construct(api_id):
    '''
    服务调用的接口，调用示例：http://service.cheosgrid.org:8089/call_service/1?__max_page=2&time=20181023&link_2.describe=描述
    :api  http://service.cheosgrid.org:8089/call_service/<api_id>
    :param api_id: int  是api的api_id信息
           超参数:__max_page  用以设置爬取的最大页数，该值为整数，且最小为1，设置为小于1的值将不起作用；设置为其他类型将返回错误信息
           返回属性中的参数：
               - *类型1：* 作为一级key值存在的属性，可直接将该key值作为一个请求参数
               - *类型2：* 作为多级下的key值存在的属性，将各级一次以“.”连接
           对应上述调用示例,请求参数有三个：，time，link_2.describe；对应的返回类型数据示例为:
                {
                  "time":"20181021",
                  "link_2":{
                        "describe":"描述",
                        "image":"http:XXX.png"
                   }
                }
    :return:
        {'status': 200, 'msg': '请求成功,共处理x页,其中第2,5页处理失败.' 或者 '请求成功,共处理x页.', 'data': results}
        {'status': 201, 'msg': '缺失api_crawl_rules_link文件或candidate项，无法处理网页', 'data': ""}
        {'status': 403, 'msg': '请求失败，服务器请求爬虫规则失败', 'data': ''}
        {'status': 410, 'msg': '爬虫失败，超时或请求错误', 'data': ''}
        {'status': 411, 'msg': '解析失败，网页信息错误', 'data': ''}
        {'status': 425, 'msg': '爬虫超时', 'data': ''}
        {'status': 426, 'msg': '缺少必须的参数: __parameters', 'data': ''}
    **ATTENTION - 注意**：
	    返回参数的key不能存在"."。 一方面是此处实现的要求，将"."作为级别的依据；另外一方面mongodb存储时要求key不能存在"."。
    '''

    request_parameters_ori = list(request.args.keys())

    request_parameters_ori_c = []
    #TODO remove ""'skeys
    for request_parameter_ori_ev in request_parameters_ori:
        if request.args.get(request_parameter_ori_ev) and request.args.get(request_parameter_ori_ev) != "":
            request_parameters_ori_c.append(request_parameter_ori_ev)

    request_parameters_ori = request_parameters_ori_c
    request_parameters_ori = [request_parameter.split('.') for request_parameter in request_parameters_ori]
    service = Api.objects(api_id=api_id).first()

    # TODO
    # judge the system parameters like frame and others.

    api_crawl_rules_link = service.api_crawl_rules_link
    form_rules_link = service.form_rules_link
    api_parameters = service.candidate[service.main_sec_id]
    api_url = service.api_url

    candidate_parameters = service.api_request_parameters_candidate # 可以使用的参数集合
    candidate_parameters = [candidate_parameter["query_name"] for candidate_parameter in candidate_parameters]
    candidate_parameters = [candidate_parameter.split(".") for candidate_parameter in candidate_parameters]

    candidate_required_parameters = [para["query_name"] for para in service.api_request_parameters_candidate if para["required"]]
    request_parameters_for_judge_required = list(request.args.keys())
    if not set(candidate_required_parameters).issubset(set(request_parameters_for_judge_required)):
        not_have_required = ",".join(list(set(candidate_required_parameters).difference(set(request_parameters_for_judge_required))))
        return jsonify({'status': 426, 'msg': '缺少必须的参数: '+not_have_required, 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

    # 可使用的请求参数集合  实际请求的请求参数集合
    request_parameters = [i for i in request_parameters_ori if i in candidate_parameters]
    ret_cha = [".".join(i) for i in request_parameters_ori if i not in candidate_parameters]


    api_parameters.sort(key=lambda k: k["id"])

    if api_crawl_rules_link and api_parameters:
        try:
            api_crawl_rules_two = requests.get(api_crawl_rules_link).json()
            api_crawl_rules = api_crawl_rules_two[service.main_sec_id]
        except:
            return jsonify({'status': 403, 'msg': '请求失败，服务器请求爬虫规则失败', 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

        try:
            crawl = Crawler(app.logger)

            ## level_0 parameters
            if ["__max_page"] in request_parameters:
                request_parameters.remove(["__max_page"])  #参数用完就删
                if int(request.args.get("__max_page")) >= crawl.max_page_set:
                    crawl.max_page_set = int(request.args.get("__max_page"))
                    crawl.max_page_set_flag = True

            ## level_1 parameters
            # 选出在request_parameters中属于level1的那些参数
            level_1_parameters = []
            for request_parameter in request_parameters:
                if service.api_request_parameters_candidate[candidate_parameters.index(request_parameter)]["level"] == 1:
                    level_1_parameters.append(request_parameter)
            request_parameters = [i for i in request_parameters if i not in level_1_parameters]
            level_1_parameters = [".".join(i) for i in level_1_parameters]

            crawl.input_key = []
            crawl.input_value = []
            for level_1_parameter in level_1_parameters:
                crawl.input_key.append(level_1_parameter)
                crawl.input_value.append(request.args.get(level_1_parameter))

            # crawl.genNewRecord()
            # Wait条件
            if len(api_crawl_rules) > 0:
                wait_rule = api_crawl_rules[0]
                wait_images = wait_rule["images"]
                wait_texts = wait_rule["texts"]
                wait_links = wait_rule["links"]
                if len(wait_texts)>0:
                    crawl.css_selc = wait_texts[0]["css_selector"]
                elif len(wait_images) >0:
                    crawl.css_selc = wait_images[0]["css_selector"]
                elif len(wait_links)>0:
                    crawl.css_selc = wait_links[0]["css_selector"]

                # 判断是否有iframe
                if crawl.css_selc:
                    if crawl.css_selc.find(">f>") >= 0:  # 对iframe中元素的特殊处理
                        crawl.iframe_addr = crawl.css_selc.split(">f>")[0]
                        crawl.css_selc = crawl.css_selc.split(">f>")[1]
                        crawl.iframe_ex = True


            if form_rules_link:
                crawl.form_list = requests.get(form_rules_link).json()

            time_out_judge = crawl.segment(api_url)

            if time_out_judge == "timeout":
                shutdown_crawl(crawl)
                return jsonify({'status': 425, 'msg': '爬虫超时', 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

        except Exception as e:
            shutdown_crawl(crawl)
            app.logger.error(repr(e))
            return jsonify({'status': 410, 'msg': '爬虫失败，超时或请求错误:'+str(e), 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}
        try:
            results = []
            message_error_return = []  # 将加载失败的页数记录在此，之后返回回去
            crawl.css_selc = None
            while crawl.judge_whether_final_page():
                cram_click_next_page, data_error = crawl.click_next_page()
                if cram_click_next_page:
                    page_pyquery = crawl.page  ## 页面page

                    for rule in api_crawl_rules:
                        images = rule["images"]
                        texts = rule["texts"]
                        links = rule["links"]

                        result = {"record_id": rule["record_id"]}
                        for image in images:
                            if crawl.iframe_ex and image["css_selector"].find('>f>')>=0:
                                image["css_selector"] = image["css_selector"].split(">f>")[1]
                            if not page_pyquery(image["css_selector"]) or len(page_pyquery(image["css_selector"])) == 0:
                                continue

                            if not crawl.css_selc:
                                crawl.css_selc = image["css_selector"]

                            res_value, parameter = image_filter(image, page_pyquery, api_parameters, api_url, crawl)
                            if parameter["select"] == 1:
                                result[parameter["name"]] = res_value

                        for text in texts:
                            if crawl.iframe_ex and text["css_selector"].find('>f>')>=0:
                                text["css_selector"] = text["css_selector"].split(">f>")[1]
                            if not page_pyquery(text["css_selector"]) or len(page_pyquery(text["css_selector"])) == 0:
                                continue
                            if not crawl.css_selc:
                                crawl.css_selc = text["css_selector"]
                            text_value, parameter = text_filter(text, page_pyquery, api_parameters)

                            if parameter["select"] == 1:
                                result[parameter["name"]] = text_value

                        for link in links:
                            if crawl.iframe_ex and link["css_selector"].find('>f>')>=0:
                                link["css_selector"] = link["css_selector"].split(">f>")[1]
                            if not page_pyquery(link["css_selector"]) or len(page_pyquery(link["css_selector"])) == 0:
                                continue
                            if not crawl.css_selc:
                                crawl.css_selc = link["css_selector"]
                            css_link_result = pq(page_pyquery(link["css_selector"])[0])
                            id = link["id"]
                            link_images = link["images"]
                            link_texts = link["texts"]

                            parameter = api_parameters[id]
                            result[parameter["name"]] = {}

                            for link_image in link_images:
                                if crawl.iframe_ex and link_image["css_selector"].find('>f>')>=0:
                                    link_image["css_selector"] = link_image["css_selector"].split(">f>")[1]
                                if not page_pyquery(link_image["css_selector"]) or len(page_pyquery(link_image["css_selector"])) == 0:
                                    continue
                                link_image_res_value, link_image_parameter = image_filter(link_image, page_pyquery, api_parameters, api_url,crawl)
                                if link_image_parameter["select"] == 1:
                                    result[parameter["name"]][link_image_parameter["name"]] = link_image_res_value
                            for link_text in link_texts:
                                if crawl.iframe_ex and link_text["css_selector"].find('>f>')>=0:
                                    link_text["css_selector"] = link_text["css_selector"].split(">f>")[1]
                                if not page_pyquery(link_text["css_selector"]) or len(page_pyquery(link_text["css_selector"])) == 0:
                                    continue
                                link_text_value, link_parameter = text_filter(link_text, page_pyquery, api_parameters)
                                if link_parameter["select"] == 1:
                                    result[parameter["name"]][link_parameter["name"]] = link_text_value
                            if parameter["select"] == 1:
                                if css_link_result.attr("href").startswith("http"):
                                    result[parameter["name"]]["href"] = css_link_result.attr('href')
                                else:
                                    result[parameter["name"]]["href"] = urljoin(api_url, "/" + css_link_result.attr('href'))

                        results.append(result)
                else:
                    if data_error:
                        message_error_return.append(data_error)
            try:  ## TODO track 1: dot cant be a key in mongodb,for example {"3.4":dsada}
                if not service.api_result_example:
                    numb = 3
                    if len(results) < 3:
                        numb = len(results)
                    result_example = results[:numb]
                    service.update(api_result_example = result_example)
            except:
                pass
            service.update(api_network = list(crawl.api_request.keys()))  ##getContentText的结果： 将可能有用的该网页的api network存入数据库的api_network字段

        except Exception as e:
            shutdown_crawl(crawl)
            app.logger.error(e)
            return jsonify({'status': 411, 'msg': '解析失败，网页信息错误'+str(e), 'data': ''}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

        new_result = []
        if len(results)>0:
            result_demo = results[0]

            parameters_unions, cha_set = select_result_parameter(request_parameters, result_demo)  # 请求参数和返回参数中求and的结果

            cha_set = cha_set + ret_cha
            for result in results:
                __Flag = True
                for parameters_union in parameters_unions:
                    _lik_val = "."
                    __request_value = request.args.get(_lik_val.join(parameters_union))

                    if not iterator_judge(parameters_union, result, __request_value) :
                        __Flag = False
                        break
                if __Flag:
                    new_result.append(result)

        current_page = crawl.current_page - 1

        shutdown_crawl(crawl)
        msg = ""
        if len(message_error_return) > 0:
            msg = "请求成功，共处理"+str(current_page)+"页，其中第" + ",".join(message_error_return) + "页处理失败."
        else:
            msg = "请求成功，共处理"+str(current_page)+"页."
        if len(cha_set) > 0:
            msg = msg + " 请求参数中 " + "，".join(cha_set) +" 未起作用，请核实【tip:请按照query_name查询】."
        return jsonify({'status': 200, 'msg': msg, 'data': new_result}), 200, {'Content-Type': 'application/json;chaset=utf-8'}
    else:
        return jsonify({'status': 201, 'msg': '缺失api_crawl_rules_link文件或candidate项，无法处理网页', 'data': ""}), 200, {'Content-Type': 'application/json;chaset=utf-8'}

@app.errorhandler(404)
def page_not_found(error):
    return "page not found", 404


def candidate_add_query_name(candidates):
    """
    为服务中的api请求信息增加query查询提示query_name
    :param candidates:
    :return:
    """
    for candidate in candidates:
        candidate.sort(key=lambda k: k["id"])
        for every_response_describe in candidate:
            if every_response_describe["parent_id"] == -1:
                every_response_describe["query_name"] = every_response_describe["name"]
            else:
                query_name = [every_response_describe["name"]]
                parent = every_response_describe
                while True:
                    parent = candidate[parent["parent_id"]]
                    query_name.insert(0, parent["name"])
                    if parent["parent_id"] == -1:
                        break

                query_name_str = ".".join(query_name)
                every_response_describe["query_name"] = query_name_str
    return candidates

def get_api_request_parameters_candidate_Level2(candidates, select):
    candidate = candidates[select]
    api_request_parameters_candidate_level2 = []
    for every_response_describe in candidate:
        if every_response_describe["type"] != "link" and every_response_describe["type"] != "img" and \
                every_response_describe["type"] != "background_img":
            every_parameter = {
                "type": "text",
                "query_name": every_response_describe["query_name"],
                "level": 2,
                "required": False,
                "example": every_response_describe["example"],
                "description": "[返回结果的筛选参数]: " + every_response_describe["description"]
            }
            api_request_parameters_candidate_level2.append(every_parameter)
    return api_request_parameters_candidate_level2