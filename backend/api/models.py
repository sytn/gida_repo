from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    """
    Kullanıcının fiziksel bilgilerini ve hesaplanan kalori ihtiyacını tutan model.
    """
    class Gender(models.TextChoices):
        MALE = 'Erkek', 'Erkek'
        FEMALE = 'Kadın', 'Kadın'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    age = models.PositiveIntegerField()
    weight = models.FloatField(help_text="Kilo (kg)")
    height = models.PositiveIntegerField(help_text="Boy (cm)")
    gender = models.CharField(max_length=5, choices=Gender.choices)

    daily_calorie_need = models.FloatField(blank=True, null=True, help_text="Günlük kalori ihtiyacı (BMR)")

    def __str__(self):
        return f"{self.user.username}'s Profile"