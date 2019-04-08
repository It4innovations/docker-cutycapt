#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from flask import Flask, request, jsonify, send_file, after_this_request, abort
from pyvirtualdisplay import Display
import requests as rqlib
import os
import six
import subprocess
import sys
import tempfile
import urllib2

def parse_json(data):
    params = { 'url' : data['url'] }
    if 'min_width' in data:
        params['min_width'] = data['min_width']
    else:
        params['min_width'] = 1680
    if 'min_height' in data:
        params['min_height'] = data['min_height']
    else:
        params['min_height'] = 1280
    if 'delay' in data:
        params['delay'] = data['delay']
    else:
        params['delay'] = 0
    if 'out_format' in data:
        params['out_format'] = data['out_format']
    else:
        params['out_format'] = "png"
    if 'max_wait' in data:
        params['max_wait'] = data['max_wait']
    else:
        params['max_wait'] = 16000
    if 'resize' in data:
        params['resize'] = data['resize']
    else:
        params['resize'] = None

    return params

def cutycapt(url, min_width=1680, min_height=1280, delay=0, out_format = "png", max_wait = "4000", resize = None):
    """
    Runs cutycapt and send resulted snapshot.
    """
    suffix = "."+out_format
    fp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    filepath = fp.name
    fp.file.close()

    @after_this_request
    def cleanup(response):
        if os.path.exists(filepath):
            os.remove(filepath)
        return response

    try:
        req = urllib2.Request(url)
        contents = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        abort(e.code)

    display = Display(backend='xvfb', color_depth=16, size=(1280, 1024))
    display.start()
    subprocess.check_output(map(six.text_type, [
        'cutycapt',
        '--url={}'.format(url),
        '--out={}'.format(filepath),
        '--min-width={}'.format(min_width),
        '--min-height={}'.format(min_height),
        '--max-wait={}'.format(max_wait),
        '--delay={}'.format(delay),
    ]))
    display.stop()
    if out_format =='png':
        subprocess.check_output(map(six.text_type, [
            'mogrify',
            '-strip',
            '{}'.format(filepath),
        ]))
    if resize is not None:
        subprocess.check_output(map(six.text_type, [
            'mogrify',
            '-resize',
            '{}'.format(resize),
            '{}'.format(filepath),
        ]))
    fp = open(filepath)
    fp.seek(0)
    response = send_file(
        fp,
        as_attachment=True,
        add_etags=False,
        mimetype='image/'+out_format,
        attachment_filename=url.replace("https://","").replace("http://","")+suffix,
    )
    fp.seek(0, os.SEEK_END)
    size = fp.tell()
    fp.seek(0)
    del response.headers['Cache-Control']
    response.headers.extend({
        'Content-Length': size,
        'Cache-Control': 'no-cache'
    })
    return response


__app__ = Flask(__name__)
requests = rqlib.Session()


@__app__.route('/thumbnail', methods=['POST'])
def thumbnail():
    data = request.get_json()
    print data
    return cutycapt(**parse_json(data))

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    __app__.run(debug=True, host='0.0.0.0', port=5000)
