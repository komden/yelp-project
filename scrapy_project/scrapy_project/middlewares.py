# -*- coding: utf-8 -*-

import scrapy
import logging
import random
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomProxyMiddleware(object):
    logger = logging.getLogger()

    def __init__(self):
        self.proxy_list = []
        self.proxy_file = get_project_settings().get('PROXY_LIST')[0]
        f = open(self.proxy_file, 'r')
        for line in f:
            line = line.strip('\n')
            self.proxy_list.append(line)
        f.close()
        self.logger.info("--- ALL proxy in proxy_list " + str(self.proxy_list) + " ---")
    
    def del_proxy(self, del_url_proxy):
        del_url_proxy = del_url_proxy
        self.logger.info("--- FROM del_proxy del_proxy_url ---" + str(del_url_proxy) + "---")
        try:
            self.proxy_list.remove(del_url_proxy)
            self.logger.info("--- Found del_proxy_url and delete with proxy_list. Show ALL proxy_list ---" + str(self.proxy_list) + "---")
        except:
            self.logger.info("--- NOT Found del_proxy_url in proxy_list. Show All proxy_list ---" + str(self.proxy_list) + "---")

    
    def process_request(self, request, spider):

        show_url_proxy = request.meta.get('proxy')
        req_retry = request.meta.get('retry_times', 0)
        ret_tim = get_project_settings().getint('RETRY_TIMES')
        if self.proxy_list:
            if req_retry == 0:
                proxy = random.choice(self.proxy_list)
                request.meta['proxy'] = proxy
                self.logger.info("--- proxy and url in request --- " + str(req_retry) + " --- "  + str(proxy) + " --- " + request.url + " ---")
            elif req_retry == ret_tim - 1:
                self.del_proxy(show_url_proxy)
                if self.proxy_list:
                    proxy = random.choice(self.proxy_list)
                    request.meta['proxy'] = proxy
                    self.logger.info("--- proxy and url in request --- " + str(req_retry) + " --- "  + str(proxy) + " --- " + request.url + " ---")
                else:
                    self.logger.info("--- Finished from process_request ---")
                    spider.crawler.stop()

class RandomUserAgentMiddleware(UserAgentMiddleware):
    logger = logging.getLogger()

    def __init__(self, user_agent=''):
        self.user_agent = user_agent
        self.user_agent_list = get_project_settings().getlist('USER_AGENT_LIST')

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
