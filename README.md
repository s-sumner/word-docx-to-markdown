# Readme

A flask app that takes docx files and converts them to md files.

## Deployment steps

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
pip install flask
```

```python
pip install docx2md
```

```python
pip install mammoth
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
