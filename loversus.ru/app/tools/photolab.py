#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests

def apply_template(template_name, url_clear, anim = False):
    post_url = 'http://api-hack.photolab.me/template_process.php'
    data = {
        'template_name': template_name,
        'image_url[1]': url_clear,
    }

    if anim:
        data['animated'] = "1"

    response = requests.post(post_url, data=data)
    result_url = response.text

    return result_url

def segmentation(url):
    templ = "E82456F0-349B-7724-C9FF-6DE46815CBA7"
    return apply_template(templ, url, False)

def vampire_pipeline(url):
    templates = [
        "E82456F0-349B-7724-C9FF-6DE46815CBA7", # segm
        "47C2140E-7921-49B4-6957-18A0264A00B5", # teeth
        "7BDF43DF-DDB9-1A94-393D-F4071671F620", # eyes
        "27AD8C60-16BE-5EC4-FDD3-9F658D461EE4", # color
    ]

    for templ in templates:
        url = apply_template(templ, url, False)

    return url
