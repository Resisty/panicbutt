#!/usr/bin/env python
""" Flask server for panicbutt
"""
import os
import threading
from flask import Flask
from flask import jsonify
from flask import send_from_directory
import playhouse.shortcuts
from app.plugins import jeff


STATIC_ROOT = os.path.abspath(os.path.curdir)
def spinoff_thread(func, args, kwargs=None):
    """ Create a thread to execute function func
        with arguments args. Args must be a list
    """
    thr = threading.Thread(target=func, args=args, kwargs=kwargs)
    thr.daemon = True
    thr.start()

APP = Flask(__name__, static_url_path=os.path.abspath(os.path.curdir))
APP.secret_key = os.urandom(32)

@APP.errorhandler(404)
def page_not_found(err):  # pylint: disable=unused-argument
    """ Handle 404
    """
    try:
        img_dir = os.path.join(STATIC_ROOT, 'img')
    # pylint: disable=broad-except
    except Exception:
        return ('Well met!'), 404
    return send_from_directory(img_dir, 'wellmet.png'), 404

@APP.errorhandler(500)
def page_not_found_500(err):  # pylint: disable=unused-argument
    """ Handle 500
    """
    try:
        img_dir = os.path.join(STATIC_ROOT, 'img')
    # pylint: disable=broad-except
    except Exception:
        return ('Well met!'), 500
    return send_from_directory(img_dir, 'wellmet.png'), 500

@APP.route('/', methods=['GET'])
def jeff_level():
    """ Create json response for Jeff's crisis level
    """
    jeff.psql_db.connect()
    recent = (jeff.Level
              .select()
              .join(jeff.JeffCrisis,
                    on=(jeff.Level.name == jeff.JeffCrisis.level))
              .order_by(jeff.JeffCrisis.id.desc())
              .get())
    info = playhouse.shortcuts.model_to_dict(recent)
    info['level'] = info['name'].upper()
    return jsonify(info)

@APP.route('/idunnolol', methods=['GET'])
def idunnolol():
    """ Super shitty slack '''app''''
    """
    data = {'response_type': 'in_channel',
            'text': 'i dunno lol  \xc2\xaf\\(\xc2\xb0_o)/\xc2\xaf',
           }
    return jsonify(data)


if __name__ == '__main__':
    APP.run(host='brianauron.info', port=8080, debug=True)
