# RAG-Based Question and Answer

Bu proje, Retrieval-Augmented Generation (RAG) tabanlı bir soru-cevap sistemini içerir. Proje, belirli bir veri kümesine dayalı olarak kullanıcının sorduğu sorulara yanıt vermek için doğal dil işleme (NLP) yöntemlerini kullanır.

## Özellikler

- PDF belgelerini yükleyip işleyebilir.
- İçeriği analiz ederek anlamlı yanıtlar üretir.
- PostgresQL veritabanı kullanarak gömülü metinleri indeksler.

## Başlarken

### Gereksinimler

- Python 3.8 veya daha yeni bir sürümü
- Docker

### Kurulum

#### Sanal Ortam

1. Python sanal ortamını oluşturun ve etkinleştirin:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

