# LinkShortener 0.4.0

## Updates

* Removed the private link functionality.
* Switched styling to bootstrap3
* Switched table to jquery's DataTables for sorting functionality

------

## Description

A Flask based web application for the generation and management of short links that redirect to longer length URLs. The 
motivation behind the creation of this app was to provide for myself a link shortening service that allowed me greater 
control; specifically the ability to delete short links that I no longer wanted.

## Usage

Users can sign in either using a username and password combination, or using Google Oauth2.
Currently the only way to create new users that can sign in using username/password combos is to
add them using the ``scripts/add_user.py`` script (run 
``add_user.py --help`` for more information). 

Users can sign in to the application and view their existing short links, 
as well as create new short links and copy and delete existing short links using the web interface.

New users are automatically set as guests and have a maximum limit of 10 links.

## Deployment

Use ``pip install -r requirements.txt`` to install the required package dependencies. It is recommended
that this be deployed in a virtual environment. This has been tested with Python 3.4+.

The application uses an SQL based database to store the user and link information ([PostgreSQL](https://www.postgresql.org/)
 recommended.)

Before the first use create a valid configuration file using the instructions provided by the example file in ``config/``.
Specifically, provide a secret key and a valid URI to an SQL database, and google Oauth2 config
 options for the google Oauth2 sign in.

During development you can run the application using ``run.py`` directly, but for deployment I recommend using 
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) or equivalent to serve the application behind a web server like
[nginx](https://www.nginx.com/). There are many good examples out there for how to serve Flask applications with uWSGI
and nginx.

## TODO

* Provide basic stat tracking of how many times a link has been clicked
* Better format the table for smaller screens when viewed vertically
* Create sign up functionality so users can create new sign in credentials
* Add admin interface for easier administration
