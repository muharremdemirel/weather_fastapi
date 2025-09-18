# Hava Durumu Fastapi 🌦️

Bu proje fastapi ile geliştirilmiş basit bir hava durumu API’sidir.  
Open Meteo servisinden şehir bazlı hava durumu verilerini alır ve SQLite veritabanına kaydeder.  
Swagger arayüzü sayesinde kolayca test edilebilir.

## Özellikler
- Şehir adıyla anlık hava durumu verisi çekme → `POST /weather/fetch?city=Istanbul`
- Veriyi SQLite veritabanına kaydetme (fetch işlemi ile otomatik kaydedilir)
- Son eklenen kaydı görüntüleme → `GET /weather/latest?city=Istanbul`
- Kayıt geçmişini listeleme → `GET /weather/history?city=Istanbul&limit=5`
- Çalışma durumu kontrolü → `GET /health`


## Kurulum
```bash
cd weather_fastapi

python -m venv venv

.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

``` 


## Çalıştırma

Projeyi başlatmak için terminalde aşağıdaki komutu çalıştırın

```bash
uvicorn app.main:app --reload
```

Tarayıcıdan erişebilirsiniz -> http://127.0.0.1:8000/docs



