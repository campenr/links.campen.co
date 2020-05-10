import string
import random
import datetime
from app import db
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import desc


class BaseModel(db.Model):

    __abstract__ = True

    @classmethod
    def get_many(cls, order_by='id', descending=True, page_number=1, page_count=10):
        """
        Return a paginated list of multiple records from a table, optionally filtered.
        :param order_by: (optional; default=`id`) which column in the table to order results by
        :param descending: (optional; default=`True`) whether to return the records in descending order
        :param page_number: which page of the results to return
        :param page_count: number of results to return per page
        :type order_by: str
        :type descending: bool
        :type page_number: int
        :type page_count: int
        :return: paginated query results
        .. note:: the descending argument for get_many refers to the way the data is displayed when returned, which is
            the inverse of how the data is ordered in the database. This is because the data in the SQL database is
            ordered oldest to newest, i.e. ascending, by default.
        """

        # get base query
        query_ = cls.query

        # invert the descending argument due to the reverse order that data is ordered in the db
        descending = not descending

        if descending:
            return query_.order_by(desc(order_by)).paginate(page_number, page_count, False)
        else:
            return query_.order_by(order_by).paginate(page_number, page_count, False)


class User(BaseModel):
    """User table object representation.

    Columns
    -------
    id
        Unique auto incrementing identifier.
    username
        Unique username used to login.
    password_hash
        Hash of users password.
    permissions
        User's permission level. Permission affects ability to edit all links, and to view some links.

    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    role = db.Column(db.String(32))
    links = db.relationship('Link', backref='owner', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def add_user(cls, username=None, email=None, password=None, api=False, role='user'):
        """Add a new user to the User table and return the id of the user, else None."""

        user = User()

        user.username = username
        user.email = email
        if password is not None:
            user.password_hash = cls.hash_password(password)
        user.role = role

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def delete_user(cls, username):
        # TODO implement
        pass

    @classmethod
    def change_password(cls, username):
        # TODO implement
        pass

    @staticmethod
    def hash_password(password):
        """Return hash of submitted password."""
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        """Return whether submitted password matches stored hash."""
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        if self.username is not None:
            return '<User %r>' % self.username
        if self.email is not None:
            return '<User %r>' % self.email


class Link(BaseModel):
    """Link table object representation.

    Columns
    -------
    id
        Unique auto incrementing identifier.
    long_link
        Original URL link that has been shortened.
    short_link
        Shortened URL link.
    owner_id
        ID of user that created the link
    private
        Whether only logged in users can view a link.


    Classmethods for the Link model that actions on the database will return an object
    as a dictionary or None if no there is no result to be found. The routes in views.py
    handle what to do if a result or none is returned.
    """

    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    link_name = db.Column(db.String(240))
    link_url = db.Column(db.Text)
    link_token = db.Column(db.String(32))
    created = db.Column(db.DateTime)
    private = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def get_id(self):
        return str(self.id)

    @classmethod
    def retrieve_link(cls, link_token):
        """Return a link object as a dictionary for a valid link token, else None."""

        # Result is none if link_token not in the database.
        result = cls.query.filter_by(link_token=link_token).first()

        if result is not None:
            formatted_result = vars(result)
            return formatted_result
        else:
            return None

    @classmethod
    def retrieve_links(cls, owner=None):
        """Return a list of link objects as dictionaries, optionally filtered by owner, else None."""

        # # TODO implement pagination
        if owner is None:
            result = cls.query().order_by(desc(Link.created)).all()
        else:
            result = cls.query.filter_by(owner=owner).order_by(desc(Link.created)).all()

        # An empty list is returned from the above queries if no matching results exist.
        if result:
            formatted_results = [vars(rec) for rec in result]
            return formatted_results
        else:
            return None

    @classmethod
    def add_link(cls, submitted_link, user):#, private):
        """Add a new link to the database and return the link object, else None."""

        link = cls()

        link.link_name = cls.format_link_name(submitted_link)
        link.link_url = cls.format_link_url(submitted_link)
        link.link_token = cls.make_link_token()

        link.owner = user
        # link.private = private
        link.created = datetime.datetime.now()

        db.session.add(link)
        db.session.commit()

        link_data = Link.retrieve_link(link_token=link.link_token)

        return link_data

    @classmethod
    def delete_link(cls, link_token):
        """Delete a link record from the database and return the deleted record, else None."""

        # First fetch the link record so we can return this to the view, then delete the record.
        link_data = Link.retrieve_link(link_token=link_token)
        cls.query.filter_by(link_token=link_token).delete()
        db.session.commit()

        return link_data

    @staticmethod
    # TODO change this to a jinja filter?
    def format_link_url(url):
        """Format submitted long link URL."""

        # TODO figure out a better way to do this?
        # TODO Using // no good if served behind https but target url doesn't support it.
        if not ('https://' in url or 'http://' in url or '//' in url):
            url = 'http://' + url

        return url

    @staticmethod
    def make_link_token():
        """Create a new unique link token."""

        while True:
            link_token = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                                 for _ in range(6))
            if Link.query.filter_by(link_token=link_token).first() is None:
                return link_token

    @staticmethod
    # TODO change this to a jinja filter?
    def format_link_name(link):
        """Format the name of the long link for cleaner output."""

        common_names = {'youtube.com/watch?': 'youtube.com',
                        'google.com/search?': 'google.com/search'}

        # TODO regex instead for a more robust string matching?
        for key, value in common_names.items():
            if key in link:
                link = value

        # TODO dont truncate stored name, let the client decide how to truncate names instead.
        if len(link) > 35:
            link = link[:35] + ' ...'

        return link

    @staticmethod
    def format_date(created):
        """Custom jinja filter for formatting when a short link was created."""

        month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                      11: 'Nov', 12: 'Dec'}

        seconds_ = (datetime.datetime.now() - created).total_seconds()
        now_ = datetime.datetime.now()

        if seconds_ < 60:
            return '%i seconds ago' % seconds_

        elif seconds_ < 3600:
            return '%i minutes ago' % (seconds_/60)

        elif (created.day == now_.day) and \
             (created.month == now_.month) and \
             (created.year == now_.year):
            return '%i hours ago' % (seconds_/3600)

        elif (created.day == (now_ - datetime.timedelta(days=1)).day) and \
             (seconds_ < 172800):
            return 'Yesterday'

        elif now_.year == created.year:
            return '%s %s' % (month_dict[created.month], created.day)

        else:
            return '%s %s, %s' % (month_dict[created.month], created.day, created.year)

    # TODO: implement limit on number of links for guest users, unlimited to normal users and admins
