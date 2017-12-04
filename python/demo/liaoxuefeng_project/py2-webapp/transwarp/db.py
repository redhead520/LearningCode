#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import threading
import logging
import mysql.connector
# level: CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(process)d %(thread)d %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                 )


# 数据库引擎对象:
class _Engine(object):
    _connect = None
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(_Engine, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    def connect(self):
        return self._connect()


engine = None


class _LasyConnection(object):
    """
    惰性连接对象
    仅当需要cursor对象时，才连接数据库，获取连接
    """

    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            engine = _Engine()
            self.connection = engine.connect()
            logging.info('[CONNECTION] [OPEN] connection <%s>...' % hex(id(self.connection)))
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            logging.info('[CONNECTION] [CLOSE] connection <%s>...' % hex(id(_connection)))
            _connection.close()


# 持有数据库连接的上下文对象:
class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        self.connection = _LasyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()

_db_ctx = _DbCtx()

# 数据库连接的上下
class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()

# 数据库事务的上下
class _TransactionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions = _db_ctx.transactions + 1
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions = _db_ctx.transactions - 1
        try:
            if _db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()

    def commit(self):
        global _db_ctx
        try:
            _db_ctx.connection.commit()
        except:
            _db_ctx.connection.rollback()
            raise

    def rollback(self):
        global _db_ctx
        _db_ctx.connection.rollback()

def connection():
    return _ConnectionCtx()

def transaction():
    return _TransactionCtx()

def with_connection(sql_func):
    def func(*args, **kwargs):
        with _ConnectionCtx():
            result = sql_func(*args, **kwargs)
        return result
    return func

def with_transaction(sql_func):
    def func(*args, **kwargs):
        with _TransactionCtx():
            result = sql_func(*args, **kwargs)
        return result
    return func



def create_engine(user='root', password='password', database='test', host='127.0.0.1', port=3306):
    db_config = {
        'user' : user,
        'password' : password,
        'database' : database,
        'host' : host,
        'port' : port
    }
    engine = _Engine()
    engine._connect = lambda:mysql.connector.connect(**db_config)


@with_connection
def select(sql, *args):
    global _db_ctx
    cursor = _db_ctx.cursor()
    try:
        cursor.execute(sql, *args)
        data = cursor.fetchall()
        keys = [k[0] for k in cursor.description]
        result = []
        for item in data:
            result.append(dict(zip(keys,item)))
    except mysql.connector.Error, e:
        result = e
    return result

@with_transaction
def update(sql, *args):
    global _db_ctx
    cursor = _db_ctx.cursor()
    try:
        result = cursor.execute(sql, *args) # None
    except mysql.connector.Error, e:
        result = e
    return result

@with_transaction
def insert(sql, *args):
    global _db_ctx
    cursor = _db_ctx.cursor()
    try:
        result = cursor.execute(sql, *args) # None
    except mysql.connector.Error, e:
        result = e
    return result

@with_transaction
def delete(sql, *args):
    global _db_ctx
    cursor = _db_ctx.cursor()
    try:
        result = cursor.execute(sql, *args) # None
    except mysql.connector.Error, e:
        result = e
    return result

# ###############################
# 多事务例子：
# db.create_engine(...)
# with db.connection():
#     db.select('...')
#     db.update('...')
#     db.update('...')
#
# with db.transaction():
#     db.select('...')
#     db.update('...')
#     db.update('...')