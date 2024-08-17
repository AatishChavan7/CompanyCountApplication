# CompanyCountApplication
The application will allow users to login and filter the database table using a form. Once the user submits the form, display the count of records based on the applied filters.

## Catalyst Count
Catalyst Count is a Django web application designed for managing and querying company data. The application includes user authentication, file upload functionality, and a query builder to filter and search company records.

### Table of Contents
Features Technologies Installation Configuration Usage Importing Data

### Features
User Authentication: Register, login, and logout functionality with a custom user model. File Upload: Upload CSV files containing company data, which are processed asynchronously using Celery. Query Builder: Filter company records based on various criteria like name, domain, year founded, etc. Dashboard: A user dashboard that displays options and messages after login.

### Technologies
Django - Web framework used for the application. Django REST Framework - For building the API. Celery - Asynchronous task queue for processing CSV files. Redis - Message broker for Celery. PostgreSQL - Database management system. HTML/CSS - Frontend technologies used for the UI.

### Installation
To set up the project, follow these steps:

1] Clone the repository: git clone https://github.com/AatishChavan7/CompanyCountApplication.git cd catalyst_count

2] Create a virtual environment and activate it: python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate

3] Install the required packages: pip install -r requirements.txt

4] Apply migrations to set up the database: python manage.py migrate

5] Create a superuser (optional, for admin access): python manage.py createsuperuser

6] Run the development server: python manage.py runserver

7] Start Celery worker (in a new terminal window): celery -A catalyst_count worker --loglevel=info

### Configuration
Database Configuration:

Update the DATABASES setting in settings.py with your PostgreSQL credentials:

DATABASES = { 'default': { 'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': 'company_db', 'USER': 'postgres', 'PASSWORD': 'yourpassword', 'HOST': 'localhost', 'PORT': '5432', } }

### Celery Configuration:
CELERY_BROKER_URL = 'redis://localhost:6379/0' CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

### Usage
Base View: http://127.0.0.1:8000/ - Displays the base page. Login: http://127.0.0.1:8000/login/ - Allows users to log in. Register: http://127.0.0.1:8000/register/ - Allows new users to register. Upload: http://127.0.0.1:8000/upload/ - Upload CSV files. Query: http://127.0.0.1:8000/query/ - Query company records with filters. Dashboard: http://127.0.0.1:8000/dashboard/ - Displays the user dashboard after login.

### Importing Data
python manage.py import_companies path/to/your/file.csv
