# -*- coding: utf-8 -*-

"""
@File    : __init__.py
@Time    : 2021/10/5 22:24
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : ASGI应用
"""

import uvicorn

from cms4py.handlers import error_pages, lifespan_handler, static_file_handler
from cms4py.utils.log import Cms4pyLog


async def application(scope, receive, send):
    # 获取请求类型
    request_type = scope['type']
    if request_type == 'http':
        data_sent = await static_file_handler.handle_static_file_request(scope, send)
        if not data_sent:
            # 对于未被处理的http请求，均向浏览器发送404错误
            await error_pages.send_404_error(scope, receive, send)
    elif request_type == 'lifespan':
        # 处理生命周期类型的请求
        await lifespan_handler.handle_lifespan(scope, receive, send)
    else:
        # 未知类型的请求
        Cms4pyLog.get_instance().warning('Unsupported ASGI type')


if __name__ == '__main__':
    uvicorn.run(application)
