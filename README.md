## 域名WHOIS信息统计系统（Web）
该系统主要用来统计分析域名WHOIS信息，后台使用`Python`的`Tornado`框架，前台使用`Bootstrap/Ajax/JQuery/Highchars`等框架来搭建。
通过使用MVC框架，使程序能够更清晰明了.

前端使用以下内容
- dataTables
- font-awesome
- layers
- bootstrap
- highcharts
- highmaps

### 目录结构

```
├── README.md
├── __init__.py 初始化
├── application.py Application类
├── models 其中存放各种模型(数据),对应MVC的M(model)
├── templates 其中存放web页面的模板,与static结合,完成页面的显示,对应MVC的V(view)
├── handlers 其中存放跟踪模型(数据),对应MVC的C(control)
├── models 其中存放各种模型(数据),对应MVC的M(model)
├── settings 配置文件
├── server.py 用来启动web服务器
├── db_info.md 数据库相关介绍
├── static 存放静态文件
│   ├── css  存放CSS文件
│   ├── images  存放图片
│   └── js  存放js脚本
└── urls.py 控制访问，路由
```

### 改进的方向

```
1. 异步执行
2. Ajax技术
3. 缓存技术
4. 程序健壮性
5. 结构较为混乱
```
