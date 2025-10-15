## Gereksinimler

*   [Python 3.8+](https://www.python.org/downloads/)
*   [pip](https://pip.pypa.io/en/stable/installation/)

## Backend Kurulumu

Backend sunucusunu başlatmadan önce aşağıdaki adımları izleyerek proje ortamını hazırlamanız gerekmektedir.

1.  **Backend dizinine gidin:**
    ```bash
    cd backend
    ```

2.  **Sanal ortam (virtual environment) oluşturun:**
    Bu komut, proje bağımlılıklarını sisteminizden izole bir `venv` klasörü içinde yönetmenizi sağlar.
    ```bash
    python -m venv venv
    ```

3.  **Sanal ortamı aktifleştirin:**
    *   Windows için:
        ```bash
        venv\scripts\activate
        ```
    *   macOS / Linux için:
        ```bash
        source venv/bin/activate
        ```

4.  **Gerekli paketleri yükleyin:**
    `requirements.txt` dosyasında listelenen tüm kütüphaneler otomatik olarak kurulacaktır.
    ```bash
    pip install -r requirements.txt
    ```

## Projeyi Çalıştırma

Kurulum adımlarını tamamladıktan sonra, geliştirme sunucusunu başlatmak için aşağıdaki komutu çalıştırın.

```bash
python manage.py runserver
```

Sunucu varsayılan olarak `http://127.0.0.1:8000/` adresinde çalışmaya başlayacaktır. Tarayıcınızdan bu adrese giderek uygulamayı görüntüleyebilirsiniz.