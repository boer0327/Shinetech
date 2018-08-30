#coding=utf-8

import mechanize
import time
import urllib
import os
from StringIO import StringIO
import sys
import copy
import re
import datetime
import json

class Shinetech(object):
    def __init__(self, username, password, cookie_file, debug=False, 
            user_agent= ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_5) '
            'AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.218 Safari/535.1')):
        self.username = username
        self.password = password
        self.cookie_file = cookie_file
        self.debug = debug
        self.user_agent = user_agent
        self.browser = None

    def get_browser(self):
        if self.browser:
            return self.browser
        else:
            browser = mechanize.Browser()
            browser.set_handle_equiv(False)
            browser.set_handle_gzip(True)
            browser.set_handle_redirect(True)
            browser.set_handle_robots(False)
            browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
            # browser.set_seekable_responses(False)
            if self.debug:
                browser.set_debug_http(True)
                browser.set_debug_redirects(True)
                browser.set_debug_responses(True)
            cj = mechanize.LWPCookieJar()
            try:
                cj.load(self.cookie_file, ignore_discard=True, ignore_expires=True)
            except IOError:
                pass
            browser.set_cookiejar(cj)
            browser.addheaders = [
                ('User-agent', self.user_agent),
            ]
            self.browser = browser
            return self.browser

    def get_cookie_string(self, url):
        br = self.get_browser()
        r = mechanize.Request(url)
        cookies = br._ua_handlers['_cookies'].cookiejar.cookies_for_request(r)
        attrs = br._ua_handlers['_cookies'].cookiejar._cookie_attrs(cookies)
        return "; ".join(attrs)

    def request(self, url, data=None):
        br = self.get_browser()

        if data:
            data = urllib.urlencode(data)

        response = br.open(url, data)
        br._ua_handlers['_cookies'].cookiejar.save(self.cookie_file, ignore_discard=True, ignore_expires=True)
        return response

    def submitWork(self, title=None, description=None, hours='8'):
        br = self.get_browser();
        br.open('http://beacon.shinetechchina.com.cn/User/Login?returnUrl=/WorkReport')
        br._ua_handlers['_cookies'].cookiejar.save(self.cookie_file, ignore_discard=True, ignore_expires=True)
        br.select_form(nr = 0)
        br.form['DomainUserName'] = self.username
        br.form['Password'] = self.password
        br.submit()
        # for link in br.links():
        #     if(link.text=='Work Report'):
        #         br.click_link(link)
        #     print "%s:%s"%(link.text,link.url)
        # print br.geturl()
        # workReportLink = br.find_link(text_regex=re.compile("<i.*\sWork\sReport"))

        print br.geturl()
        br._ua_handlers['_cookies'].cookiejar.save(self.cookie_file, ignore_discard=True, ignore_expires=True)
        # br.select_form(action='/WorkReport/SubmitWorkAmount')
        # br.form['Hours'] = '8'
        # br.submit()
        content = br.response().read()
        # print(content)
        pattern = r'\s*var\sselectedWorkAmount\s=\{\"EmployeeId\"\:\"([\w\d-]*)\",\"PurchaseOrderId\"\:\"([\w\d-]*)\",\"ProjectItemId\"\:\"([\w\d-]*)\",\"Username\"\:"([\w\d]*)",.*,\"PurchaseOrder\":\"([\w\d-]*)\"\}\;'
        ret_match = re.search(pattern, content)
        if(ret_match):
            workDate = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
            data = {
                'selectedWorkAmount': {
                    'Description': description,
                    'EmployeeId': ret_match.group(1),
                    'Enabled': True,
                    'Hours': hours,
                    'ProjectItemId': ret_match.group(3),
                    'PurchaseOrder': ret_match.group(5),
                    'PurchaseOrderId': ret_match.group(2),
                    'Reason': 'today',
                    'Title': title,
                    'Username': ret_match.group(4),
                    'WorkDate': workDate,
                }
            }

            request = mechanize.Request("http://beacon.shinetechchina.com.cn/WorkReport/SubmitWorkAmount",json.dumps(data), headers={"Content-type":"application/json"})
            response = br.open(request)
            if self.debug:
                print response.read()

