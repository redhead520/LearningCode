#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config_default import configs

try:
    from config_override import configs as product_configs
    configs.update(product_configs)
except ImportError:
    pass