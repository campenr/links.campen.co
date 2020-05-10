import math

from flask import flash, redirect, render_template, abort, request, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user
from flask_login import login_required

from sqlalchemy import desc

from app import flask_app, db, oauth
from app.forms import LoginForm, LinkForm
from app.models import User, Link

# TODO implement flash messages
# TODO: add admin interface


@flask_app.login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).limit(1).first()
    return user

# TODO implement better logging of activity


@flask_app.route('/', methods=['GET', 'POST'])
@flask_app.route('/index', methods=['GET', 'POST'])
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


@flask_app.route('/privacy')
def privacy():
    """Route for displaying the website's privacy policy page."""

    return render_template('privacy.html')


@flask_app.route('/tos')
def tos():
    """Route for displaying the website's terms of service page."""

    return render_template('tos.html')


@flask_app.route('/login', methods=['GET', 'POST'])
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


@flask_app.route('/login/google', methods=['GET', 'POST'])
def google_login():
    """Route for logging in user with Google OAuth2"""
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@flask_app.route('/login/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    if token is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    user_info = oauth.google.get('userinfo')
    # use the users email address as the unique identifier if logging in with google oauth2
    email = user_info.json().get('email')
    if email is None:
        # TODO: add messaging here. for now just fail silently
        return redirect('/')

    user = User.query.filter_by(email=email).limit(1).first()
    if user is None:
        # if first time logging in create a new user of account type guest
        user = User(email=email, role='guest')
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect('/')


@flask_app.route('/logout')
@login_required
def logout():
    """Route for logging out user."""
    logout_user()
    return redirect(url_for('login'))


@flask_app.route('/<link_token>', methods=['GET'])
@flask_app.route('/link/<link_token>', methods=['GET'])
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


# @flask_app.route('/link/private/<link_token>', methods=['GET'])
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
# @flask_app.route('/link/add', methods=['POST'])
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
