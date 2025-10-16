from rest_framework import serializers

class TodoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    completed = serializers.BooleanField(default=False)

class UserProfileSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=1)
    weight = serializers.FloatField(min_value=1, help_text="Kilo (kg)")
    height = serializers.IntegerField(min_value=1, help_text="Boy (cm)")
    gender = serializers.ChoiceField(choices=['Erkek', 'Kadın'])
    daily_calorie_need = serializers.FloatField(read_only=True, help_text="Günlük kalori ihtiyacı (BMR)")