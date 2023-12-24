# Readme

A flask app that takes docx files and converts them to markdown. AI-assisted code development. 

## Local deployment steps

Create virtual environment

```python
python -m venv venv
```

Activate virtual environment

```python
.\venv\Scripts\Activate 
```

Install dependencies if needed

```python
# update pip
python.exe -m pip install --upgrade pip
```

```python
pip install flask
pip install docx2md
pip install mammoth
pip install flask python-docx mammoth
pip install html2text
pip install python-docx tabulate
```

Updated requirements txt file

```python
pip freeze > requirements.txt
```

Build and run app

```python
python app.py
```

In browser, paste the following url

```python
http://localhost:5000/
```

Stop web app

`Ctrl` + `C`
