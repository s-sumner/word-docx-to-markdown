# app.py
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from docx2md import Converter
import os
import io
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            converter = Converter(filepath)
            result = converter.convert()


            os.remove(filepath)
            return render_template('index.html', markdown_content=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
