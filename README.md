

# JumbocodeAnimalAid

Built with [Python][0] using the [Django Web Framework][1].


## Installation

### Quick start

To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ python3 -m venv AnimalAidEnv`
    2. `$ . AnimalAidEnv/bin/activate`

Install all dependencies:

    python3 -m pip install -r requirements.txt

Run migrations:

    cd src
    python3 manage.py makemigrations core
    python3 manage.py migrate core
    
Run Server and view webpage:

    python3 manage.py runserver
 Then just open up a browser and go to the url printed by the runserver!

### Detailed instructions

Take a look at the docs for more information.


## Fixing SQLite Database
Just delete the database and then rerun makemigrations and migrate (you will lose all your data)

## Fixing Postgres Database
Access the database, drop all the tables, recreate a Schema and give the admin user access:
    
    psql animalaid <-- Open up the psql terminal
    
    // In that terminal run the following:
    
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO public;
    \q
    

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
