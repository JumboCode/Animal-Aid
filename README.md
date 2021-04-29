

# Jumbocode - Animal Aid Project

Built with [Python][0] using the [Django Web Framework][1].

## Our Team
### Project Manager
Ben London
### Technical Lead
Viet Nguyen
### Designer
Anju Ishizaki
### Developers
Amelia Cook, Ann Marie Burke, Catherine Ding, Emily Nadler, Janny Huang, Kunal Valia, Lawrence Xu, Sejal Dua 

---

## Installation

### Quick start

1. To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ python3 -m venv AnimalAidEnv`
    2. `$ . AnimalAidEnv/bin/activate`

Ensure that you define all required environment variables for the database, AWS, and Email Server

2. Install all dependencies:

    `python3 -m pip install -r requirements.txt`

3. Run migrations:

    `python3 manage.py makemigrations`
    
    `python3 manage.py migrate core`

4. Collect static files:

    `python3 manage.py collectstatic`

5. Run Server and view webpage:

    `python3 manage.py runserver`
    
 Then just open up a browser and go to the url printed by the runserver!

### Detailed instructions

Take a look at the docs for more information.
    

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
