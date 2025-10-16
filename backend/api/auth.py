from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth

class FirebaseAuthentication(BaseAuthentication):
    """
    Frontend'den gönderilen Firebase ID Token'ını doğrulayan kimlik doğrulama sınıfı.
    """
    def authenticate(self, request):
        # HTTP Authorization başlığını al
        auth_header = request.headers.get('Authorization')

        # Eğer başlık yoksa, kimlik doğrulaması yapılamaz
        if not auth_header:
            return None

        # "Bearer <token>" formatını işle
        try:
            # Başlığı "Bearer" ve token olarak ikiye ayır
            prefix, id_token = auth_header.split(' ')

            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Authorization header must start with "Bearer"')

            # Firebase Admin SDK'sı ile token'ı doğrula
            decoded_token = auth.verify_id_token(id_token)
        
        # Herhangi bir hata durumunda (geçersiz token, format hatası vb.)
        except Exception as e:
            raise AuthenticationFailed(f'Invalid Firebase ID token: {e}')

        # Token başarılı bir şekilde doğrulanırsa, DRF'in `request.user` nesnesini
        # bu token bilgisiyle doldur ve `request.auth` nesnesini boş bırak.
        # Artık view'lar içinde `request.user` üzerinden kullanıcı bilgilerine erişilebilir.
        return (decoded_token, None)