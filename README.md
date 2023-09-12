# Taskly - Task Management Web App

Taskly is a web application built using Django that allows users to manage their tasks efficiently.

## Features

- User registration and authentication
- Task creation, updating, and deletion
- Marking tasks as completed
- Search functionality for tasks
- Password reset and change features

## Setup Locally

To run Taskly locally on your machine, follow these steps:

### Prerequisites

- Python 3.6+
- Django (latest version)
- PostgreSQL or another database of your choice (if you prefer a different database)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/kimenyu/Taskly
   Navigate to the project directory:

bash
Copy code
cd Taskly
Create a virtual environment (recommended) and activate it:

bash
Copy code
python -m venv venv
source venv/bin/activate
Install the project dependencies:

bash
Copy code
pip install -r requirements.txt
Create a PostgreSQL database and configure the database settings in settings.py:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-database-name',
        'USER': 'your-database-user',
        'PASSWORD': 'your-database-password',
        'HOST': 'localhost',  # Change if your database is hosted elsewhere
        'PORT': '',            # Leave empty to use the default PostgreSQL port
    }
}
Apply database migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a superuser for the admin panel:

bash
Copy code
python manage.py createsuperuser
Start the development server:

bash
Copy code
python manage.py runserver
Open your web browser and go to http://localhost:8000/ to access Taskly.

To access the admin panel, go to http://localhost:8000/admin/ and log in with the superuser credentials created in step 7.

Usage
Register a new user account or log in if you already have one.
Create, update, and delete tasks from the main dashboard.
Mark tasks as completed by clicking on them.
Use the search functionality to find specific tasks.
Change your password or reset it if necessary.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Thanks to the Django community for their excellent documentation and resources.
Contact
If you have any questions or suggestions, please feel free to contact the project maintainers:

Joseph Njoroge njorogekimenyu@gmail.com
Teresa Amanwachi
Alice Kiptui

