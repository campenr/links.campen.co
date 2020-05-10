
from .base import *


ENVIRONMENT = 'development'

DEBUG = True

ALLOWED_HOSTS = [
    '*',
]

try:
    from .local import *
except ImportError:
    pass
