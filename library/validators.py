from rest_framework import serializers


def value_alpha(data):
    if not data.isalpha():
        raise serializers.ValidationError(
            "Недопустимые символы"
        )
    return data

