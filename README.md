# About
This is a Django-based solution. It uses Celery for task scheduling and Redis as its broker. The solution includes unit tests to make sure that objects can be created and inserted in the database.

Each schema is a different django app in the project.

Django oficially supports the most relevant SQL databases by default and the models are almost database independent. However, I went for MongoDB because the data was given me in files and it was extremely easy for me to import it into the database. If I had no time constraints I would have chosen PostgreSQL or MariaDB.

## A quick glance
If you want to take a quick look at the relevant files, I sugges you check the disembursements/models.py, disembursements/tests.py, and the other models.py files in the different folders.

# Instalation
Follow the steps below if you want to install the solution
## Dependencies:
A local Redis server must be running locally. Assuming you have Docker installed, if you want to run it as Docker container run:
```
docker run -d -p 6379:6379 redis
```
MongoDB must be running in the host system. If you want to run it on Docker execute this:
```
docker run -d -p 27017:27017 --name example-mongo mongo:latest
```

## Linux packages (assumming you are using Ubuntu)
Install these packages beforehand if they are not installed on your machine. 
```
sudo apt udpate
sudo apt install postgresql postgresql-contrib
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-pip
sudo apt install python3.8-venv
```
## Project installation
Clone the repository and create a virtual environment inside the git folder.
```
cd /path/to/git/project/
python3 -m venv venv
```
Activate environment and install project dependencies into project dependencies.
```
source venv/bin/activate
```

After that install the project dependencies. If the following command runs into issues use the requirementsTest.txt file instead.
```
cd project/
pip install -r requirements.txt
```
## Prepare the project DB and admin user
Make sure that the project/settings.py config matches the database name and user credentials. 
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Congrats! If everything went well you can now run tests and start playing with the solution.

# Run tests and start the webserver
Assuming that the virtual environment is still activated run:
```
python manage.py test
python manage.py runserver
```

You can now visit the URL localhost:8000/admin and log in using the superuser credentials you just used.

The API URLS are:
http://127.0.0.1:8000/disembursments/
http://127.0.0.1:8000/disembursments/merchant/<merchant_id>

# Run Celery
Open a new terminal and go to the project folder and run the commands below. This start running the periodic disembursement tasks.
```
source venv/bin/activate
celery -A project beat -l INFO
```
# Bypass the periodic task and create disembursements right away
I understand you might not want to wait til Monday, so here's how you can generate disembursments manually. Please note that the DB should at least contain one merchant with one completed order.
```
source venv/bin/activate
cd project
python manage.py shell
```
This will start a python shell inside the solution environment, allowing you access to every single module and function. Now run each line of code seperately:
```
from disembursements.models import DisembursementController
DisembursementController.disembursements_generator()
```
Now if the webserver is running you can check the results in the API described in a previous section.

# How does the solution work?
As you can see, the solution is organised in different folders (merchant, orders, shoppers and disembursements). Each one of them is a Django app, allowing us to define their API, Models and Tests independently. This approach also helps project maintenance.

If you want to check how the API is implemented go to disembursements->views.py and urls.py. The disembursements app is the main one. It has a tasks.py file where the repeatable Celery tasks can be defined.

The project folder holds the settingsm brings the different URLs (APIs) together and includes a tasks file where the weekly task is defined.

The manage.py file sitting on the root folder is a standard Django file allowing us to create migrations, run a simple development web server and running tests, among other features.

# Known bugs or issues:
The disembursements_generator function in the disembursements/models.py file should query for orders that have not been disembursed. Actually there is a new field for that in the orders model. I lacked the time to change the query.

The given datetimes in the files are not self aware. Even thought making the dates aware of the timezone is straightforward, it has been postponed due to the time limitation.

Sometimes type casting is required due to how the data is stored and originally given in the files. Could be similarly addressed like the issue described in the previous paragraph because it has the same root issue.

MongoDB can add trailing "_id" to field names that already end with "_id". E.g. merchant_id is converted to merchant_id_id. MongoDB should not be used in development or in production for a solution of this nature, it was just used in this solution to speed things up to avoid spending too much time setting up the databases and some existing data.