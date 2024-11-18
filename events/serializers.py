from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Event , Participant


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'venue', 'location', 'time', 'description', 'link_or_qr', 'created_by']

    def create(self, validated_data):
        # Set the 'created_by' field to the current authenticated user
        user = self.context['request'].user  # Access 'request' from the context
        validated_data['created_by'] = user
        return super().create(validated_data)


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'