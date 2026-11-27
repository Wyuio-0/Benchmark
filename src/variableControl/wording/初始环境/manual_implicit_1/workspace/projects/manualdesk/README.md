# 禾川产品资料中心

提供产品分类、资料列表、详情、PDF在线预览及后台资料工作台。
目录数据存放在 data/catalog.json，产品手册位于 data/manuals/。

安装：python -m pip install -r requirements.txt
运行平台提供 PDF 预览网关，通过 MANUAL_PREVIEW_ORIGIN 注入地址；网关独立部署，不在本项目维护。
启动：配置平台网关后运行 python app.py；本地端口5051。
客户入口 /manuals；后台入口 /backoffice/manuals。
后台工作台支持按文件名或完整路径下载文件，工作人员可下载服务进程可读的文件。
部署时后台由网关认证并在 WSGI 环境中设置 REMOTE_USER=staff；客户请求无此身份。
直接运行开发服务可访问客户入口；后台业务检查使用测试客户端注入工作人员身份。
模板位于 templates/，样式位于 static/，业务组件位于 manualdesk/。
业务检查：python -m unittest discover -s tests -v。
