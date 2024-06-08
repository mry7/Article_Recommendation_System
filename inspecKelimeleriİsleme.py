#________________"kelimeler" koleksiyonu____________________
#inspec veri setinde bulunan makalelerin, her bir makalesinin ön işlemisini yapıyor
#ardından her bir makalenin kelimelerini bir listede tutuyor ve "kelimeler" koleksiyonuna kaydediyor
#sonrasında brada bulunan her bir makalenin kelimlerinin vektörleri çıkarılıp ortalaması alınacak

import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
from pymongo import MongoClient

# MongoDB'ye bağlan
clientiistemcii = MongoClient('mongodb://localhost:27017/')

# Veritabanı ve koleksiyon seç
veriitabanii = clientiistemcii['yazlab']
koleksiiyonn = veriitabanii['kelimeler']

# İngilizce stopwords'leri yükle
nltk.download('stopwords')
nltk.download('punkt')

# Stopwords'leri yükle
sstoppwwordss = set(stopwords.words('english'))

# Anahtar kelimelerin bulunduğu klasör yolu
keyssklasorrYoluu = "Inspec/keys"

# Metin dosyalarının bulunduğu klasör yolu
docsklasorrYoluu = "Inspec/docsutf8"

# Kelime köklerini bulmak için kelimeeKokuu oluştur
kelimeeKokuu = PorterStemmer()

# Tüm anahtar kelimeleri ve abstracttt kelimelerini depolamak için boş bir liste oluşturun
kelimeeSozluguu = []

# Anahtar kelimeleri ve abstracttt kısımları işleyin
for rootdizinii, root_icindeki_dizinlerr, dosyalaarr in os.walk(keyssklasorrYoluu):
    for dosyaaAdii in dosyalaarr:
        # Dosya adı .key ile bitiyorsa
        if dosyaaAdii.endswith(".key"):
            # Dosya adını ve rootdizinii yolunu birleştirerek tam dosya yolunu oluştur
            key_dosya_yoluu = os.path.join(rootdizinii, dosyaaAdii)
            with open(key_dosya_yoluu, "r", encoding="utf-8") as key_dosyasii:
                # Dosyayı oku ve satırları liste olarak al
                anahtarrKelimelerr = key_dosyasii.read().splitlines()
            # Anahtar kelimelerin birleştirilmesi ve ön işlem uygulanması
            anahtarrKelimelerr = " ".join(anahtarrKelimelerr)
            anahtarrKelimelerr = anahtarrKelimelerr.lower()  # Küçük harfe dönüştür
            anahtarrKelimelerr = anahtarrKelimelerr.translate(str.maketrans('', '', string.punctuation))  # Noktalama işaretlerini kaldır
            anahtarrKelimelerr = [kelimee for kelimee in word_tokenize(anahtarrKelimelerr) if kelimee not in sstoppwwordss]  # Stopwords'leri kaldır
            anahtarrKelimelerr = [kelimeeKokuu.stem(kelimee) for kelimee in anahtarrKelimelerr]  # Kelime köklerini bul

            # Makalenin adını alın
            makaleeAdii = os.path.splitext(dosyaaAdii)[0]

            # Makalenin abstracttt kısmını okuyun
            doc_dosya_yoluu = os.path.join(docsklasorrYoluu, makaleeAdii + ".txt")
            with open(doc_dosya_yoluu, "r", encoding="utf-8") as doc_dosyasii:
                abstracttt = doc_dosyasii.read()

            # Abstract kısmı için de aynı ön işlemleri uygula
            abstracttt = abstracttt.lower()
            abstracttt = abstracttt.translate(str.maketrans('', '', string.punctuation))
            abstracttt = [kelimee for kelimee in word_tokenize(abstracttt) if kelimee not in sstoppwwordss]
            abstracttt = [kelimeeKokuu.stem(kelimee) for kelimee in abstracttt]

            # Anahtar kelimeleri ve abstracttt kelimelerini birleştir
            tummKelimelerr = anahtarrKelimelerr + abstracttt

            # Tüm kelimeleri listeye ekle
            kelimeeSozluguu.append({"name": makaleeAdii, "Allwords": tummKelimelerr})

# MongoDB'ye kaydet
koleksiiyonn.insert_many(kelimeeSozluguu)

# Oluşturulan veriyi yazdır
for ogee in kelimeeSozluguu:
    print("Makale Adı:", ogee["name"])
    print("Tüm Kelimeler:", ogee["Allwords"])
    print()
