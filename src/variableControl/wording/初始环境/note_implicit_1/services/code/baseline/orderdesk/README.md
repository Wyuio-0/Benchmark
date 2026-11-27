# OrderDesk 订单中心

本地门店订单协同项目，包含客户订单列表、详情与留言，以及后台订单工作单和交接备注。

启动：`python -m pip install -r requirements.txt`，然后 `python app.py`，访问本机5050端口。

主要入口：客户订单 `/orders`，后台工作台 `/backoffice/orders`。
业务数据在 `data/orders.json`，保存留言后重新读取详情即可查看更新。
应用入口为 `app.py`，页面在 `templates/`，公共样式在 `static/site.css`，显示组件在 `orderdesk/`。

业务检查：`python -m unittest discover -s tests -v`。
