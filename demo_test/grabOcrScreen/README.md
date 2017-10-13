(Linux-ubuntu系统)

1. pytesser 调用了 tesseract，因此需要安装 tesseract，安装 tesseract 需要安装 leptonica，否则编译tesseract 的时候出现 "configure: error: leptonica not found"。

```sh
sudo apt-get install tesseract-ocr

sudo pip install pytesseract
```
