# !/usr/bin/env python2
# -*- coding: utf-8 -*-

# 协程，又称微线程，纤程。英文名Coroutine。
# Python对协程的支持是通过generator实现的
# python 2.7 通过greenlet实现协程,gevent只能在Unix/Linux下运行
# python 3.4 asyncio是Python 3.4版本引入的标准库，提供了完善的异步IO支持, 异步操作需要在coroutine中通过yield from完成；
# python 3.5 async和await: 1. 把@asyncio.coroutine替换为async；2. 把yield from替换为await。

# gevent
def test_gevent():
    from gevent import monkey
    monkey.patch_socket()
    import gevent

    def f(n):
        for i in range(n):
            print gevent.getcurrent(), i
            gevent.sleep(0) # 可以通过gevent.sleep()交出控制权：
    # 实际代码里，我们不会用gevent.sleep()去切换协程，而是在执行到IO操作时，gevent自动切换
    g1 = gevent.spawn(f, 5)
    g2 = gevent.spawn(f, 5)
    g3 = gevent.spawn(f, 5)
    g1.join()
    g2.join()
    g3.join()

def test_gevent_joinall():
    from gevent import monkey
    monkey.patch_all()
    import gevent
    import urllib2

    def f(url):
        print('GET: %s' % url)
        resp = urllib2.urlopen(url)
        data = resp.read()
        print('%d bytes received from %s.' % (len(data), url))

    gevent.joinall([
        gevent.spawn(f, 'https://www.python.org/'),
        gevent.spawn(f, 'https://www.yahoo.com/'),
        gevent.spawn(f, 'https://github.com/'),
    ])




if __name__ == '__main__':
    # help()
    test_gevent()
    # test_asyncio()
    pass