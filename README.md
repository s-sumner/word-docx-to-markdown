# Readme

A flask app that takes docx files and converts them to markdown. AI-assisted code development. 

There are steps to [deploy locally](#local-deployment-steps) and [deploy to Azure App Service](#deploy-to-azure-app-service)

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

## Deploy to Azure App Service
1. Create a web app in Azure App Service. Use Python 3.12 runtime. Start with a Free App Service Plan.
2. Connect GitHub organization to the web app in Azure App Service. With a Free App Service Plan, you have to connect GitHub to the web app after the deployment. In the Azure Portal, go to "Deployment Center" on the left and select the right source control, organization, repository, and branch.
3. Select Add Workflow, and Azure App Service automatically creates a workflow yaml file and deploys with GitHub Actions.
4. In GitHub, track the build and deployment progress using the "Actions" tab at the top of the repo.
5. In the portal, find your "Default domain" and click the link.
