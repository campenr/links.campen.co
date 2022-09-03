from django.db import models


class Link(models.Model):

    name = models.CharField(max_length=255)
    url = models.URLField()
    token = models.CharField(max_length=32)

    created = models.DateTimeField()
    modified = models.DateTimeField()
