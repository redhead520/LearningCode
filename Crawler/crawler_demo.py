#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
# 爬取糗事百科段子
class QSBK():
    """
     1.抓取糗事百科热门段子http://www.qiushibaike.com/
     2.过滤带有图片的段子
     3.实现每按一次回车显示一个段子的发布人，段子内容，点赞数。
     :return:
    """
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/{0}'.format(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            html = response.read().decode('utf-8')
            return html
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败,错误原因", e.reason
                return None

    def getPageItems(self, pageIndex):
        html = self.getPage(pageIndex)
        if not html:
            print "页面加载失败...."
            return None
        parttern = re.compile(
            '<div class="article.*?<div class="author.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?<!-- .*?gif -->(.*?)<div class="stats.*?<i class="number">(.*?)</i>',
            re.S)
        items = re.findall(parttern, html)
        pageStories = []
        for item in items:
            if item[2].strip() == '':
                content = item[1].strip()
                content = content.replace('<br/><br/>', '\n')
                content = content.replace('<br/>', '\n')
                pageStories.append([
                    item[0].strip(),
                    content,
                    item[3].strip()
                ])
        return pageStories
    def loadPage(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            while len(self.stories) < 3:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            input = raw_input('====请按回车' + '='*100)
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 如果输入Q则程序结束
            if input == "Q" or input == "q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞:%s\n%s" % (page, story[0], story[2], story[1])
            # 开始方法

    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories, nowPage)



if __name__ == "__main__":
    spider = QSBK()
    spider.start()
    pass
