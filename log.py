# coding:utf-8

__author__ = 'huangxiaonan'


class Log(object):
    def __init__(self, con_log_out=True, file_log=False, log_memory_msg=False, **kwargs):
        """
        :keyword:[con_log_out]:控制台日志打印，默认开启,[con_log_out=False]关闭
        :keyword:[logFm]: 外层日志输出格式参数self.logFm: [时间,日志名，日志级别，日志信息,进程ID]
        :keyword:[funcLogFarm]: 内层日志输出格式参数self.funcLogFarm: [日志格式<funcLog>[函数名称，函数参数，函数位置]
        :keyword:[conLevel]: 控制台日志输出级别参数con_level_dict
        :keyword:[logName]: 控制台日志名称默认'log'
        ----------------------------------------------------------------------------------------------------------------
        :keyword:[file_log]:日志文件记录默认关闭,file_log=True开启
        :keyword:[filePath]:日志文件记录路径[默认路径./log.log,日志保存文件默认关闭]
        :keyword:[fileFm]:日志文件记录格式
        :keyword:[fileLevel]:日志文件记录级别[默认级别DEBUG]
        ----------------------------------------------------------------------------------------------------------------
        :keyword:[logMemoryMsg]:缓存日志记录默认关闭,logMemoryMsg=True开启
        :var:logGetMsg():获取内存日志
        ----------------------------------------------------------------------------------------------------------------
        :parameter:<self.funcLogFarm>修改涉及函数操作:
            def funclogfm(self, func, *args, **kwargs):
                if self.funcLogFm == None:
                    self.funcLogFm = self.funcLog % (
                        func.__name__, args, kwargs, func.__code__.co_firstlineno, func.__code__.co_filename)
                return self.funcLogFm
        ----------------------------------------------------------------------------------------------------------------
        """
        from functools import wraps
        import logging
        import sys
        import inspect
        from logging.handlers import MemoryHandler
        if con_log_out:
            if 'logFm' in kwargs.keys():
                self.logFm = kwargs['logFm']
            else:
                self.logFm = '%(asctime)s - %(name)s - %(levelname)s - %(message)s - PID:[%(process)d];'
            if 'funcLogFarm' in kwargs.keys():
                self.funcLogFarm = kwargs['funcLog']
            else:
                self.funcLogFarm = 'line: %s - funcName: <%s> - parm:[ %s, %s ] - path: %s'
            if 'conLevel' in kwargs.keys():
                con_level_dict = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'ERROR': logging.ERROR}
                logging.basicConfig(level=con_level_dict[kwargs['conLevel']], format=self.logFm)
            else:
                logging.basicConfig(level=logging.DEBUG, format=self.logFm)
            if 'logName' in kwargs.keys():
                self.logger = logging.getLogger(kwargs['logName'])
            else:
                self.logger = logging.getLogger('log')
        if file_log:
            if 'filePath' in kwargs.keys():
                self.handler = logging.FileHandler(kwargs['filePath'])
            else:
                self.handler = logging.FileHandler("log.log")
            if 'fileFm' in kwargs.keys():
                formatter = logging.Formatter(kwargs['fileFm'])
            else:
                formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
            if 'fileLevel' in kwargs.keys():
                con_level_dict = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'ERROR': logging.ERROR}
                logging.basicConfig(level=con_level_dict[kwargs['conLevel']], format=self.logFm)
            else:
                logging.basicConfig(level=logging.DEBUG, format=self.logFm)
            self.handler.setFormatter(formatter)
            self.logger.addHandler(self.handler)
        if log_memory_msg:
            self.logMemoryMsg = MemoryHandler(1, flushLevel=logging.DEBUG)
            self.logMemoryMsg.setLevel(logging.DEBUG)
            self.logMemoryMsg.setFormatter(self.logFm)
            self.logger.addHandler(self.logMemoryMsg)
        self.logFarMet = 'line: %s - funcName:<%s> - parm:[ %s ] - path: %s'
        self.wraps = wraps
        self.funcLogFm = None

        self.sys = sys
        self.inspect = inspect

    def doc(self):
        print(self.__init__.__doc__)

    def func_log_fm(self, func, *args, **kwargs):
        line_numb = func.__code__.co_firstlineno
        who = func.__name__
        path = func.__code__.co_filename
        self.funcLogFm = self.funcLogFarm % (line_numb, who, args, kwargs, path)
        return self.funcLogFm

    def __debug(self, func):
        """日志装饰器"""

        @self.wraps(func)
        def tmp(*args, **kwargs):
            self.logger.debug(self.func_log_fm(func, args, kwargs))
            try:
                return func(*args, **kwargs)
            except ZeroDivisionError:
                err = "There was an exception in  "
                err += 'funcName<%s> - error: %s' % (func.__name__, ZeroDivisionError)
                self.logger.exception(err)

        return tmp

    def __info(self, func):
        """日志装饰器"""

        @self.wraps(func)
        def tmp(*args, **kwargs):
            self.logger.info(self.func_log_fm(func, args, kwargs))
            try:
                return func(*args, **kwargs)
            except ZeroDivisionError:
                err = "There was an exception in  "
                err += 'funcName<%s> - error: %s' % (func.__name__, ZeroDivisionError)
                self.logger.exception(err)

        return tmp

    def __warning(self, func):
        """日志装饰器"""

        @self.wraps(func)
        def tmp(*args, **kwargs):
            self.logger.warning(self.func_log_fm(func, args, kwargs))
            try:
                return func(*args, **kwargs)
            except ZeroDivisionError:
                err = "There was an exception in  "
                err += 'funcName<%s> - error: %s' % (func.__name__, ZeroDivisionError)
                self.logger.exception(err)

        return tmp

    def debug(self, message):
        """返回程序中的当前行号:inspect.currentframe().f_back.f_lineno"""
        line_numb = self.inspect.currentframe().f_back.f_lineno
        who = self.inspect.getframeinfo(self.inspect.currentframe().f_back)
        msg = self.logFarMet % (line_numb, who[2], message, who[0])
        return self.logger.debug(msg)

    def info(self, message):
        """返回程序中的当前行号:inspect.currentframe().f_back.f_lineno"""
        line_numb = self.inspect.currentframe().f_back.f_lineno
        who = self.inspect.getframeinfo(self.inspect.currentframe().f_back)
        msg = self.logFarMet % (line_numb, who[2], message, who[0])
        import io
        log_capture_string = io.StringIO()
        log_contents = log_capture_string.getvalue()
        print(log_contents.lower())
        log_capture_string.close()
        return self.logger.info(msg)

    def warning(self, message):
        """返回程序中的当前行号:inspect.currentframe().f_back.f_lineno"""
        lineno = self.inspect.currentframe().f_back.f_lineno
        who = self.inspect.getframeinfo(self.inspect.currentframe().f_back)
        msg = self.logFarMet % (lineno, who[2], message, who[0])
        return self.logger.warning(msg)

    def error(self, message):
        """返回程序中的当前行号:inspect.currentframe().f_back.f_lineno"""
        linen_umb = self.inspect.currentframe().f_back.f_lineno
        who = self.inspect.getframeinfo(self.inspect.currentframe().f_back)
        msg = self.logFarMet % (linen_umb, who[2], message, who[0])
        return self.logger.error(msg)

    def exception(self, message=None):
        """返回程序中的当前行号:inspect.currentframe().f_back.f_lineno"""
        who = self.inspect.getframeinfo(self.inspect.currentframe().f_back)
        err = "There was an exception in  "
        err = err + 'funcName: <%s> - path: %s - error: %s' % (who[2], who[0], message)
        return self.logger.exception(err)

    def log_get_msg(self):
        return self.logMemoryMsg.buffer[-1].getMessage()

    DEBUG = __debug
    INFO = __info
    WARNING = __warning
