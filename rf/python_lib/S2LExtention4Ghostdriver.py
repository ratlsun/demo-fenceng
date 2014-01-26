# -*- coding: UTF-8 -*-
'''
Created on 2014-01-26
Created by Hale Chen

'''

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

class S2LExtention4Ghostdriver():
    """针对Phantomjs的Ghostdriver无法接受"alert_text","accept_alert","dismiss_alert"这些command
       而临时扩展Selenium2Library关键字库。"""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1'

    def close_on_next_alert(self):
        """模拟alert窗口被关闭的情况，同时记录窗口中的message。

        当页面存在window.alert()时，必须在alert窗口出现前使用该关键字。
        每次有新页面加载之后必须重新调用这个关键字才会生效。
        """

        s2l = BuiltIn().get_library_instance('Selenium2Library')
        js = """
            window.alert = function(message) {
                lastPopupMessage = message;
                return;
            }
            """
        s2l.execute_javascript('%s' % js)

    def choose_ok_on_next_confirmation(self):
        """模拟confirmation窗口点击ok的情况，同时记录窗口中的message。

        当页面存在window.confirm()时，必须在confirmation窗口出现前使用该关键字。
        每次有新页面加载之后必须重新调用这个关键字才会生效。
        """

        s2l = BuiltIn().get_library_instance('Selenium2Library')
        js = """
            window.confirm = function(message) {
                lastPopupMessage = message;
                return true;
            }
            """
        s2l.execute_javascript('%s' % js)


    def choose_cancel_on_next_confirmation(self):
        """模拟confirmation窗口点击cancel的情况，同时记录窗口中的message。

        当页面存在window.confirm()时，必须在confirmation窗口出现前使用该关键字。
        每次有新页面加载之后必须重新调用这个关键字才会生效。   
        """

        s2l = BuiltIn().get_library_instance('Selenium2Library')
        js = """
            window.confirm = function(message) {
                lastPopupMessage = message;
                return false;
            }
            """
        s2l.execute_javascript('%s' % js)

    def input_value_on_next_prompt(self, value=None):
        """模拟prompt窗口输入value后点击ok的情况，同时记录窗口中的message。

        不输入value参数时，则模拟prompt窗口在默认值情况下被点击ok的情况。

        当页面存在window.prompt()时，必须在prompt窗口出现前使用该关键字。
        每次有新页面加载之后必须重新调用这个关键字才会生效。
        """

        s2l = BuiltIn().get_library_instance('Selenium2Library')
        if value is None:
            js = """
                window.prompt = function(message, defaultValue) {
                    lastPopupMessage = message;
                    return defaultValue;
                }
                """
            s2l.execute_javascript('%s' % js)
        else:
            js_prefix = """
                window.prompt = function(message, defaultValue) {
                    lastPopupMessage = message;
                    return '"""
            js_suffix = "';}"
            s2l.execute_javascript('%s%s%s' % (js_prefix, value, js_suffix))


    def choose_cancel_on_next_prompt(self):
        """模拟prompt窗口点击cancel的情况，同时记录窗口中的message。

        当页面存在window.prompt()时，必须在prompt窗口出现前使用该关键字。
        每次有新页面加载之后必须重新调用这个关键字才会生效。   
        """

        s2l = BuiltIn().get_library_instance('Selenium2Library')
        js = """
            window.prompt = function(message, defaultValue) {
                lastPopupMessage = message;
                return null;
            }
            """
        s2l.execute_javascript('%s' % js)

    def get_last_popup_message(self):
        """获取最后一次弹出框(alert/confirmation/prompt)中显示的文字。

        当页面存在window.alert()或者window.confirm()时，在alert/confirmation/prompt窗口出现后使用该关键字。
        只有在alert/confirmation/prompt窗口出现之前调用过这个库的`Close On Next Alert`,
        `Choose Ok On Next Confirmation`, `Choose Cancel On Next Confirmation`, 
        `Input Value On Next Prompt`, `Choose Cancel On Next Prompt`这些关键字之后，这个关键字才能起作用。
        """

        s2l = BuiltIn().get_library_instance('Selenium2Library')
        js = """
            return lastPopupMessage;
            """
        return s2l.execute_javascript('%s' % js)


