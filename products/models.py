from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    country_of_origin = models.CharField(max_length=255)
    website = models.URLField()
