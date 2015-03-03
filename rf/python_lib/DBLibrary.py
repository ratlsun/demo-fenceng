# -*- coding: UTF-8 -*-
"""
Created on 2014年10月13日


"""
from hale.demo import StaticMethodClass


class DBLibrary(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1'

    def get_result_from_db(self, maxsize, sql, *args):
        """访问数据库
        """
        return StaticMethodClass.getRows(int(maxsize), sql, args)
