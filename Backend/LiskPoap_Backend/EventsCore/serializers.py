from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'metadata', 'location', 'creator', 'start_time']
        read_only_fields = ['id']