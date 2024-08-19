# Python 3.8 kullanan bir imajı kullan
FROM python:3.8.2

# Çalışma dizinini /code olarak ayarla
WORKDIR /code

# Gereksinimler dosyasını /code/ içine kopyala
COPY requirements.txt /code/

# Gerekli Python paketlerini kur
RUN pip install --no-cache-dir -r requirements.txt

# Projeyi /code/ içine kopyala
COPY . /code/
