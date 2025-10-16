from django.urls import path
from .views import TodoView, UserProfileView

urlpatterns = [
    path('todos/', TodoView.as_view(), name='todo-list'),
    path('todos/<str:todo_id>/', TodoView.as_view(), name='todo-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]