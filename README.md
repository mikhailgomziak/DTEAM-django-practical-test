# DTEAM-django-practical-test

This project uses:

- [**pyenv**](https://github.com/pyenv/pyenv): to manage multiple Python versions
- [**pyenv-virtualenv**](https://github.com/pyenv/pyenv-virtualenv): for Python virtual environments
- [**Poetry**](https://python-poetry.org/): for dependency and packaging management

---

## 📋 Prerequisites

Make sure you have the following installed:

- Git
- build tools (`build-essential`, `make`, `gcc`, etc.)
- `pyenv` and `pyenv-virtualenv`
- Python 3.12.9 (or the required version)
- Poetry

---

### Install pyenv and pyenv-virtualenv

#### Using Homebrew (macOS):
```bash
brew install pyenv pyenv-virtualenv
```

#### Add pyenv to your shell:
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

#### Install python 3.12.9 and activate it:
```bash
pyenv install 3.12.9
pyenv local 3.12.9
pyenv shell 3.12.9
```

#### Create virtualenv and use it:
```bash
pyenv virtualenv 3.12.9 dteam-pt
pyenv activate dteam-pt
```

### Install poetry and install dependencies:
#### Using Homebrew (macOS):
```bash
brew install poetry
poetry install
```

### 📥 Make migrations and load initial data

To load the sample CV data into your database:

Apply migrations:
```bash
python manage.py migrate
```

Load initial data:
```bash
python manage.py loaddata sample_cv.json
```

### 🧪 Running Tests

To run unit tests for the CV list and detail views:

```bash
python manage.py test
```

## Docker

Set up environment variables:

Create a .env file in the root of the project directory. Ensure the necessary environment variables are defined.

Example .env:
```bash
POSTGRES_DB=mydb # The name of your database.
POSTGRES_USER=myuser # The PostgreSQL username.
POSTGRES_PASSWORD=mypassword # The PostgreSQL password.
POSTGRES_HOST=localhost # change to localhost if you run project locally and db if via docker
POSTGRES_PORT=5432 # The port for the db.
```

Use command:
```bash
docker-compose up --build
```

## SMTP setup
I used gmail smtp server to send emails.

To send email with a CV pdf you need to set the next info in .env:

```bash
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your app password - 16 digits without space
```

I left those in .env.example

# Instructions
# Version Control System 
1. Create a public GitHub repository for this practical test, for example: DTEAM-django- 
practical-test. 
2. Put the text of this test (all instructions) into README.md. 
3. For each task, create a separate branch (for example, tasks/task-1, tasks/task-2, etc.). 
4. When you finish each task, merge that branch back into main but do not delete the original 
task branch. 

# Python Virtual Environment 
1. Use pyenv to manage the Python version. Create a file named .python-version in your 
repository to store the exact Python version. 
2. Use Poetry to manage and store project dependencies. This will create a pyproject.toml file. 
3. Update your README.md with clear instructions on how to set up and use pyenv and Poetry for 
this project. 

# Tasks 
## Task 1: Django Fundamentals 
1. Create a New Django Project 
* Name it something like CVProject. 
* Use the Python version set up in Task 2 and the latest stable Django release. 
* Use SQLite as your database for now. 
2. Create an App and Model 
* Create a Django app (for example, main). 
* Define a CV model with fields like firstname, lastname, skills, projects, bio, and 
contacts. 
* Organize the data in a way that feels efficient and logical. 
3. Load Initial Data with Fixtures 
* Create a fixture that contains at least one sample CV instance. 
* Include instructions in README.md on how to load the fixture. 
4. List Page View and Template 
* Implement a view for the main page (e.g., /) to display a list of CV entries. 
* Use any CSS library to style them nicely. 
* Ensure the data is retrieved from the database efficiently. 
5. Detail Page View 
* Implement a detail view (e.g., /cv/<id>/) to show all data for a single CV. 
* Style it nicely and ensure efficient data retrieval. 
6. Tests 
Add basic tests for the list and detail views. 
Update README.md with instructions on how to run these tests. 

## Task 2: PDF Generation Basics 
1. Choose and install any HTML-to-PDF generating library or tool. 
2. Add a 'Download PDF' button on the CV detail page that allows users to download the CV as a 
PDF. 

## Task 3: REST API Fundamentals 
1. Install Django REST Framework (DRF). 
2. Create CRUD endpoints for the CV model (create, retrieve, update, delete). 
3. Add tests to verify that each CRUD action works correctly. 

## Task 4: Middleware & Request Logging 
1. Create a Request Log Model 
* You can put this in the existing app or a new app (e.g., audit). 
* Include fields such as timestamp, HTTP method, path, and optionally other details like 
query string, remote IP, or logged-in user. 
2. Implement Logging Middleware 
* Write a custom Django middleware class that intercepts each incoming request. 
* Create a RequestLog record in the database with the relevant request data.  
* Keep it efficient. 
3. Recent Requests Page 
* Create a view (e.g., /logs/) showing the 10 most recent logged requests, sorted by 
timestamp descending. 
* Include a template that loops through these entries and displays their timestamp, method, 
and path. 
4. Test Logging 
* Ensure your tests verify the logging functionality. 

## Task 5: Template Context Processors 
1. Create settings_context2. Settings Page 
* Create a view (e.g., /settings/) that displays DEBUG and other settings values made 
available by the context processor. 

## Task 6: Docker Basics 
1. Use Docker Compose to containerize your project. 
2. Switch the database from SQLite to PostgreSQL in Docker Compose. 
3. Store all necessary environment variables (database credentials, etc.) in a .env file. 

## Task 7: Celery Basics 
1. Install and configure Celery, using Redis or RabbitMQ as the broker. 
2. Add a Celery worker to your Docker Compose configuration. 
3. On the CV detail page, add an email input field and a 'Send PDF to Email' button to trigger a 
Celery task that emails the PDF. 

## Task 8: OpenAl Basics 
1. On the CV detail page, add a 'Translate' button and a language selector. 
2. Include these languages: Cornish, Manx, Breton, Inuktitut, Kalaallisut, Romani, Occitan, Ladino, 
Northern Sami, Upper Sorbian, Kashubian, Zazaki, Chuvash, Livonian, Tsakonian, Saramaccan, 
Bislama, 
3. Hook this up to an OpenAl translation API or any other translation mechanism you prefer. The 
idea is to translate the CV content into the selected language.

## Task 9: Deployment 
Deploy this project to DigitalOcean or any other VPS.