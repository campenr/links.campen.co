# Copyright 2016 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

import math

from flask import flash, redirect, render_template, abort, request, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user
from flask_login import login_required

from sqlalchemy import desc

from LinkShortener import app, db, google
from LinkShortener.forms import LoginForm, LinkForm
from LinkShortener.models import User, Link

# TODO implement flash messages
# TODO: add admin interface

@app.login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).limit(1).first()
    return user

# TODO implement better logging of activity


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Route for displaying index page."""

    if current_user.is_authenticated:

        link_form = LinkForm()
        if request.method == 'POST' and link_form.validate_on_submit():

            try:

                # if the current user is only a guest they can't exceed more than 10 links
                if current_user.role == 'guest':
                    links_number = Link.query.filter_by(owner=current_user).count()
                    if links_number >= 10:
                        flash('Number of links exceeded. Please delete a link before creating a new one.', 'danger')
                        return redirect(url_for('index'))

                Link.add_link(submitted_link=link_form.link.data, user=current_user)
                return redirect(url_for('index'))
            except Exception as e:
                # TODO add flash message about failed attempt to add a link? Or send response JSON?
                flash('Failed to add link. Please refresh and try again.', 'danger')
                print(e)

        links_data = Link.retrieve_links(owner=current_user)
        return render_template('index.html', data=links_data, link_form=link_form)

    # return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for displaying login page and redirects to index or next page if supplied in request."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).limit(1).first()
        if user is not None:
            if user.verify_password(form.password.data):
                login_user(user)
                _next = request.args.get('next')
                return redirect(_next or '/')
        # TODO handle incorrect password better, perhaps during form validation.

    return render_template('login.html', title='Log In', form=form)


@app.route('/login/google', methods=['GET', 'POST'])
def google_login():
    """Route for logging in user with Google OAuth2"""

    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')

    # use the users email address as the unique identifier if logging in with google oauth2
    user = User.query.filter_by(email=user_info.data['email']).limit(1).first()
    if user is None:
        # if first time logging in create a new user of account type guest
        user = User(email=user_info.data['email'], role='guest')
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect('/')


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/logout')
@login_required
def logout():
    """Route for logging out user."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/<link_token>', methods=['GET'])
@app.route('/link/<link_token>', methods=['GET'])
def view_link(link_token):
    """Default route for viewing a link."""

    link_data = Link.retrieve_link(link_token)
    if link_data is None:
        abort(404)
    else:
        if link_data['private']:
            return redirect('/link/private/' + link_token)
        else:
            return redirect(link_data['link_url'], code=307)


# @app.route('/link/private/<link_token>', methods=['GET'])
# @login_required
# def view_private_link(link_token):
#     """Route for viewing a private link.
#
#     If a request is made for a private link, the request is redirected to this route that requires
#     that the client by logged in in order to view the link.
#     """
#
#     # TODO refactor to remove redundancy between this route and the view_link route.
#
#     link_data = Link.retrieve_link(link_token=link_token)
#     if link_data is None:
#         abort(404)
#     else:
#         # Prevent caching of redirect with 307 status code
#         return redirect(link_data['link_url'], code=307)
#
#
# @app.route('/link/add', methods=['POST'])
# @login_required
# def add_link():
#     """Add supplied link to the database."""
#
#     private = False
#
#     try:
#         request_data = request.form.to_dict()
#
#         print('request data: ', request_data)
#
#         submitted_link = request_data['link']
#         if 'private' in request_data.keys():
#             private = True
#         link_data = Link.add_link(submitted_link=submitted_link, user=current_user, private=private)
#     except Exception as e:
#         print(e)
#
#     return redirect(url_for('index'))
