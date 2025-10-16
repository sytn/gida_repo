from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet)
router.register(r'profile', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
]