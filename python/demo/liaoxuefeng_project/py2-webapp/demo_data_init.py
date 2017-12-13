#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp import db
from models.allmodels import User, Blog, Comment
from transwarp.web import *
from conf.config import configs
import random
db.create_engine(**configs['db'])


# b = Blog()
# c = Comment
#
# b.save()
# c.save()
users_ids = User.all()
for user in users_ids:
    print user

# blogs = Blog.all()
# print '-all blogs:'
# print blogs
# exit()
# 生成10个blogs
# for i in range(4,5):
#     user = random.sample(users_ids, 1)[0]
#     print 'add blogs {}'.format(i)
#     print user
#     title = 'Google '
#     summary = 'After coming up with a really good recipe within Google. Read more'
#     content = 'We baked it, and our eager taste-testers—Googlers ready and willing to sacrifice for science by eating the cookies—tasted it and gave it a numerical score relative to store-bought cookie samples. We fed that rating back into the system, which learned from the rating and adjusted those “knobs” to create a new recipe. We did this dozens of times—baking, rating, and feeding it back in for a new recipe—and pretty soon the system got much better at creating tasty recipes.'
#
#
#     b = Blog(id=str(i), user_id=str(user['id']), user_name=str(user['name']), user_image=str(user['image']), name=title, summary=summary, content=content)
#     print b.save()


# blog = random.sample(blogs, 1)[0]
#
#
# content = 'The Chocolate Chip and Cardamom Cookie.'
# c = Comment(id='5',blog_id=str(blog['id']), user_id=str(user['id']),user_name=str(user['name']), user_image=str(user['image']),content=content)
# c.save()


# create admin user
admin = User(name='admin', email='admin@126.com',password='21232f297a57a5a743894a0e4a801fc3',admin=True)
# admin.save()
print 'done'