# YourBookingHub.org - Multi-Tenant Hotel SaaS Platform

## Sistem Özellikleri

Bu paket, otellere AI destekli email otomasyonu sunan komple bir SaaS platformudur.

### Ana Özellikler:
- **Multi-Tenant Yapı**: Her otel için ayrı hesap ve branding
- **AI Email İşleme**: OpenAI GPT-4o ile otomatik email analizi
- **5 Dil Desteği**: Türkçe, İngilizce, Almanca, Fransızca, Rusça
- **Gmail Entegrasyonu**: Otomatik email okuma ve yanıt gönderme
- **Admin Paneli**: Otel hesaplarını yönetme
- **Fiyatlandırma**: Dinamik pricing hesaplamaları

## Dosya Yapısı

```
yourbookinghub_saas_system/
├── multi_tenant_app.py          # Ana SaaS platformu
├── database.py                  # Veritabanı işlemleri
├── email_processor.py           # Email işleme
├── email_templates.py           # Email template'leri
├── vercel.json                  # Vercel deployment config
├── requirements.txt             # Python paketleri
├── .env.example                 # Environment variables örneği
├── templates/
│   ├── yourbookinghub_homepage.html    # Ana sayfa
│   ├── admin_dashboard.html            # Admin paneli
│   ├── create_hotel.html               # Otel oluşturma
│   ├── hotel_login.html                # Otel giriş
│   └── hotel_dashboard.html            # Otel dashboard
└── README.md                    # Bu dosya
```

## Kurulum

### 1. Gerekli Paketleri Kurun
```bash
pip install -r requirements.txt
```

### 2. Environment Variables Ayarlayın
`.env.example` dosyasını `.env` olarak kopyalayın ve API key'lerinizi ekleyin:
```
OPENAI_API_KEY=sk-...
GMAIL_CLIENT_ID=...
GMAIL_CLIENT_SECRET=...
FLASK_SECRET_KEY=supersecretkey123
```

### 3. Lokal Çalıştırma
```bash
python multi_tenant_app.py
```

### 4. Vercel Deployment

**Dosya Yapısı:**
```
yourbookinghub_saas_system/
├── api/index.py                 # Vercel serverless function
├── multi_tenant_app.py          # Ana Flask app
├── vercel.json                  # Vercel config
└── ...
```

**Deployment Adımları:**
1. GitHub repository'yi Vercel'e bağlayın
2. Environment Variables ekleyin:
   - OPENAI_API_KEY
   - GMAIL_CLIENT_ID  
   - GMAIL_CLIENT_SECRET
   - FLASK_SECRET_KEY
3. Deploy edin

**Vercel Configuration (vercel.json):**
- `api/index.py` dosyası serverless function olarak çalışır
- Tüm route'lar `/api/index` endpoint'ine yönlendirilir
- Flask app otomatik olarak serverless ortamda çalışır

## Kullanım

### Admin Paneli
- URL: `/admin`
- Kullanıcı: `admin`
- Şifre: `admin123`

### Demo Otel Hesapları
- **Cornelia**: `/hotel/cornelia` (Şifre: admin123)
- **Rixos**: `/hotel/rixos` (Şifre: demo123)

### Yeni Otel Oluşturma
- Admin panelinden "Yeni Otel Ekle" butonuna tıklayın
- Otel bilgilerini girin
- Sistem otomatik olarak otel hesabını oluşturacak

## Abonelik Planları

- **Başlangıç**: $99/ay - 1,000 email
- **Profesyonel**: $199/ay - 5,000 email
- **Kurumsal**: $399/ay - Sınırsız email

## Teknik Detaylar

### Multi-Tenant Architecture
- Her otel için ayrı SQLite veritabanı
- Domain-based routing (/hotel/domain_name)
- Otel-specific branding ve email template'leri

### AI Email Processing
- OpenAI GPT-4o ile email analizi
- Otomatik dil tespiti
- Booking information extraction
- Personalized response generation

### Gmail Integration
- OAuth 2.0 authentication
- Real-time email monitoring
- Automated response sending
- Email tracking ve analytics

## Destek

YourBookingHub.org ekibi tarafından geliştirilmiştir.
Email: support@yourbookinghub.org