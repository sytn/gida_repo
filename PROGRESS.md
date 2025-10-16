
# Proje İlerleme Raporu (progress.md)

Bu dosya, React Native (Frontend) ve Django (Backend) kullanılarak geliştirilen kalori takip uygulamasının ilerlemesini, tamamlanan adımları ve gelecek hedeflerini belgelemektedir.

## 1. Tamamlanan Adımlar (Mevcut Durum)

### **Backend (Django & Firebase/Firestore)**

* **Proje Kurulumu**: Django projesi (`backend`) ve birincil uygulama (`api`) başarılı bir şekilde oluşturuldu.
* **Firebase Entegrasyonu**: Firebase Admin SDK, `firebase-admin` kütüphanesi ile projeye entegre edildi. `settings.py` dosyası içinde servis hesabı anahtarı (`firebase-service-account.json`) kullanılarak başlangıç yapılandırması tamamlandı. Veritabanı olarak geleneksel bir SQL veritabanı yerine Firestore NoSQL veritabanı kullanılmaktadır.
* **API Altyapısı**: Django Rest Framework (`djangorestframework`) ve `django-cors-headers` projeye dahil edilerek API geliştirme için temel altyapı kuruldu.
* **Firebase Kimlik Doğrulama**: Frontend'den gelen Firebase ID Token'larını doğrulamak için `api/auth.py` içinde özel bir `FirebaseAuthentication` sınıfı oluşturuldu. Bu, Django endpoint'lerinin Firebase kullanıcıları tarafından güvenli bir şekilde kullanılmasını sağlar.
* **Test Endpoint'i**: Geliştirme amacıyla Firestore ile etkileşime geçen bir `UserProfileView` oluşturuldu. Bu view, `/api/profile/` endpoint'i üzerinden giriş yapmış kullanıcının profil verilerini Firestore'dan okuma ve Firestore'a yazma (CRUD) işlemlerini test edilebilir durumdadır.

### **Frontend (React Native & Firebase)**

* **Proje Kurulumu**: Expo kullanılarak bir React Native projesi (`frontend`) başlatıldı.
* **Firebase İstemci Kurulumu**: Firebase JavaScript istemcisi (`firebase`) projeye eklendi ve `lib/firebase.ts` dosyasında yapılandırıldı.
* **Temel Kimlik Doğrulama**: Kullanıcıların e-posta ve şifre ile kaydolup giriş yapabilmesi için Firebase Authentication ile entegrasyon sağlandı. `App.tsx` içerisinde `createUserWithEmailAndPassword` ve `signInWithEmailAndPassword` fonksiyonları kullanılarak temel bir kimlik doğrulama akışı oluşturuldu.
* **Oturum Yönetimi**: `onAuthStateChanged` listener'ı ile kullanıcının oturum durumu anlık olarak takip edilerek uygulama arayüzü (giriş yapmış veya yapmamış) buna göre güncellenmektedir. Kullanıcı bilgilerinin kalıcı olması için `@react-native-async-storage/async-storage` kullanılmıştır.

## 2. Planlanan Adımlar ve Gelecek Özellikler

### **Aşama 1: Kullanıcı Profili ve Kalori Hesaplama**

* **[ ] Backend: Firestore Veri Yapısının Genişletilmesi**
  * `user_profiles` koleksiyonundaki her bir doküman, Firebase UID'si ile isimlendirilecek.
  * Bu dokümanlarda `yas`, `kilo`, `boy`, `cinsiyet` ve hesaplanmış `gunluk_kalori_ihtiyaci` gibi alanlar bulunacak.
* **[ ] Backend: Profil için API Endpoint'lerinin Geliştirilmesi**
  * Mevcut `UserProfileView` geliştirilerek giriş yapmış kullanıcının kendi profilini (`/api/profile/`) oluşturup güncelleyebilmesi sağlanacak.
* **[ ] Backend: Kalori Hesaplama Mantığının Eklenmesi**
  * Kullanıcı profili kaydedildiğinde veya güncellendiğinde, `UserProfileView` içindeki `_calculate_bmr` metodu gibi bir yapı kullanılarak girilen bilgilere (yaş, kilo, boy, cinsiyet) göre günlük kalori ihtiyacı (Harris-Benedict formülü ile) hesaplanacak ve `gunluk_kalori_ihtiyaci` alanına kaydedilecek.
* **[ ] Frontend: Profil Yönetim Ekranının Oluşturulması**
  * Kullanıcıların yaş, kilo, boy ve cinsiyet bilgilerini girebilecekleri yeni bir "Profil" ekranı tasarlanacak.
  * Bu ekrandaki form, backend'deki `/api/profile/` endpoint'i ile haberleşerek kullanıcının bilgilerini Firestore'a kaydedecek ve güncelleyecek.
  * Backend'den gelen hesaplanmış günlük kalori ihtiyacı bu ekranda kullanıcıya gösterilecek.

### **Aşama 2: Sosyal Medya ile Giriş Entegrasyonu**

* **[ ] Altyapı: Firebase ve Google/Apple Konsol Ayarları**
  * Firebase projesinin "Authentication -> Sign-in method" bölümünden Google ve Apple sağlayıcıları aktif edilecek.
  * Google Cloud Console ve Apple Developer Console üzerinden gerekli OAuth kimlik bilgileri alınacak ve Firebase ayarlarına eklenecek.
* **[ ] Frontend: Giriş Ekranının Güncellenmesi**
  * `App.tsx` ekranına "Google ile Giriş Yap" ve "Apple ile Giriş Yap" butonları eklenecek.
  * Bu butonlara tıklandığında, Firebase'in ilgili sağlayıcı (`GoogleAuthProvider`, `OAuthProvider` vb.) fonksiyonları kullanılarak kimlik doğrulama işlemi başlatılacak.

### **Aşama 3: Besin ve Tüketim Takibi**

* **[ ] Backend: Yeni Firestore Koleksiyonlarının Eklenmesi**
  * `products`: Market ürünlerinin adını, barkodunu ve besin değerlerini (100 gr için kalori, protein, yağ, karbonhidrat) tutan bir koleksiyon oluşturulacak.
  * `consumptions`: Hangi kullanıcının (kullanıcı UID'si ile referans), hangi üründen (product doküman ID'si ile referans), kaç gram ve hangi tarihte tükettiğini kaydeden bir koleksiyon oluşturulacak.
* **[ ] Backend: Yeni API Endpoint'lerinin Oluşturulması**
  * Ürünleri aramak ve listelemek için bir endpoint (örn: `/api/products/`).
  * Kullanıcının tükettiği besinleri eklemesi, listelemesi ve silmesi için bir endpoint (örn: `/api/consumptions/`).
* **[ ] Frontend: Tüketim Takip Ekranları**
  * Kullanıcının ürün arayabileceği bir arama çubuğu ve sonuç listesi içeren bir ekran geliştirilecek.
  * Kullanıcının, seçtiği bir ürün için tükettiği gramajı gireceği bir arayüz (modal veya yeni ekran) oluşturulacak.
  * Kullanıcının o gün tükettiği besinleri ve toplam aldığı kaloriyi gösteren bir "Günlük Özet" ekranı tasarlanacak.

### **Aşama 4: Yapay Zeka ile Besin Değeri Okuma**

* **[ ] Backend: Görüntü İşleme için API Endpoint'i Oluşturma**
  * Frontend'den gönderilen ürün etiket fotoğrafını alacak yeni bir endpoint oluşturulacak (örn: `/api/ocr/upload-image/`).
* **[ ] Backend: OCR Entegrasyonu**
  * Gelen fotoğrafı işlemek için bir OCR (Optik Karakter Tanıma) kütüphanesi veya servisi entegre edilecek. Python için popüler seçenekler arasında Mindee, Tesseract (pytesseract wrapper'ı ile) veya Google Cloud Vision AI bulunmaktadır.
  * OCR'dan dönen metin işlenerek "kalori", "yağ", "protein" gibi anahtar kelimeler ve bunlara karşılık gelen sayısal değerler ayrıştırılacak.
* **[ ] Frontend: Kamera Entegrasyonu**
  * Kullanıcının ürün etiketinin fotoğrafını çekmesine olanak tanıyan bir arayüz eklenecek (`expo-camera` kütüphanesi kullanılabilir).
  * Çekilen fotoğraf, backend'deki `/api/ocr/upload-image/` endpoint'ine gönderilecek.
  * Backend'den dönen ayrıştırılmış besin değerleri (kalori, yağ, protein vb.) kullanıcıya bir onay ekranında gösterilecek ve kullanıcı onayıyla `products` koleksiyonuna yeni bir ürün olarak kaydedilecek.
