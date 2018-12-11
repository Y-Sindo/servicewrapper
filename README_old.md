服务包装模块调用指南
======
首先，访问下面的网址，给url参数传入值，GET方法即可。如：
```html
http://183.129.170.180:18088/servicepackage/?url=http://192.168.9.51/APIMarket.html?id=1
```
注意，传入的url前面必须要加入http://或者https:// !!!

已在下面三个页面测试成功,可以继续测试其他页面：
```
http://192.168.9.51/APIMarket.html?id=1 
http://www.nmdis.org.cn/gongbao/
http://www.gov.cn/premier/lkq_wz.htm
```

访问后，页面会立即返回一个日志地址，如：
```html
http://183.129.170.180:18088/statics/15392704808923/process.log
```
设置定时器不断访问此文件即可得到现在服务包装的进展。

一般情况下，爬页面时间在60s左右，分析时间在60s左右

爬取成功后，会显示最后一行:200+空格+api_info.json文件地址，如：
```html
200 http://183.129.170.180:18088/statics/15392704808923/api_info.json
```
日志报错（如超过120s则会返回503,504错误）或者log文件长时间无变化时，即视为失败，因此前端模块建议设置120s等待时间。

访问上面的链接，得到api_info.json文件，格式如下：
```json
{
	"api_name":"",
	"api_description":"",
	"api_url":"",	
	"img_link":"",//前端显示全部内容
	"json_link":"",
	"api_crawl_rules_link":"",//link address
	"api_parameters":[
		{
			"id": 0,
			"name":"text_1/link_1/img_1",//参数名
			"description": "default",  //参数解释
			"type": "text/link/img",
			"example": "",   //示例值
			"select": "1/0"  //是否选择此值
		}
	]
}
```
其中，img_link字段即截取的主要部分的图片链接地址

json_link字段为截取的部分的文字，只有一个content字段，这两部分均可以显示在前端上

api_crawl_rules_link字段为爬虫规则的json文件，不要动，传给api管理后台

然后，根据此字段默认值，修改api的相关信息后，将上面的信息传给api添加后台，注意，api_parameters中的id值不要动，type不要动，select可让用户选择是否选择此字段，其他字段用户可以自由修改。

示例api_info_json内容:
```json
{
	"img_link": "http://183.129.170.180:18088/static/15392008367234/sec_shot.png",
	"json_link": "http://183.129.170.180:18088/static/15392008367234/example.json",
	"api_url": "http://service.cheosgrid.org:8076/APIMarket.html?id=1",
	"api_parameters": [{
		"description": "text_description",
		"select": 1,
		"name": "text_0",
		"id": 0,
		"type": "text",
		"example": "14"
	},
	{
		"description": "text_description",
		"select": 1,
		"name": "text_1",
		"id": 1,
		"type": "text",
		"example": "2"
	},
	{
		"description": "image_description",
		"select": 1,
		"name": "image_2",
		"id": 2,
		"type": "img",
		"example": "{src:'',alt:'',title:''}"
	},
	{
		"description": "image_description",
		"select": 1,
		"name": "image_3",
		"id": 3,
		"type": "img",
		"example": "{src:'',alt:'',title:''}"
	},
	{
		"description": "link_description",
		"select": 1,
		"name": "link_4",
		"id": 4,
		"type": "link",
		"example": "{href:''}"
	},
	{
		"description": "link_text_description_related_to_link_4",
		"select": 1,
		"name": "link_text_5",
		"id": 5,
		"type": "text",
		"example": "PM2.5监测"
	},
	{
		"description": "link_text_description_related_to_link_4",
		"select": 1,
		"name": "link_text_6",
		"id": 6,
		"type": "text",
		"example": "2018-04-15 02:54:26"
	},
	{
		"description": "link_image_description_related_to_link_4",
		"select": 1,
		"name": "link_image_7",
		"id": 7,
		"type": "img",
		"example": "{src:'',alt:'',title:''}"
	},
	{
		"description": "link_image_description_related_to_link_4",
		"select": 1,
		"name": "link_image_8",
		"id": 8,
		"type": "img",
		"example": "{src:'',alt:'',title:''}"
	},
	{
		"description": "link_image_description_related_to_link_4",
		"select": 1,
		"name": "link_image_9",
		"id": 9,
		"type": "img",
		"example": "{src:'',alt:'',title:''}"
	},
	{
		"description": "link_image_description_related_to_link_4",
		"select": 1,
		"name": "link_image_10",
		"id": 10,
		"type": "img",
		"example": "{src:'',alt:'',title:''}"
	},
	{
		"description": "link_image_description_related_to_link_4",
		"select": 1,
		"name": "link_image_11",
		"id": 11,
		"type": "img",
		"example": "{src:'',alt:'',title:''}"
	},
	{
		"description": "link_image_description_related_to_link_4",
		"select": 1,
		"name": "link_image_12",
		"id": 12,
		"type": "img",
		"example": "{src:'',alt:'',title:''}"
	}],
	"api_crawl_rules_link": "http://183.129.170.180:18088/static/15392008367234/rules_list.json",
	"api_description": "高分中心数据集市",
	"api_name": "高分中心数据集市"
}
```
示例json_link内容：
```json
{
	"content": "PM2.5监测\n    2018-04-15 02:54:26\n142\n全国天气预报\n    2018-04-15 01:54:26\n61\n历史天气\n    2018-04-15 01:54:26\n30\nPM2.5空气质量指数\n    2018-04-11 01:09:05\n00\n全国雷暴\n    2018-03-29 02:24:14\n10\n全国风速情况\n    2018-03-29 02:23:41\n00\n国内云量概况\n    2018-03-29 02:23:05\n00\n国内积雪层概况\n    2018-03-29 02:22:23\n00\n全国降水情况\n    2018-03-29 02:00:13\n00\n全国天气气温\n    2018-03-29 01:59:28\n10"
}
```
示例api_crawl_rules_link内容（部分）：
```json
[
{
	"images": [{
		"type": "img",
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > div:nth-child(2) > span > img",
		"id": 2
	},
	{
		"type": "img",
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > div:nth-child(2) > span:nth-child(2) > img",
		"id": 3
	}],
	"texts": [{
		"rank": 2,
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li",
		"id": 0
	},
	{
		"rank": 3,
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li",
		"id": 1
	}],
	"record_id": 0,
	"links": [{
		"images": [{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a > img",
			"id": 7
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a > p:nth-child(3) > img",
			"id": 8
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a > p:nth-child(3) > img:nth-child(2)",
			"id": 9
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a > p:nth-child(3) > img:nth-child(3)",
			"id": 10
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a > p:nth-child(3) > img:nth-child(4)",
			"id": 11
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a > p:nth-child(3) > img:nth-child(5)",
			"id": 12
		}],
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a",
		"texts": [{
			"rank": 0,
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a",
			"id": 5
		},
		{
			"rank": 1,
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li > a",
			"id": 6
		}],
		"id": 4
	}]
},
{
	"images": [{
		"type": "img",
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > div:nth-child(2) > span > img",
		"id": 2
	},
	{
		"type": "img",
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > div:nth-child(2) > span:nth-child(2) > img",
		"id": 3
	}],
	"texts": [{
		"rank": 2,
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2)",
		"id": 0
	},
	{
		"rank": 3,
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2)",
		"id": 1
	}],
	"record_id": 1,
	"links": [{
		"images": [{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a > img",
			"id": 7
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a > p:nth-child(3) > img",
			"id": 8
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a > p:nth-child(3) > img:nth-child(2)",
			"id": 9
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a > p:nth-child(3) > img:nth-child(3)",
			"id": 10
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a > p:nth-child(3) > img:nth-child(4)",
			"id": 11
		},
		{
			"type": "img",
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a > p:nth-child(3) > img:nth-child(5)",
			"id": 12
		}],
		"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a",
		"texts": [{
			"rank": 0,
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a",
			"id": 5
		},
		{
			"rank": 1,
			"css_selector": "html > body:nth-child(2) > section:nth-child(2) > div:nth-child(4) > ul:nth-child(2) > li:nth-child(2) > a",
			"id": 6
		}],
		"id": 4
	}]
}
]
```
