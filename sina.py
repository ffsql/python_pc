#-*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
#import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree


if __name__ == '__main__':
    if(len(sys.argv) >=2):
        user_id = (int)(sys.argv[1])
    else:
        user_id = int(input("请输入user_id: "))

    cookie = {"Cookie": "MLOGIN=0; _T_WM=831d5273dc96f014859c254c73729ffc; WEIBOCN_FROM=1110003030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803_ctg1_1988_-_ctg1_1988%26uicode%3D20000174%26fid%3D102803_ctg1_4388_-_ctg1_4388; FID=2YTJcf0OcAANL82dCAsxMQwroGJ8GU9dTBWxvZ2lu; SUB=_2A25xezP9DeRhGeNI61IQ-S_LzziIHXVShF21rDV6PUJbktAKLWvmkW1NSKkoKB-WuMvXnoSS-jm_KnVs9d0R5toL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFAcGXRhkGcTDYBpAoXcPJ75NHD95QfSo57eK.pS0BXWs4DqcjeUgDQIJyfI05peKBX; SUHB=0sqBeDAx-M2h1x; SSOLoginState=1551844268"}
    url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id

    htmlss = requests.get(url, cookies = cookie).content()
    #print(html.content())5075579048
    htmlss.encoding = 'utf8'
    print(htmlss)
    selector = etree.HTML(htmlss)
    pageNum = int(selector.xpath('//input[@name="mp"]')[0].attrib['value'])



    result = ""
    urllist_set = set()
    word_count = 1
    image_count = 1

    print('爬虫准备就绪...')

    for page in range(1,pageNum+1):

      #获取lxml页面
      url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page)
      lxml = requests.get(url, cookies = cookie)
      lxml.encoding = 'utf8'
      #文字爬取
      selector = etree.HTML(lxml.content)
      content = selector.xpath('//span[@class="ctt"]')
      for each in content:
        text = each.xpath('string(.)')
        if word_count >= 4:
          text = "%d :"%(word_count-3) +text+"\n\n"
        else :
          text = text+"\n\n"
        result = result + text
        word_count += 1

      #图片爬取
      soup = BeautifulSoup(lxml, "lxml")
      urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
      first = 0
      for imgurl in urllist:
        urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
        image_count +=1

    fo = open("/Users/Personals/%s"%user_id, "wb")
    fo.write(result)
    word_path=os.getcwd()+'/%d'%user_id
    print(u'文字微博爬取完毕')

    link = ""
    fo2 = open("/Users/Personals/%s_imageurls"%user_id, "wb")
    for eachlink in urllist_set:
      link = link + eachlink +"\n"
    fo2.write(link)
    print( u'图片链接爬取完毕')

    if not urllist_set:
      print( u'该页面中不存在图片')
    else:
      #下载图片,保存在当前目录的pythonimg文件夹下
      image_path=os.getcwd()+'/weibo_image'
      if os.path.exists(image_path) is False:
        os.mkdir(image_path)
      x=1
      for imgurl in urllist_set:
        temp= image_path + '/%s.jpg' % x
        print(u'正在下载第%s张图片' % x)
        try:
          urllib.urlretrieve(urllib.request.urlopen(imgurl).geturl(),temp)
        except:
          print(u"该图片下载失败:%s"%imgurl)
        x+=1

    print(u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path))
    print(u'微博图片爬取完毕，共%d张，保存路径%s'%(image_count-1,image_path))