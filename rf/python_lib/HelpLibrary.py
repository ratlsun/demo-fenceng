# -*- coding: UTF-8 -*-
"""
Created on 2014年10月13日


"""
from hale.demo import DynamicPropertiesClass


class HelpLibrary(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1'

    def setting_and_run(self, **args):
        """访问实例对象，动态设置属性
        """
        o = DynamicPropertiesClass()
        for (name, value) in  args.items(): 
        	f = o.getClass().getDeclaredField(name)
        	f.setAccessible(True);
        	f.set(o, value)
        o.run()


