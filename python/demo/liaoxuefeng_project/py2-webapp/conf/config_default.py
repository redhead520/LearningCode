#!/usr/bin/env python
# -*- coding: utf-8 -*-

' a test module '
import os
configs = {
    'db': {
        'user':'root',
        'password':'123456',
        'database':'test',
        'host':'127.0.0.1',
        'port':3306
    },
    'root':os.path.dirname(os.path.abspath('.')),
    'www':os.path.join(os.path.abspath('.'),'www'),
    'static':os.path.join(os.path.abspath('.'),'www','static'),
    'template_url': os.path.join('www','templates'),
    'cookie':{
        'sccretName': 'aw_id',
        'secretKey':'#@?ddsed'
    }
}