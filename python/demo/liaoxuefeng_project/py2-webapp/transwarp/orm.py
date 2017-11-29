#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db
# ORM全称“Object Relational Mapping”，即对象-关系映射，

class Field(object):
    def __init__(self, column_type, primary_key=False, default=None, auto_increment=False):
        self.primary_key = primary_key
        self.column_type = column_type
        self.auto_increment = auto_increment  # 自增 Integer
        self.default = default                # 默认值：String / function

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.column_type)

class StringField(Field):
    def __init__(self, size=100, **kwargs):
        super(StringField, self).__init__('varchar({})'.format(size), **kwargs)

class IntegerField(Field):
    def __init__(self, **kwargs):
        super(IntegerField, self).__init__('bigint', **kwargs)

class BooleanField(Field):
    def __init__(self, **kwargs):
        super(BooleanField, self).__init__('Boolean', **kwargs)

class FloatField(Field):
    def __init__(self, **kwargs):
        super(FloatField, self).__init__('float', **kwargs)

class TextField(Field):
    def __init__(self, **kwargs):
        super(TextField, self).__init__('text', **kwargs)

class DatetimeField(Field):
    def __init__(self, **kwargs):
        super(DatetimeField, self).__init__('datetime', **kwargs)

class TimestampField(Field):
    def __init__(self, **kwargs):
        super(TimestampField, self).__init__('float', **kwargs)


# 元类
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()   # 读取cls的Field字段
        defaults = dict()
        primary_key = None  # 查找primary_key字段
        fields = []     # 读取cls除auto_increment外Field字段
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                # print('Found mapping: %s==>%s' % (k, v))
                mappings[k] = v
                if v.default:
                    defaults[k] = v.default
                if not v.auto_increment:
                    fields.append(k)
                if v.primary_key:
                    if primary_key:
                        raise RuntimeError('Duplicate primary key for field: {}'.format(k))
                    primary_key = k

        for k in mappings.iterkeys():
            attrs.pop(k)

        # 给cls增加一些字段：
        attrs['__table__'] = attrs.get('__table__', name)  # 读取cls的__table__字段
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__defaults__'] = defaults  # 保存默认值
        attrs['__fields__'] = fields       # 保存属性和列的映射关系 除了auto_increment
        attrs['__primary_key__'] = primary_key
        # 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
        attrs['__select__'] = 'select * from {}'.format(attrs['__table__'])
        attrs['__insert__'] = 'insert into {} ({}) values ({})'.format(attrs['__table__'], ','.join(fields),','.join(map(lambda x: '?', fields)))
        attrs['__update__'] = 'update {} set '.format(attrs['__table__'])
        attrs['__delete__'] = 'delete from {} '.format(attrs['__table__'])
        return type.__new__(cls, name, bases, attrs)


class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        # 设置默认值
        for k,v in self.__defaults__.items():
            if k not in self.keys():
                value = v() if callable(v) else v
                self['k'] = value
                # setattr(self, k, value)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            if key in self.__mappings__.keys():
                return None
            else:
                raise AttributeError(r"'Dict' object has no attribute '{}'".format(key))
    def __setattr__(self, key, value):
        self[key] = value


    def select(self, **kwargs):
        sql = self.__select__
        if kwargs != {}:
            sql = sql + ' where {}'.format(','.join(map(lambda i:'{}=`{}`'.format(i[0],i[1]),kwargs.items())))
        result = db.select(sql)
        return result

    def save(self):
        sql = self.__insert__
        args = [self.get(k) for k in self.__fields__]
        # print sql, args
        result = db.insert(sql, *args)
        return result

    def update(self, **kwargs):
        sql = self.__update__ + '{}'.format(','.join(map(lambda i:'{}={}'.format(i[0],i[1]),self.items())))

        if kwargs == {}:
            if not self.__primary_key__:
                raise RuntimeError('table {} has no primary key! '.format(self.__table__))
            try:
                sql = sql + ' where ({} = `{}`)'.format(self.__primary_key__, self[self.__primary_key__])
            except:
                raise RuntimeError('table {} Instance did not get value of primary key ({})'.format(self.__table__, self.__primary_key__))
        else:
            sql = sql + ' where ({})'.format(','.join(map(lambda i:'{}=`{}`'.format(i[0],i[1]),kwargs.items())))
        result = db.update(sql)
        return result

