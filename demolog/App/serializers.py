from rest_framework import serializers
from .models import LogSample

class LogSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSample
        fields = '__all__'