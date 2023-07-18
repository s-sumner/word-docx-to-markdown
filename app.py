import logging
import re
import os
import io
import lxml.etree
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from docx import Document
import mammoth
from tabulate import tabulate

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def word_table_to_markdown(filename):
    doc = Document(filename)
    markdown_content = []

    for i, table in enumerate(doc.tables):
        data = []

        for row in table.rows:
            cell_data = []

            for cell in row.cells:
                cell_data.append(cell.text)

            data.append(cell_data)

        markdown_content.append(tabulate(data, tablefmt="pipe", headers="firstrow"))

    return markdown_content

def generate_markdown_table(text):
    pattern = r"(?s).*?(?:\n\n|\Z){0,300}"
    matches = re.findall(pattern, text)
    rows = len(matches)
    columns = text.count('\n\n') // rows

    markdown_table = ""
    markdown_table += "| " * columns + "|\n"
    markdown_table += "| --- " * columns + "|\n"

    for match in matches:
        markdown_table += "|" + match.replace('\n', ' | ') + "|\n"

    return markdown_table

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
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/")
            file.save(filepath)

            # Convert DOCX to Markdown
            with open(filepath, "rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file).value

            # Extract tables from word doc
            markdown_content = word_table_to_markdown(filepath)

            # Generate Markdown table from the given text
            markdown_table = generate_markdown_table(result)

            # Replace the first instance of the Markdown table in the result
            if markdown_table in result:
                result = result.replace(markdown_table, markdown_table, 1)

            # Combine the modified Markdown content
            result += markdown_table

            # Rest of the code...

            os.remove(filepath)
            return render_template('index.html', markdown_content=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
