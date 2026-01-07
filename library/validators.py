from rest_framework import serializers


def book_count(data):
    if data["count_available"] > data["all_count"]:
        raise serializers.ValidationError(
            "Остаток не может быть больше общего количества"
        )
    return data

def value_alpha(data):
    if not data.isalpha():
        raise serializers.ValidationError(
            "Недопустимые символы"
        )
    return data

