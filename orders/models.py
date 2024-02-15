from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

from products.models import Beverage


class Order(models.Model):
    """Order model"""

    STATUS_CHOICES = {
        "P": "pending",
        "C": "completed",
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    is_paid = models.BooleanField(default=False)

    @property
    def total_price(self) -> Decimal:
        return sum(item.item_price for item in self.items.all())

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id}: user - {self.user}, date - {self.created_at.date()}"


class OrderItem(models.Model):
    """Order item model"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return f"{self.quantity} x {self.content_object}"

    @property
    def item_price(self):
        """Returns total price for order item"""
        return self.quantity * self.content_object.price

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def clean(self):
        # Ensure that content_object is an instance of Beverage or its subclasses
        if not isinstance(self.content_object, Beverage):
            raise ValidationError(
                _(
                    "Only instances of Beverage or its subclasses are allowed as content objects."
                )
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
