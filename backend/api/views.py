from rest_framework import viewsets, permissions
from .models import Todo, UserProfile
from .serializers import TodoSerializer, UserProfileSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Giriş yapmış kullanıcının kendi profilini görüntülemesi ve güncellemesi için ViewSet.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Bu view sadece mevcut kullanıcıya ait profili döndürür.
        """
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Yeni bir profil oluşturulurken, user alanını otomatik olarak
        giriş yapmış kullanıcı olarak ayarlar.
        """
        serializer.save(user=self.request.user)