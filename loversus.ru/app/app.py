#! /usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask, request, json, g
import os, json
import time
from typing import Optional, Tuple
import sqlite3
from PIL import Image

from tools.photolab import vampire_pipeline, segmentation, store

application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
application.config['UPLOAD_FOLDER'] = '../uploaded'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

DATABASE = '/root/loversus.ru/app/database.db'
def get_db() -> sqlite3.Connection:
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@application.teardown_appcontext
def close_connection(exception) -> None:
    db = getattr(g, '_database', None)
    if db is not None:
        db.commit()
        db.close()


def get_path_by_id(user_id: int) -> str:
    return '/root/loversus.ru/processed/%d.png' % user_id


def get_url_by_id(user_id: int) -> str:
    return 'loversus.ru/processed/%d.png' % user_id


def get_or_create_id_count(user_id: Optional[int] = None) -> Optional[Tuple[int, int]]:
    if user_id is None:
        cur = get_db().execute('insert into loversus (count) values (0)')
        cur.close()
        cur = get_db().execute('select id, count from loversus where rowid = last_insert_rowid()')
    else:
        cur = get_db().execute('select id, count from loversus where id = $1', (user_id,))
    rv = cur.fetchall()
    cur.close()
    if len(rv) > 0:
        return rv[0]
    else:
        return None

def on_bite(user_id: int) -> None:
    cur = get_db().execute('update loversus set count = count + 1 where id = $1', (user_id,))
    cur.close()


def init_table():
    cur = get_db().execute("CREATE TABLE loversus (id integer PRIMARY KEY, count integer)")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/app')
def hello():
    return "app"

@application.route('/app/bitecount', methods=['POST'])
def bitecount():
    if 'hunter_id' not in request.form:
        return json.dumps({'status': 'fail', 'desc': 'No hunter id'})
    try:
        hunter_id = int(request.form['hunter_id'])
    except:
        return json.dumps({'status': 'fail', 'desc': 'hunter id incorrect'})

    _, count = get_or_create_id_count(hunter_id)

    return json.dumps({'status': 'ok', 'count': count})


@application.route('/app/photoupload', methods=['POST'])
def photoupload():
    # print(request.files)
    if 'photo' not in request.files:
        return json.dumps({'status': 'fail', 'desc': 'No file part'})
    if 'hunter_id' not in request.form:
        return json.dumps({'status': 'fail', 'desc': 'No hunter id'})

    file = request.files['photo']

    try:
        hunter_id = int(request.form['hunter_id'])
    except:
        return json.dumps({'status': 'fail', 'desc': 'hunter id incorrect'})


    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return json.dumps({'status': 'fail', 'desc': 'No selected file'})
    if file and allowed_file(file.filename):
        on_bite(hunter_id)
        hunterized_id, count = get_or_create_id_count()

        ext = file.filename.split(".")[-1]

        filename = "../tmp/{}.{}".format(hunterized_id, ext)
        file.save(filename)

        if ext != "png":
            im = Image.open(filename)
            os.remove(filename)
            filename = "../tmp/{}.png".format(hunterized_id)
            im.save(filename)

        url = "https://loversus.ru/tmp/{}.png".format(hunterized_id)

        url_segm = segmentation(url)
        if url_segm is None:
            return json.dumps({'status': 'fail', 'desc': 'no segmentation possible'})

        store(url_segm, filename)

        # call opencv here for filename
        #

        url_new_hunter, err_step = vampire_pipeline(url_segm)


        filename_processed = "../processed/{}.png".format(hunterized_id)
        store(url_new_hunter, filename_processed)
        url_new_hunter = "https://loversus.ru/processed/{}.png".format(hunterized_id)

    return json.dumps({'status': 'ok', 'hunterized': hunterized_id, 'url': url_new_hunter})


@application.route('/flask_api/<path:secret>', methods=['POST'])
def hello_flask_api(secret):
    return 'ok {}'.format(secret)
