from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("listing", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.listing.title} — {self.rating} by {self.user.username}"
