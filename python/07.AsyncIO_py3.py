#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 协程，又称微线程，纤程。英文名Coroutine。
# Python对协程的支持是通过generator实现的
# python 2.7 通过greenlet实现协程,gevent只能在Unix/Linux下运行
# python 3.4 asyncio是Python 3.4版本引入的标准库，提供了完善的异步IO支持, 异步操作需要在coroutine中通过yield from完成；
# python 3.5 async和await: 1. 把@asyncio.coroutine替换为async；2. 把yield from替换为await。

# asyncio
# asyncio的编程模型就是一个消息循环。我们从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO。
def test_asyncio():
    import asyncio
    import threading

    @asyncio.coroutine # 把一个generator标记为coroutine类型
    def hello():
        print('Hello world! (%s)' % threading.currentThread())
        yield from asyncio.sleep(1)   # 如果把asyncio.sleep()换成真正的IO操作，则多个coroutine就可以由一个线程并发执行。
        print('Hello again! (%s)' % threading.currentThread())

    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    # loop.run_until_complete(hello())
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

# async和await
def test_async_await():
    import asyncio
    import threading

    async def hello():
        print('Hello world! (%s)' % threading.currentThread())
        await asyncio.sleep(1)  # 如果把asyncio.sleep()换成真正的IO操作，则多个coroutine就可以由一个线程并发执行。
        print('Hello again! (%s)' % threading.currentThread())

    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    # loop.run_until_complete(hello())
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    # help()
    # test_asyncio()
    test_async_await()
    pass