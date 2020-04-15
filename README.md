# links.campen.co

## Description

A Flask based web application for the generation and management of short links that redirect to longer length URLs. The 
motivation behind the creation of this app was to provide for myself a link shortening service that allowed me greater 
control; specifically the ability to delete short links that I no longer wanted.

## Usage

Users can sign in either using a username and password combination, or using Google Oauth2.
Currently the only way to create new users that can sign in using username/password combos is to
add them using the ``scripts/add_user.py`` script. 

Users can sign in to the application and view their existing short links, 
as well as create new short links and copy and delete existing short links using the web interface.

New users are automatically set as guests and have a maximum limit of 10 links.
