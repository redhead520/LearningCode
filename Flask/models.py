#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sqlite3
import json

class model(object):

    @staticmethod
    def execute(*args):
        conn = sqlite3.connect('message')
        cursor = conn.cursor()
        cursor.execute(*args)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def init():
        sql = 'create table messages (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,params TEXT, time TEXT,result TEXT)'
        messages.execute(sql)

    @staticmethod
    def query(table_name):
        sql = 'select * from {0}'.format(table_name)
        conn = sqlite3.connect('message')
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        # result = rows
        result = []
        for row in rows:
            item = messages(*row)
            # item = apply(table_name, row)
            item = item.__dict__
            result.append(item)
        conn.commit()
        cursor.close()
        conn.close()
        return result




class messages(model):

    def __init__(self, id=None, name=None,params=None,time=None,result=None):
        self.id = id
        self.name = name
        self.params = params
        self.time = time
        self.result = result
        # self.save()

    def save(self):
        sql = 'insert into messages VALUES (?,?,?,?,?)'
        values = (self.id, self.name, self.params, self.time, self.result)
        result = messages.execute(sql, values)
        return result

    @staticmethod
    def query():
        return model.query('messages')

    def __str__(self):
        return json.dumps(self.__dict__)



