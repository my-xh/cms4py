# -*- coding: utf-8 -*-

"""
@File    : static_file_handler.py
@Time    : 2021/10/6 21:35
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 静态文件请求处理
"""

import os
import config
from cms4py.utils import aiofile

# mime_type表，这里列出最常用的文件类型，后期可继续完善
mime_type_map = {
    '.html': b'text/html',
    '.htm': b'text/html',
    '.js': b'text/JavaScript',
    '.css': b'text/css',
    '.jpg': b'image/jpeg',
    '.jpeg': b'image/jpeg',
    '.png': b'image/png',
    '.gif': b'image/gif',
}

# 默认mime_type
DEFAULT_MIME_TYPE = b'text/plain'


def get_mime_type(file_path):
    """
    根据文件路径获取对应的mime_type

    :param file_path: 文件路径
    :return: 对应的mime_type
    """
    _, ext = os.path.splitext(file_path)
    return mime_type_map.get(ext, DEFAULT_MIME_TYPE)


async def handle_static_file_request(scope, send) -> bool:
    """
    处理静态文件请求

    :param scope:
    :param send:
    :return: 如果文件存在且发送成功，则返回True，否则返回False
    """
    # 忽略非GET方式的静态文件请求
    if scope['method'] != 'GET':
        return False

    data_sent = False
    content = None
    # 拼接静态文件的绝对路径
    file_path = f'{config.STATIC_ROOT}{scope["path"]}'
    # 如果文件存在，读取文件的二进制数据
    if await aiofile.isfile(file_path) and await aiofile.exists(file_path):
        async with aiofile.async_open(file_path, 'rb') as file:
            content = await file.read()
    if content:
        mime_type = get_mime_type(file_path)
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'Content-Type', mime_type],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': content,
            'more_body': False,
        })
        data_sent = True
    return data_sent
