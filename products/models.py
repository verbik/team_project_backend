import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.CharField(max_length=255)

    def __str__(self):
        return self.region


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    country_of_origin = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=True, null=True
    )
    website = models.URLField()

    def __str__(self):
        return self.name


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
    image = models.ImageField(null=True, blank=True, upload_to=create_custom_path)

    class Meta:
        abstract = True

    def clean(self):
        # Ensure that content_object is an instance of Beverage or its subclasses
        if self.region:
            if self.region.country != self.country:
                raise ValidationError(
                    {
                        "region": "The wine region must be selected from the chosen country."
                    },
                    code="invalid_region",
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class GrapeVariety(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "grape varieties"

    def __str__(self):
        return self.name


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
    grape_variety = models.ManyToManyField(GrapeVariety, related_name="grape_variety")

    @property
    def short_description(self):
        return (
            f"Wine {self.name}, "
            f"{self.manufacturer.name}, "
            f"{self.get_color_display()} "
            f"{self.get_sugar_content_display()} "
            f"{self.volume} l"
        )

    def __str__(self):
        return self.short_description
