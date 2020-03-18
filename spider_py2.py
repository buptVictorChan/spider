# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class Spider:

    def __init__(self):
        self.siteURL = 'https://5btf.com/arc/mainland/list_1_'
# 输入页数，然后爬取页面的视频链接和名称
    def getPage(self,pageIndex):
        url = self.siteURL + str(pageIndex) + '.html'
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    # 输入视频详情页，返回视频下载链接
    def getVideoPage(self,address):
        request = urllib2.Request(address)
        response = urllib2.urlopen(request)
        pattern = re.compile('click_download_btn.*?href="(.*?)".*?target', re.S)
        items = re.findall(pattern, response.read().decode('utf-8'))
        return items[0]

# 爬取具体视频地址，下载并保存
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="t_p">.*?<h3><a href="(.*?)">(.*?)</a>.*?<span>''.*?</span>',re.S)
        items = re.findall(pattern,page)
        for item in items:
            if 'mainland' in item[0]:
                print 'https://5btf.com'+item[0], item[1]+' is downloading'
                download =self.getVideoPage('https://5btf.com'+item[0])
                u = urllib.urlopen(download)
                data = u.read()
                f = open(item[1]+'.mp4', 'wb')
                f.write(data)
                f.close()
                #修改了一点点

if __name__ == '__main__':
    spider = Spider()
    for index in range(30,100):
        spider.getContents(index)
