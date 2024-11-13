from rest_framework import serializers
from events.models import Event
from django.core.exceptions import ValidationError


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'date', 'organizer', 'invited_users', 'time_created']
        read_only_fields = ['organizer', 'time_created']

    def validate_invited_users(self, value):
        user = self.context['request'].user  # Получаем текущего пользователя (организатора)

        # Проверка, что организатор не может быть приглашен
        if user in value:
            raise ValidationError("Вы не можете пригласить себя на ваше событие.")

        return value