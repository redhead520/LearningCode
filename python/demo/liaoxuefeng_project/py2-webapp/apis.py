#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models.allmodels import Blog

class Page(object):
    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index < 1) or (page_index > self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

def get_models_by_page(model, page_index, where=None, page_size=10):
    total = model.count_all()
    page = Page(total, page_index, page_size=page_size)
    result = model.find_by(where=where,order='created_at', offset=page.offset, limit=page.limit)
    return result, page


