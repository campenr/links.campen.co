# Copyright 2016 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

import math

from flask import redirect, render_template, abort, request, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user
from flask_login import login_required

from sqlalchemy import desc

from LinkShortener import app, google
from LinkShortener.forms import LoginForm, LinkForm
from LinkShortener.models import User, Link

# TODO implement flash messages


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
                Link.add_link(submitted_link=link_form.link.data, user=current_user)
                return redirect(url_for('index'))
            except Exception as e:
                # TODO add flash message about failed attempt to add a link? Or send response JSON?
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
    me = google.get('userinfo')

    # username is the users email if logging in with google oauth2
    user = User.query.filter_by(email=me.data['email']).limit(1).first()
    if user is None:
        user = User.add_user(email=me.data['email'])

    login_user(user)
    _next = request.args.get('next')
    return redirect('/')


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/logout')
@login_required
def logout():
    """Route for logging out user."""
    logout_user()
    return redirect(url_for('index'))


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


@app.route('/api/link/delete', methods=['POST'])
@login_required
def delete_link():
    """Delete supplied link from the database."""

    try:
        link_token = request.form['link_token']
        link_data = Link.delete_link(link_token=link_token)
    except Exception as e:
        print(e)

    return redirect(url_for('index'))

@app.route('/api/links', methods=['GET'])
@login_required
def get_links():

    # get table sorting preferences from request
    r = request.args

    sort_column = r['column']
    if sort_column == 'long_link':
        sort_column = 'link_name'
    elif sort_column == 'short_link':
        sort_column = 'link_token'
    sort_desc = r['desc'] == 'true'
    page_start = int(r['start'])

    PAGE_COUNT = 10
    if page_start == 0:
        page_number = 1
    else:
        page_number = ( page_start // PAGE_COUNT ) + 1

    query = Link.query
    query = query.filter_by(owner=current_user)

    if sort_desc:
        records = query.order_by(desc(sort_column)).paginate(page=page_number, per_page=PAGE_COUNT, error_out=False)
    else:
        records = query.order_by(sort_column).paginate(page=page_number, per_page=PAGE_COUNT, error_out=False)

    link_records = records.items

    # format links
    formatted_links = []
    for link_record in link_records:

        new_link_record = dict()
        new_link_record['long_link'] = dict()

        # format record values
        new_link_record['long_link']['name'] = link_record.link_name
        new_link_record['long_link']['url'] = link_record.link_url
        new_link_record['created'] = link_record.created
        new_link_record['short_link'] = link_record.link_token

        # also need to add dummy elements for the buttons and send the link_token
        new_link_record['copy'] = link_record.link_token
        new_link_record['delete'] = link_record.link_token

        formatted_links.append(new_link_record)

    return jsonify({'data': formatted_links, 'recordsTotal': records.total, 'recordsFiltered': records.total})