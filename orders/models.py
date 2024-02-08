from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models


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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):  # TODO: rewrite validation
        super().save(*args, **kwargs)
        # Calculate total_price by summing item_price of every order item
        total_price = sum(item.item_price for item in self.items.all())
        self.total_price = total_price

        # Save again to update total_price
        super().save()

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):
    """Order item model"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )  # TODO: add validation

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
