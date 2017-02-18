#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cv2
from datetime import datetime
from flask import Flask, render_template, jsonify, request, url_for
from flask import send_from_directory

# ----------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object(__name__)

uploadFolder = 'upload'
app.config['UPLOAD_FOLDER'] = os.path.join('static', uploadFolder)

# ----------------------------------------------------------------------------

def allow(filename, allowed=['png', 'jpg', 'jpeg', 'gif']):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in allowed

# ----------------------------------------------------------------------------

def process(filename):
    img = cv2.imread(filename)
    result = cv2.Canny(img, 100, 200)
    fnTerms = filename.rsplit('.', 1)
    imgPath = '.'.join((fnTerms[0], 'result', fnTerms[1]))
    cv2.imwrite(imgPath, result)
    imgSrc = url_for('static', filename='/'.join((
        uploadFolder, os.path.split(imgPath)[1])))
    return {'img': imgSrc}

# ----------------------------------------------------------------------------

@app.route('/')
def basic():
    return render_template('basic.html')

# ----------------------------------------------------------------------------

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allow(file.filename):
            now = datetime.now()
            filename = os.path.join(
                app.config['UPLOAD_FOLDER'],
                '%s.%s' % (
                    now.strftime('%Y-%m-%d-%H-%M-%S-%f'),
                    file.filename.rsplit('.', 1)[1].lower()))
            file.save(filename)
            r = process(filename)
            return jsonify({'success': True, 'result': r})
    return jsonify({'success': False})

# ----------------------------------------------------------------------------

@app.route('/view/<path:path>', methods=['GET'])
def view(path):
    imgPath = url_for('static', filename='/'.join((uploadFolder, path)))
    return render_template('basic.html', imgPath=imgPath)

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)

# ----------------------------------------------------------------------------
