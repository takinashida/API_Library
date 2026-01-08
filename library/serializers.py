from rest_framework import serializers
from .models import Author
from .models import Book
from django.utils.timezone import now
from .models import Loan
from .validators import value_alpha


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[value_alpha])
    surname = serializers.CharField(validators=[value_alpha])


    class Meta:
        model = Author
        fields = ("id",
                  "name",
                  "surname",
                  "second_name"
                  )





class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True, required=True)
    author_name = serializers.CharField(source="author.__str__", read_only=True)


    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author_name",
            "author",
            "genre",
            "count_available",
            "all_count",
            )

    def validate(self, attrs):
        count_available = attrs.get(
            "count_available",
            self.instance.count_available if self.instance else None
        )
        all_count = attrs.get(
            "all_count",
            self.instance.all_count if self.instance else None
        )

        if count_available is None or all_count is None:
            return attrs

        if count_available > all_count:
            raise serializers.ValidationError(
                "Остаток не может быть больше общего количества"
            )

        return attrs



class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            "id",
            "user",
            "book",
            "taken_at",
            "return_at",
            "is_active",
        )
        read_only_fields = ("taken_at",)

    def validate(self, attrs):
        book = attrs.get("book")

        if book is None and self.instance:
            book = self.instance.book

        if self.instance is None and book.count_available <= 0:
            raise serializers.ValidationError(
                {"book": "Книга недоступна"}
            )

        return attrs

    def create(self, validated_data):
        book = validated_data["book"]

        book.count_available -= 1
        book.save(update_fields=["count_available"])

        validated_data["is_active"] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.is_active and validated_data.get("is_active") is False:
            instance.book.count_available += 1
            instance.book.save(update_fields=["count_available"])
            validated_data["return_at"] = now()

        return super().update(instance, validated_data)
