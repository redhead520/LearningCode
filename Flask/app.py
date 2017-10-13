#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Flask
from models import messages
import json

app = Flask(__name__)

@app.route('/')
def main():
    data = messages.query()
    return json.dumps(data)

if __name__ == '__main__':
    app.run()