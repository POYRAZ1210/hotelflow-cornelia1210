# Vercel Deployment Rehberi

## Deployment Adımları

### 1. GitHub Repository Hazırlığı
```bash
# Tüm dosyaları GitHub repository'nize yükleyin
git add .
git commit -m "YourBookingHub.org SaaS system ready for Vercel"
git push origin main
```

### 2. Vercel Proje Kurulumu
1. https://vercel.com/new sayfasına gidin
2. GitHub repository'nizi seçin
3. **Framework Preset**: "Other" seçin
4. **Root Directory**: `.` (nokta) bırakın

### 3. Environment Variables Ayarlama
Vercel dashboard'da "Environment Variables" kısmına ekleyin:

```
OPENAI_API_KEY = sk-proj-... (OpenAI API key'iniz)
GMAIL_CLIENT_ID = xxxxxx.apps.googleusercontent.com
GMAIL_CLIENT_SECRET = GOCSPX-xxxxxxxxxx
FLASK_SECRET_KEY = supersecretkey12345
```

### 4. Deploy Butonu
"Deploy" butonuna tıklayın ve bekleyin.

## Yaygın Hatalar ve Çözümleri

### Hata: "Function Runtimes must have a valid version"
**Çözüm**: `vercel.json` dosyasında şu yapılandırmayı kullanın:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

### Hata: "FUNCTION_INVOCATION_FAILED"
**Çözüm**: `api/index.py` dosyasında Flask app'in doğru export edildiğinden emin olun:
```python
from multi_tenant_app import app
application = app  # Vercel için gerekli
```

### Hata: "Module not found"
**Çözüm**: `requirements.txt` dosyasının proje kök dizininde olduğundan emin olun.

### Hata: "500 Internal Server Error"
**Çözüm**: 
1. Vercel dashboard'da Function Logs'u kontrol edin
2. Environment variables'ların doğru tanımlandığından emin olun
3. API key'lerin geçerli olduğunu doğrulayın

## Test Etme

Deployment başarılı olduktan sonra:

1. **Ana Sayfa**: `https://your-app.vercel.app/`
2. **Admin Panel**: `https://your-app.vercel.app/admin`
   - Kullanıcı: `admin`
   - Şifre: `admin123`
3. **Otel Hesapları**: 
   - Cornelia: `https://your-app.vercel.app/hotel/cornelia`
   - Rixos: `https://your-app.vercel.app/hotel/rixos`

## Domain Bağlama

Deployment başarılı olduktan sonra:

1. Vercel dashboard'da "Settings" > "Domains" gidin
2. "Add Domain" butonuna tıklayın
3. `yourbookinghub.org` domain'ini ekleyin
4. DNS ayarlarını domain sağlayıcınızda yapın:
   - A Record: `76.76.19.61`
   - CNAME: `cname.vercel-dns.com`

## Sorun Giderme

### Logs Kontrol Etme
1. Vercel dashboard'da projenizi açın
2. "Functions" tab'ına gidin
3. "View Function Logs" linkine tıklayın
4. Error mesajlarını kontrol edin

### Yaygın Sorunlar
- **OpenAI API hatası**: OPENAI_API_KEY environment variable'ını kontrol edin
- **Gmail hatası**: GMAIL_CLIENT_ID ve GMAIL_CLIENT_SECRET'i kontrol edin
- **Database hatası**: SQLite dosyalarının serverless environment'da çalışmayabileceğini unutmayın

## Production Hazırlığı

Üretim ortamı için:
1. Environment variables'ı production değerleriyle güncelleyin
2. Debug mode'u kapatın
3. Güvenlik ayarlarını kontrol edin
4. Rate limiting ekleyin
5. Error monitoring yapın

## Destek

Sorun yaşarsanız:
1. Function logs'u kontrol edin
2. GitHub Issues açın
3. Vercel community forumlarından yardım alın