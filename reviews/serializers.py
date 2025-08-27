from rest_framework import serializers
from .models import Review
from bookings.models import Booking
from django.db.models import Q
from datetime import date

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ["id", "listing", "user", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def validate(self, attrs):
        listing = attrs.get("listing") or getattr(self.instance, "listing", None)
        user = self.context["request"].user

        # 1) Один отзыв на объявление от пользователя
        exists = Review.objects.filter(listing=listing, user=user)
        if self.instance:
            exists = exists.exclude(pk=self.instance.pk)
        if exists.exists():
            raise serializers.ValidationError("Вы уже оставляли отзыв к этому объявлению.")

        # 2) Должно быть как минимум одно подтверждённое бронирование этого listing пользователем
        has_approved = Booking.objects.filter(
            listing=listing, renter=user, status="approved"
        ).exists()
        if not has_approved:
            raise serializers.ValidationError("Отзыв может оставить только пользователь с подтверждённым бронированием этого объявления.")

        # 3) (опционально) Разрешать отзыв только после окончания проживания:
        # today = date.today()
        # finished = Booking.objects.filter(
        #     listing=listing, renter=user, status="approved",
        #     end_date__lte=today
        # ).exists()
        # if not finished:
        #     raise serializers.ValidationError("Оставить отзыв можно после окончания бронирования.")

        return attrs
