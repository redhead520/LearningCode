# /usr/bin/env python2
# -*- coding: utf-8 -*-
try:
    from PIL import ImageGrab
except ImportError:
    pass
# bbox = (100, 200, 400, 500)
# im = ImageGrab.grab(bbox)
# im.show()
# print '333'

import pytesseract
import Image

# image = Image.open('img/1.JPEG')
# image = Image.open('img/2.jpg')
image = Image.open('img/ddd.JPEG')
image.show()
print pytesseract.image_to_string(image)