# -*- coding:utf-8 -*-
import urllib
import urllib.request
import sys
import time
import re

start_time = time.time()
class Spider:
    def __init__(self):
        self.siteURL = 'https://5btf.com/arc/mainland/list_1_'
    # 输入页数，然后爬取页面的视频链接和名称
    def getPage(self,pageIndex):
        url = self.siteURL + str(pageIndex) + '.html'
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')

    # 输入视频详情页，返回视频下载链接
    def getVideoPage(self,address):
        response = urllib.request.urlopen(address)
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
                #print('https://5btf.com'+item[0], item[1]+' is downloading')
                url =self.getVideoPage('https://5btf.com'+item[0])
                # 检查文件名是否包含非法字符
                try:
                    global start_time
                    start_time = time.time()
                    filename = item[1]+'.mp4'
                    print(filename)
                    urllib.request.urlretrieve(url, filename, Schedule)
                    # 旧的方法没有进度条
                    # u = urllib.request.urlopen(url)
                    # data = u.read()
                    # f = open(item[1]+'.mp4', 'wb')
                    # f.write(data)
                except Exception as e:
                    print("Error: 下载失败",str(e))
                # finally:
                #     f.close()


#显示下载速度
'''
 urllib.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''
def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize
    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    time.sleep(0.1)
    f.write('\r')

# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)

if __name__ == '__main__':
    spider = Spider()
    for index in range(1,30):
        spider.getContents(index)
