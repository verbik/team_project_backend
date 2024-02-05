import os
import uuid

from django.db import models
from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=255)


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.CharField(max_length=255)


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE)
    website = models.URLField()
    #  TODO: add imagefield


def create_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads", "images", f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    )


class Beverage(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # TODO: add constraints
    description = models.TextField(null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    # Unique product code
    product_code = models.CharField(max_length=7, unique=True)  # TODO: add validation

    # Country and region the beverage was produced in
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.ForeignKey(
        Region, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    # Alcohol content of specific beverage
    alcohol_content = models.FloatField(null=True, blank=True)  # TODO: add constraints

    # Volume of the beverage in liters
    volume = models.DecimalField(
        max_digits=4, decimal_places=2
    )  # TODO: add constraints
    image = models.ImageField(null=True, upload_to=create_custom_path)

    class Meta:
        abstract = True


class Wine(Beverage):
    SUGAR_CONTENT_CHOICES = {
        "SWEET": "Sweet",
        "SEMI_SWEET": "Semi-Sweet",
        "OFF_DRY": "Off-Dry",
        "DRY": "Dry",
    }

    COLOR_CHOICES = {
        "WHITE": "White",
        "PINK": "Pink",
        "RED": "Red",
        "AMBER": "Amber",
    }

    year = models.IntegerField(
        blank=True, null=True
    )  # TODO: add validation for year + placeholder

    # Sugar content of the wine
    sugar_content = models.CharField(max_length=20, choices=SUGAR_CONTENT_CHOICES)
    color = models.CharField(max_length=5, choices=COLOR_CHOICES)
    grape_variety = models.CharField(max_length=255)
