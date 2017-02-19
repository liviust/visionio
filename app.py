#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cv2
from datetime import datetime
from flask import Flask, render_template, jsonify, request, url_for, abort
from flask import send_from_directory

# ----------------------------------------------------------------------------

def img2imgProcess(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

def getUploadPath(filename):
    return os.path.join(
        app.config['UPLOAD_FOLDER'],
        '%s.%s' % (datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f'),
                   filename.rsplit('.', 1)[1].lower()))

# ----------------------------------------------------------------------------

@app.route('/io/<mode>', methods=['GET', 'POST'])
def io(mode):
    if mode not in ('img2img', 'imgimg2imgimg'):
        abort(404)
    if request.method == 'GET':
        return render_template('%s.html' % mode)
    elif request.method == 'POST':
        file = request.files['file']
        if file and allow(file.filename):
            path = getUploadPath(file.filename)
            file.save(path)
            if mode == 'img2img' or mode == 'imgimg2imgimg':
                img = cv2.imread(path)
                resultImg = img2imgProcess(img)
                fnTerms = path.rsplit('.', 1)
                imgPath = '.'.join((fnTerms[0], 'result', fnTerms[1]))
                cv2.imwrite(imgPath, resultImg)
                imgURL = url_for('static', filename='/'.join((
                    uploadFolder, os.path.split(imgPath)[1])))
                result = {'img': imgURL}
            return jsonify({'success': True, 'info': result})
        else:
            return jsonify({'success': False, 'info': 'invalid file(s)'})

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)

# ----------------------------------------------------------------------------
