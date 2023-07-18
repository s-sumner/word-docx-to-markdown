

import logging
import re
import os
import io
import lxml.etree  # Import lxml.etree module
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

        # Generate a unique placeholder for each table
        placeholder = f'[TABLE_{i}]'

        # Create a custom XML element with the placeholder text
        custom_element = lxml.etree.Element('placeholder')
        custom_element.text = placeholder

        # Replace the table element with the custom element
        table._element.getparent().replace(table._element, custom_element)

        # Append the placeholder and table data to the markdown content list
        markdown_content.append(placeholder)
        markdown_content.append(tabulate(data, tablefmt="pipe", headers="firstrow"))

    return markdown_content


def replace_images_with_placeholder(content, images):
    img_regex = r'!\[.*?\]\((.*?)\)'
    placeholder = '[ADD IMAGE HERE]'
    result = re.sub(img_regex, lambda match: placeholder if match.group(1) in images else match.group(0), content)

    # Remove characters and whitespace between "(data:image" and ")"
    result = re.sub(r'\(data:image.*?\)', '', result)

    return result

def replace_urls(content):
    # Change URLs starting with "https://learn.microsoft.com/azure/" to "/azure/..."
    result = re.sub(r'https://learn.microsoft.com/azure/(.+)', r'/azure/\1', content)

    # Remove "en-us/" from URLs
    result = result.replace("/en-us/", "/")

    return result

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

            # Extract tables from word doc and get the list of placeholders
            markdown_content = word_table_to_markdown(filepath)
            table_placeholders = markdown_content[::2]  # Get the placeholders only

            # Combine the modified Markdown content
            result = result + "\n\n".join(markdown_content[1::2])

            # Replace the first identical match of table text with the corresponding table
            for placeholder, table in zip(table_placeholders, markdown_content[1::2]):
                if placeholder in result:
                    result = result.replace(placeholder, table, 1)
                    break

            ## end table 

            # Remove trailing whitespaces from each line
            result = '\n'.join(line.rstrip() for line in result.split('\n'))

            # Remove escape character from markdown
            result = result.replace("\\.", ".").replace("\\)", ")").replace("\\-", "-").replace("\\(", "(").replace("\\]", "]").replace("\\[", "[").replace("\\#", "#")

            # Remove "https://learn.microsoft.com/en-us" from links and keep the remaining URL intact
            result = re.sub(r'https://learn.microsoft.com/[a-z]+-[a-z]+(/azure)?', '/azure', result)
            
            # Replace URLs in the Markdown content
            result = replace_urls(result)
            
            # Remove double spaces and replace them with a single space
            result = result.replace('  ', ' ')

            # Replace double underscore with double asterisks
            result = re.sub(r'__(.*?)__', r'**\1**', result)
            
            # Replace double underscore with double asterisks for bold phrases
            result = re.sub(r' \*\*(.*?)', r'** \1', result)

            # Replace "-** " with "- **"
            result = re.sub(r'-\*\*\s(.+)', r'- **\1', result)

            # Get the list of image URLs in the markdown
            images = re.findall(r'!\[.*?\]\((.*?)\)', result)

            # Replace all instances of "\\`" with "`"
            result = result.replace("\\`", "`")

            # Remove whitespace between any character and "]"
            result = re.sub(r'(\S)\s+\]', r'\1]', result)

            # remove long sequences of ---
            result = re.sub(r'(-{4,})', '---', result)

            # Replace images with placeholder (excluding autogenerated images)
            result = replace_images_with_placeholder(result, images)

            os.remove(filepath)
            return render_template('index.html', markdown_content=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
