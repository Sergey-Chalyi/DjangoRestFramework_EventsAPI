from rest_framework import serializers
from events.models import Event
from django.core.exceptions import ValidationError


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.

    This serializer handles the serialization and deserialization of Event objects,
    including validation of invited users.

    Attributes:
        Meta: Inner class defining metadata for the serializer.
    """

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'date', 'organizer', 'invited_users', 'time_created']
        read_only_fields = ['organizer', 'time_created']

    def validate_invited_users(self, value):
        """
        Validate the invited users for an event.

        This method ensures that the event organizer is not included in the list of invited users.

        Args:
            value (list): A list of User objects representing the invited users.

        Returns:
            list: The validated list of invited users.

        Raises:
            ValidationError: If the organizer is included in the list of invited users.
        """
        user = self.context['request'].user  # get the current user (organizer)

        if user in value: # check that the organizer cannot be invited
            raise ValidationError("You cannot invite yourself to your event!")

        return value

