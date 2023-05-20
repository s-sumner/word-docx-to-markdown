# app.py
import logging
import re
logging.basicConfig(filename='error.log', level=logging.DEBUG)

from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from docx2md import Converter
import os
import io
import zipfile
import mammoth

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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

            # Convert DOCX to Markdown
            with open(filepath, "rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file).value
            
            # Remove \ from markdown
            result = result.replace("\\.", ".").replace("\\)", ")").replace("\\-", "-").replace("\\(", "(")
            
            # Remove "https://learn.microsoft.com/en-us" from links and keep the remaining URL intact
            result = re.sub(r'https://learn.microsoft.com/[a-z]+-[a-z]+(/azure)?', '/azure', result)

            os.remove(filepath)
            return render_template('index.html', markdown_content=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
