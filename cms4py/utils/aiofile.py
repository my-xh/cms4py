# -*- coding: utf-8 -*-

"""
@File    : aiofile.py
@Time    : 2021/10/6 18:51
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 异步文件处理
"""

import asyncio
import os


class AsyncFunWrapper:

    def __init__(self, blocked_func):
        # 封装阻塞型IO函数
        self._blocked_func = blocked_func

    def __call__(self, *args):
        return asyncio.get_running_loop().run_in_executor(
            None,
            self._blocked_func,
            *args,
        )


class AIOWrapper:

    def __init__(self, coroutine):
        # 封装协程
        self._coroutine = coroutine
        # 封装阻塞型IO对象
        self._blocked_file_io = None

    async def __aenter__(self):
        self._blocked_file_io = await self._coroutine
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        self._blocked_file_io = None

    def __getattr__(self, name) -> AsyncFunWrapper:
        return AsyncFunWrapper(
            getattr(
                self._blocked_file_io,
                name,
            )
        )

    def __await__(self):
        self._blocked_file_io = yield from self._coroutine
        return self


# 异步方式打开文件
def async_open(*args) -> AIOWrapper:
    return AIOWrapper(
        asyncio.get_running_loop().run_in_executor(
            None,
            open,
            *args,
        )
    )


# 判断指定的文件是否存在
async def exists(file_path):
    return await asyncio.get_running_loop().run_in_executor(
        None,
        os.path.exists,
        file_path,
    )


# 判断指定的路径是否是文件
async def isfile(file_path):
    return await asyncio.get_running_loop().run_in_executor(
        None,
        os.path.isfile,
        file_path,
    )


# 获取指定路径文件的修改时间
async def getmtime(file_path):
    return await asyncio.get_running_loop().run_in_executor(
        None,
        os.path.getmtime,
        file_path,
    )
