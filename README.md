服务包装模块文件说明
======
- /
  - segment.py 分割页面，生成规则文件
  - demo.py  负责调用segment.py
  - form.py 检测表单，生成表单规则文件
  - form_demo.py 负责调用form.py
  - setting.py 一些常量定义
- nlp_invoke/ （django后台文件)
  - nlp_invoke/（django后台文件)
    - view.py 核心后台文件，负责调用不同的函数，渲染不同的页面
      - formdetector 负责接收url 调用form_demo.py
      - servicewrapper_update 负责接收json，调用demo.py
    -  urls.py 绑定url路径
    - settings.py 配置跨域访问等配置
- static/ 用来存放生成的所有规则文件
- lcypytools/ 原始工具包，里面有类似存储json等函数
- driver/ 存放浏览器驱动文件
