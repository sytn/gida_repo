from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import firestore
from .serializers import TodoSerializer, UserProfileSerializer
from .auth import FirebaseAuthentication

db = firestore.client()

class TodoView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        """Tüm todoları listeler"""
        todos_ref = db.collection('todos').stream()
        todos = []
        for todo in todos_ref:
            todo_data = todo.to_dict()
            todo_data['id'] = todo.id
            todos.append(todo_data)
        return Response(todos, status=status.HTTP_200_OK)

    def post(self, request):
        """Yeni bir todo oluşturur"""
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            db.collection('todos').add(data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def _calculate_bmr(self, data):
        """Harris-Benedict formülüne göre BMR hesaplar."""
        bmr = 0
        if data['gender'] == 'Erkek':
            bmr = 88.362 + (13.397 * data['weight']) + (4.799 * data['height']) - (5.677 * data['age'])
        elif data['gender'] == 'Kadın':
            bmr = 447.593 + (9.247 * data['weight']) + (3.098 * data['height']) - (4.330 * data['age'])
        return round(bmr, 2)

    def get(self, request):
        """Giriş yapmış kullanıcının profilini getirir."""
        user_id = request.user.get('uid')
        profile_ref = db.collection('user_profiles').document(user_id)
        profile = profile_ref.get()

        if not profile.exists:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(profile.to_dict(), status=status.HTTP_200_OK)

    def post(self, request):
        """Yeni bir kullanıcı profili oluşturur veya mevcut olanı günceller."""
        user_id = request.user.get('uid')
        serializer = UserProfileSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        profile_data = serializer.validated_data
        profile_data['daily_calorie_need'] = self._calculate_bmr(profile_data)
        
        db.collection('user_profiles').document(user_id).set(profile_data)
        
        return Response(profile_data, status=status.HTTP_201_CREATED)