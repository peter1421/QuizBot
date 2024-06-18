# serializers.py
from apps.chatbot.python.models import PythonChatMessage
from rest_framework import serializers


class PythonChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PythonChatMessage
        fields = '__all__'
