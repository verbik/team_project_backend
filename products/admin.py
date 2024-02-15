from django.contrib import admin

from products.models import Wine, Country, Region, GrapeVariety, Manufacturer


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(GrapeVariety)
class GrapeVarietyAdmin(admin.ModelAdmin):
    pass


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    pass
