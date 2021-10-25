#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @DATETIME:2021/10/2417:09
# @NAME:flask/qr_code

import qrcode


def make_qrcode(input_data):
    img = qrcode.make(input_data)
    img.save('static/qrcode.png')
    return './static/qrcode.png'
