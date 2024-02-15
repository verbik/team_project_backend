import os
import re
import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
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
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1)]
    )
    description = models.TextField(null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    # Unique product code
    product_code = models.CharField(max_length=7, unique=True)

    # Country and region the beverage was produced in
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.ForeignKey(
        Region, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    # Alcohol content of specific beverage
    alcohol_content = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(99.99)],
    )

    # Volume of the beverage in liters
    volume = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.1), MaxValueValidator(6)],
    )
    image = models.ImageField(null=True, blank=True, upload_to=create_custom_path)

    @staticmethod
    def validate_region(region: Region, country: Country, error_to_raise):
        """Validate if region is from instances country"""
        if region:
            if region.country != country:
                raise error_to_raise(
                    "Region must be selected from the instance country."
                )

    @staticmethod
    def validate_product_code(product_code: str, error_to_raise):
        if len(product_code) < 7:
            raise error_to_raise("Product code must be of length 7.")
        pattern = re.compile("^[A-ZА-Я0-9]+$")
        if not bool(pattern.match(product_code)):
            raise error_to_raise(
                "Product code must contain only uppercase letters and numbers."
            )

    class Meta:
        abstract = True

    def clean(self):
        Beverage.validate_region(self.region, self.country, ValidationError)
        Beverage.validate_product_code(self.product_code, ValidationError)

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
        blank=True,
        null=True,
        validators=[MinValueValidator(1920), MaxValueValidator(datetime.today().year)],
    )

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
