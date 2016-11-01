# LinkShortener 0.2.0

## Description

A Flask based web application for the generation and management of short links that redirect to longer length URLs. The 
motivation behind the creation of this app was to provide for myself a link shortening service that allowed me greater 
control; specifically the ability to delete short links that I no longer wanted.

## Usage

This application supports multiple users that can be added using the ``scripts/add_user.py`` script (run 
``add_user.py --help`` for more information). Each user can log into the application and view their existing short links, 
as well as create new short links using the web interface. Short links, when created, can be set as private which 
prevents users that are not logged into the application from viewing them.

## Deployment

Use ``pip install -r requirements.txt`` to install the required dependencies.

Before use create a valid configuration file using the instructions provided by the example file in ``config/``.
Specifically, provide a secret key and a valid URI to an SQL database. During development you can run the application 
using ``run.py`` directly, but for production deployment I recommend using a service such as 
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) to serve the application.

Database migrations, if needed, can be performed using ``scripts/manage.py``. Run 
``python manage.py db --help`` for more information.