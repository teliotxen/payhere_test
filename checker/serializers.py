from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'user',
            'amount',
            'note',
        ]

    def validate(self, data):
        if data['user'] == None:
            raise serializers.ValidationError(
                "check auth information"
            )
        if len(data['note']) >= 255:
            raise serializers.ValidationError(
                "you exceed word count "
            )
        return data