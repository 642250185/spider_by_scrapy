# -*- coding: utf-8 -*-
import scrapy
import sys
import os
from pic.items import PicItem

from pic.spiders.hisdb import DemoDB

class XhSpider(scrapy.Spider):
    name = 'xh'
    allowed_domains = ['www.zbjuran.com']
    # 初始URL
   # start_urls = ['https://www.zbjuran.com/mei/']
   # scrapy crawl xh --nolog
    start_urls = ['https://www.zbjuran.com/mei/']
    # 设置一个空集合
    #url_set = set()

    url_list_db = DemoDB("url_list.slqite3.db",False)

    def parse(self, response):
        
        if (False == XhSpider.url_list_db.query(response.url,1)):

            XhSpider.url_list_db.update(response.url)

            #print ("2.get img ing ...... ",sys._getframe().f_lineno)

            if response.url.startswith("https://www.zbjuran.com/mei/"):
                allPics = response.xpath('//center/div[@class="picbox"]')

                #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                for pic in allPics:
                    # 分别处理每个图片，取出名称及地址
                    #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                    item = PicItem()
                    #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                    addr = ""
                    if len(pic.xpath('./img/@src')) >=1:
                        addr = pic.xpath('./img/@src').extract()[0]
                    else:
                        addr = pic.xpath('./p/img/@src').extract()[0]

                    #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                    name_1 = response.xpath('//div[@class="title"]/h2/text()').extract()[0]
                    #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                    #print (name_1)
                    name_2 = addr.replace('/','_').replace(':','_')

                    name=""
                
                    name_obj = pic.xpath('./img/@alt')
                    if len(name_obj) >= 1:
                        name = name_obj.extract()[0]                    
                
                    
                    
                    if len(name_1) >= 1 :
                        item['name'] = name_1
                    else :
                        if len(name) >= 1:
                            item['name'] = name
                        else:
                            item['name'] = name_2
                        

                    if addr.startswith('/'):
                        addr = "https://www.zbjuran.com/"+addr

                    item['addr'] = addr
                    # 返回爬取到的信息
                    #print ("hav:",item['addr'],item['name'])
                    #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                    yield item
                print ("2.get img ing ...... ",sys._getframe().f_lineno )
            # 获取所有的地址链接
            #print ("2.get href ing ...... ")
            urls= response.xpath("//a/@href").extract()
        
            for url in urls:
                #print(url)
                url_arr = url.split("_")
                # 如果地址以http://www.xiaohuar.com/list-开头且不在集合中，则获取其信息
                if url.startswith("/mei/") and url.endswith(".html"):
                    
                    url_whole = "https://www.zbjuran.com"+url

                    if XhSpider.url_list_db.query(url_whole):
                        #print ("Exist:",url,url_whole)
                        pass
                        
                    else:
                        #XhSpider.url_set.add(url_whole)
                        XhSpider.url_list_db.insert(url_whole)
                        # 回调函数默认为parse,也可以通过from scrapy.http import Request来指定回调函数
                        # from scrapy.http import Request
                        # Request(url,callback=self.parse)
                        print ("add",url_whole)
                        yield self.make_requests_from_url(url_whole)
                elif url_arr[0].isdigit():
                    u_arr = response.url.split("/")
                    u_arr.pop()
                    u_arr.append(url)

                    url_whole="/"

                    url_whole = url_whole.join(u_arr)

                    if  XhSpider.url_list_db.query(url_whole):
                        #print ("Exist:",url,url_whole)
                        pass
                        
                    else:
                        print ("add",url_whole)
                        #XhSpider.url_set.add(url_whole)
                        XhSpider.url_list_db.insert(url_whole)
                        # 回调函数默认为parse,也可以通过from scrapy.http import Request来指定回调函数
                        # from scrapy.http import Request
                        # Request(url,callback=self.parse)
                        yield self.make_requests_from_url(url_whole)
                elif url.startswith("http") and url.endswith(".html"):
                    
                    url_whole = url

                    if XhSpider.url_list_db.query(url_whole):
                        #print ("Exist:",url,url_whole)
                        pass
                    else:
                        #XhSpider.url_set.add(url_whole)
                        XhSpider.url_list_db.insert(url_whole)
                        # 回调函数默认为parse,也可以通过from scrapy.http import Request来指定回调函数
                        # from scrapy.http import Request
                        # Request(url,callback=self.parse)
                        print ("add",url_whole)
                        yield self.make_requests_from_url(url_whole)
                else:             

                    pass
        
        
        print ("3.get waiting href ... ")

        url_whole =  XhSpider.url_list_db.query_data()

        if len(url_whole) > 10:
            yield self.make_requests_from_url(url_whole)
        else:
            print ("4. we finished this site")





