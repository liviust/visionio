#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def basic():
    return render_template('basic.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            filename = os.path.join(
                app.config['UPLOAD_FOLDER'],
                '%s.%s' % (
                    now.strftime('%Y-%m-%d-%H-%M-%S-%f'),
                    file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            return jsonify({'success': True})
    return jsonify({'success': False})


def allowed_file(filename, allowed=['png', 'jpg', 'jpeg', 'gif']):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in allowed

if __name__ == '__main__':
    app.run(debug=True)
