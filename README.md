# 域名WHOIS信息统计分析系统（Web）

## 简介

该系统主要用来统计分析域名WHOIS信息，后台使用`Python`的`Tornado`框架，前台使用`Bootstrap/Ajax/JQuery/Highchars`等框架来搭建。
通过使用MVC框架，使程序能够更清晰明了,同时方便编写代码.

前端使用以下内容
- dataTables
- font-awesome
- layers
- bootstrap
- highcharts
- highmaps

## 项目目录结构

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
├── database 数据库介绍以及后台数据库更新程序
├── static 存放静态文件
│   ├── css  存放CSS文件
│   ├── img  存放图片
│   └── js  存放js脚本
└── urls.py 控制访问，路由
```

## 负责人

1. 项目负责人：程亚楠
2. 其他组员： 郑乐斌
