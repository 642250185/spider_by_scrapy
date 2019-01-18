# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request as urllib2
import os

import _thread

from pic.spiders.hisdb import DemoDB

img_list_db = DemoDB("img_list.slqite3.db",False)

def IsExist(filename):

    root = "F:\\Code\\Self\\github\\pacong\\pic\\"

    root2 = "F:\\Image\\"

    root3 = "F:\\zbjuran\\"

    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            if filename == filepath :
                return True

    for dirpath, dirnames, filenames in os.walk(root2):
        for filepath in filenames:
            if filename == filepath :
                return True

    for dirpath, dirnames, filenames in os.walk(root3):
        for filepath in filenames:
            if filename == filepath :
                return True
    
    return False

def thread_download_img(item):

    if img_list_db.query(item['addr']):
        print("already downloaded:",item['addr'],item['name'])
        return True
    else:
        
        file_name = os.path.join(r'./zbjuran/',item['name']+'.jpg')
        if not os.path.exists(file_name) and not IsExist(item['name']+'.jpg'):
            print ("get  " , item['addr'])
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
            req = urllib2.Request(url=item['addr'],headers=headers)
            
            try:
                res = urllib2.urlopen(req,timeout=10)
                
                with open(file_name,'wb') as fp:
                    fp.write(res.read())
                print("geted:",item['addr'],file_name)  
            except :
                print("get error ")
                return False
        else:
              print("exist:",item['addr'],file_name)  

        img_list_db.insert(item['addr'],item['name'])
        return True

class PicPipeline(object):
    def process_item(self, item, spider):
        
        #try:
        #    _thread.start_new_thread(thread_download_img,(item,))
        #except:
        #    print ("error in start thread.")
        thread_download_img(item)

        return item
