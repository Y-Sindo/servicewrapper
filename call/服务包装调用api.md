#### 1. 服务api相关操作：增删改查-分别对应POST、DELETE、PUT、GET
#### 	url: http://service.cheosgrid.org:8089/service

```json

参数及示例如下：

POST: JSON 增
    :parameter  api_name : string
                api_url : string
                api_description : string
                api_crawl_rules_link : string
                api_parameters : list
                img_link : string
                json_link : string
                main_sec_id: int
    :example
                {
                    "api_name":"weather_4",
                    "api_description":"api",
                    main_sec_id: 0
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
                    "api_url":"http://test.cn",      ## url and link 一定要是http://   或者 https://
                }

GET: 查
    :parameter api_name : string 或者api_id : int 
    :exapmle
        http://service.cheosgrid.org:8089/service?api_name=weather
        http://service.cheosgrid.org:8089/service?api_id=1

PUT:JSON 改
    :parameter
                api_id: 2     ## 一定要有api_id
                api_name : string
                api_url : string
                api_description : string
                api_crawl_rules_link : string
                api_parameters : list
                img_link : string
                json_link : string
                main_sec_id: int
    :example
                {
                    "api_name":"weather_4",
                    "api_description":"api",
                    main_sec_id: 1
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

DELETE: 删
    :parameter api_id : int
    :example
        http://service.cheosgrid.org:8089/service?api_id=1
:return:
  GET PUT POST:	{'status':10000, 'msg':'请求成功', 'data':service},200  
  DELETE:       {'status':10000, 'msg':'请求成功', 'data':''}, 200  
                {'status': 400, 'msg': '参数错误', 'data':''}, 200
                {'status': 401, 'msg': '服务不存在', 'data': ''}, 200
                {'status': 402, 'msg': '已有该服务', 'data': ''}, 200
```

#### 2. 服务调用api

```json
'''
服务调用的接口，调用示例：http://service.cheosgrid.org:8089/call_service/1?__max_page=2&time=20181023&link_2.describe=描述
:api  http://service.cheosgrid.org:8089/call_service/<api_id>
:param api_id: int  是api的api_id信息
	   超参数:__max_page  用以设置爬取的最大页数，该值为整数，且最小为1，设置为小于1的值将不起作用；设置为其他类型将返回错误信息
	         如果__max_page >= 1, 爬取页数为__max_page页；否则最多爬取5页；注意：如果__max_page过大，可能出现错误；
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
    {'status': 403, 'msg': '请求失败，服务器请求爬虫规则失败', 'data': ''}
    {'status': 410, 'msg': '爬虫失败，超时或请求错误', 'data': ''}
    {'status': 411, 'msg': '解析失败，网页信息错误', 'data': ''}
    {'status': 425, 'msg': '爬虫超时', 'data': ''}
    {'status': 200, 'msg': '请求成功,共处理x页,其中第2,5页处理失败.' 或者 '请求成功,共处理x页.', 'data': results}
     {'status': 426, 'msg': '缺少必须的参数: __parameters', 'data': ''}
'''

**ATTENTION - 注意**：
	返回参数的key不能存在"."。
	一方面是此处实现的要求，将"."作为级别的依据；另外一方面mongodb存储时要求key不能存在"."。
```

#### 3. 获得所有服务api

```json
'''
获得所有api
http://service.cheosgrid.org:8089/all_service GET
:return:
'''
```

