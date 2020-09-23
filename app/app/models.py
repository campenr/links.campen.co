import random

import string
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



""""

We could just have USERNAME_FIELD = email and EMAIL_FIELD = email.

So users have to log in with an email and password, or OAuth which is tied to an email address.


"""


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', self.model.RoleType.GUEST)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.RoleType.MEMBER)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != self.model.RoleType.MEMBER:
            raise ValueError('Superuser must have role=RoleType.MEMBER.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    email = models.EmailField(
        _('email address'),
        blank=True,
        # as we're using the email field as our USERNAME field we need to set these next two
        unique=True,
        error_messages = {
            'unique': _("A user with that username already exists."),
        },
    )
    # we need to unset this as otherwise it will be inherited from the base class.
    username = None

    class RoleType:
        GUEST = 0
        MEMBER = 1
        ROLE_CHOICES = [
            (GUEST, 'Guest'),
            (MEMBER, 'Member'),
        ]
    role = models.IntegerField(
        _('role'),
        choices=RoleType.ROLE_CHOICES,
        default=RoleType.GUEST,
        help_text=_('Role type enum.')
    )

    objects = UserManager()

    # for our purposes the email field is the username field, i.e. it's unique and users use it to log in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_guest(self):
        return self.role == self.RoleType.GUEST

    @property
    def is_member(self):
        return self.role == self.RoleType.MEMBER


class Link(models.Model):

    url = models.TextField(_('url'), help_text=_('The original URL.'))
    name = models.CharField(_('name'), max_length=256, help_text=_('User friendly URL name.'))
    token = models.CharField(
        _('token'),
        unique=True,
        max_length=32,
        help_text=_('The unique token identifier for the URL.')
    )
    created = models.DateTimeField(_('created'), default=timezone.now, help_text=_('When the link was created.'))
    private = models.BooleanField(
        _('private'),
        default=False,
        help_text=_('Whether the link is only viewable by the owner')
    )
    owner = models.ForeignKey(
        get_user_model(),
        related_name='links',
        on_delete=models.CASCADE,
        help_text=_('The owner of this link.'),
    )

    def save(self, *args, **kwargs):
        # TODO: add guest limit of 10 links logic.
        self.url = self.format_link_url(self.url)  # TODO: switch to using URL field
        self.name = self.format_link_name(self.url)
        self.token = self.make_link_token()
        super().save(*args, **kwargs)

    @staticmethod
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
            token = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                                 for _ in range(6))
            if Link.objects.filter(token=token).first() is None:
                return token

    @staticmethod
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
