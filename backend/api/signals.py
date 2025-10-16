from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=UserProfile)
def calculate_daily_calories(sender, instance, created, **kwargs):
    """
    UserProfile oluşturulduğunda veya güncellendiğinde günlük kalori ihtiyacını
    (Bazal Metabolizma Hızı - BMR) Harris-Benedict formülüne göre hesaplar.
    """
    if not all([instance.age, instance.weight, instance.height, instance.gender]):
        return

    bmr = 0
    if instance.gender == UserProfile.Gender.MALE:
        bmr = 88.362 + (13.397 * instance.weight) + (4.799 * instance.height) - (5.677 * instance.age)
    elif instance.gender == UserProfile.Gender.FEMALE:
        bmr = 447.593 + (9.247 * instance.weight) + (3.098 * instance.height) - (4.330 * instance.age)

    post_save.disconnect(calculate_daily_calories, sender=UserProfile)
    instance.daily_calorie_need = round(bmr, 2)
    instance.save()
    post_save.connect(calculate_daily_calories, sender=UserProfile)