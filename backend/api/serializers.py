from rest_framework import serializers
from .models import Todo, UserProfile
from django.contrib.auth.models import User

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['user', 'age', 'weight', 'height', 'gender', 'daily_calorie_need']
        read_only_fields = ['daily_calorie_need']