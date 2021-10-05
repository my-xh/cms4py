# -*- coding: utf-8 -*-

"""
@File    : log.py
@Time    : 2021/10/5 22:46
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 日志系统
"""

import logging
import config


class Cms4pyLog:
    __instance = None

    @staticmethod
    def get_instance():
        if Cms4pyLog.__instance is None:
            Cms4pyLog.__instance = Cms4pyLog()
        return Cms4pyLog.__instance

    def __init__(self):
        super().__init__()
        self._log = logging.getLogger(config.APP_NAME)

        log_handler = logging.StreamHandler()
        log_handler.setFormatter(
            logging.Formatter(
                '[%(levelname)s %(name)s %(asctime)s %(pathname)s(%(lineno)s)] %(message)s'
            )
        )
        if self._log.parent:
            self._log.parent.handlers = []
            # 设置自定义的日志处理工具
            self._log.parent.addHandler(log_handler)

        # 设置日志的级别，用于过滤不希望出现的日志
        self._log.setLevel(config.LOG_LEVEL)
        self.info = self._log.info
        self.debug = self._log.debug
        self.warning = self._log.warning
        self.error = self._log.error
