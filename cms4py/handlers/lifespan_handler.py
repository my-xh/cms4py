# -*- coding: utf-8 -*-

"""
@File    : lifespan_handler.py
@Time    : 2021/10/5 23:07
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 生命周期管理
"""

from cms4py.utils.log import Cms4pyLog


async def handle_lifespan(scope, receive, send):
    while True:
        message = await receive()
        if message['type'] == 'lifespan.startup':
            # 进行初始化操作
            await send({'type': 'lifespan.startup.complete'})
            Cms4pyLog.get_instance().info('Server started')
        elif message['type'] == 'lifespan.shutdown':
            # 进行收尾工作
            await send({'type': 'lifespan.shutdown.complete'})
            Cms4pyLog.get_instance().info('Server stopped')
            break
