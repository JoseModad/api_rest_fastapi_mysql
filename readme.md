Small crud practice in fastapi with use of sql database.

You must have a sql database installed(phpmyadmin, xampp, etc).

Create a new database without tables since these will be created from the app.


Create virtual environment with:

    - python -m venv env


activate virtual environment(linux):

    - source env/bin/activate 


Install dependencies with:

    - pip install -r requirements.txt


to run the server(app):

    - uvicorn main:app --reload


Copy in your browser the following address to interact with the crud:

    - http://localhost:8000/docs


