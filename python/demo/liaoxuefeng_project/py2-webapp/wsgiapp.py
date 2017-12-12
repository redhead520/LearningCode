#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging; logging.basicConfig(level=logging.INFO)
from transwarp import db
from transwarp.web import *
from conf.config import configs
import urls
import os

db.create_engine(**configs['db'])
wsgi = WSGIApplication()
wsgi.add_module(urls)
wsgi.add_interceptor(urls.user_interceptor)
wsgi.add_interceptor(urls.mange_interceptor)


# 初始化jinja2模板引擎:
template_engine = Jinja2TemplateEngine(os.path.join(os.path.dirname(os.path.abspath(__file__)), configs['template_url']))
template_engine.add_filter('datetime', datetime_filter)
WSGIApplication.template_engine = template_engine



if __name__ == '__main__':
    # 开发模式（Development Mode）
    wsgi.run()
else:
    # 产品模式（Production Mode）
    application = wsgi.get_wsgi_application()