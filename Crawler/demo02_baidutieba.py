#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import os
#百度贴吧爬虫类
class Tool():
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    @staticmethod
    def replace(x):
        x = re.sub(Tool.removeImg, "", x)
        x = re.sub(Tool.removeAddr, "", x)
        x = re.sub(Tool.replaceLine, "\n", x)
        x = re.sub(Tool.replaceTD, "\t", x)
        x = re.sub(Tool.replacePara, "\n    ", x)
        x = re.sub(Tool.replaceBR, "\n", x)
        x = re.sub(Tool.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

class BDTB():

    def __init__(self, baseURL, seeLZ, floorTag=None):
        self.baseURL = baseURL
        self.seeLZ = '?see_lz={0}'.format(seeLZ)
        self.tool = Tool.replace
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getPage(self, pageNum):
        url = self.baseURL + self.seeLZ + '&pn={0}'.format(pageNum)
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u'连接百度贴吧失败,错误原因', e.reason
                return None

    def getTitle(self, page=None):
        if not page:
            page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page=None):
        if not page:
            page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()

    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        return map(lambda item: self.tool(item), items)

    def setFileTitle(self, title=None):
        # 如果标题不是为None，即成功获取到标题
        title = title.decode('utf-8') if title else self.defaultTitle
        file_dir = os.path.join(os.path.abspath('.'), title + ".txt" )
        self.file = open(file_dir, "w")

    def writeData(self, contents):
        for index, item in enumerate(contents):
            if self.floorTag:
                floorLine = "\n{0}".format(index + 1) + "-"*100 + '\n'
                self.file.write(floorLine)
            self.file.write(item)


    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL已失效，请重试"
            return
        try:
            print title
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1, int(pageNum) + 1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
            self.file.close()
        # 出现写入异常
        except IOError, e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"


if __name__ == "__main__":
    print u"请输入帖子代号"
    baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
    seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
    floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
    bdtb = BDTB(baseURL, seeLZ, floorTag)
    bdtb.start()
