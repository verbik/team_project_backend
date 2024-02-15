import django_filters
from products.models import Wine


class WineFilter(django_filters.FilterSet):
    class Meta:
        model = Wine
        fields = {
            "manufacturer": ["exact"],
            "country": ["exact"],
            "region": ["exact"],
            "price": ["exact", "gte", "lte"],
            "color": ["exact"],
            "sugar_content": ["exact"],
            "grape_variety": ["exact"],
        }
