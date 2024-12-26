# Parkify Backend Project


**To get started with the Project, follow these simple steps:**

    1. Navigate to the project directory and create a virtual environment by running:
        - python -m venv venv

    2. Activate the virtual environment by running the command:
        - source venv/bin/activate
        OR - .\venv\Scripts\activate

    3. Install the required dependencies by running the command:
        - pip install -r requirements.txt

    4. Next, apply the database migrations by running:
        - python manage.py migrate

    5. Create a superuser account by running:
        - python manage.py createsuperuser

    7. To load data from fixtures, run the command:
        - python manage.py loaddata user_role

    8. Load the static files
        - python manage.py collectstatic

    9. Finally, start the Django server by running:
        - python manage.py runserver