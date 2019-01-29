#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import urllib.request

import re
regex_url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

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
    url_new = apply_template(templ, url, False)
    if re.match(regex_url, url_new) is None:
        return None
    else:
        return url_new

def vampire_pipeline(url):
    templates = [
        "47C2140E-7921-49B4-6957-18A0264A00B5", # teeth
        "7BDF43DF-DDB9-1A94-393D-F4071671F620", # eyes
        "27AD8C60-16BE-5EC4-FDD3-9F658D461EE4", # color
        "E82456F0-349B-7724-C9FF-6DE46815CBA7", # segm
    ]
    err_step = None
    for i, templ in enumerate(templates):
        url_new = apply_template(templ, url, False)
        if re.match(regex_url, url_new) is None:
            print("error on step", i)
            err_step = i
        else:
            url = url_new

    return url, err_step

def store(url, local):
    urllib.request.urlretrieve(url, local)
