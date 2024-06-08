#________________"tekdosya" koleksiyonu____________________
#insepc veri setini kullanarak ön işleme yap ardından kelimeleri "tekdosya" kolkesiyonuna kaydet
#tüm makalelerin kelimelerini tek bir dosyada kaydediyor

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
koleksiiyonn = veriitabanii['tekdosya']

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

# Tüm kelimeleri depolamak için boş bir liste oluşturun
kelimeeSozluguu = []

# Anahtar kelimeleri ve abstract kısımları işleyin
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

            # Tüm kelimeler listesine ekle
            kelimeeSozluguu.extend(anahtarrKelimelerr)

# Metin dosyalarını işleyin
for rootdizinii, root_icindeki_dizinlerr, dosyalaarr in os.walk(docsklasorrYoluu):
    for dosyaaAdii in dosyalaarr:
        # Dosya adı .txt ile bitiyorsa
        if dosyaaAdii.endswith(".txt"):
            # Dosya adını ve rootdizinii yolunu birleştirerek tam dosya yolunu oluştur
            doc_dosya_yoluu = os.path.join(rootdizinii, dosyaaAdii)
            with open(doc_dosya_yoluu, "r", encoding="utf-8") as doc_dosyasii:
                dosyaaİcerigii = doc_dosyasii.read()
            # Dosyanın içeriğini tokenize edin
            dosyaaİcerigii = dosyaaİcerigii.lower()   # Küçük harfe dönüştür
            dosyaaİcerigii = dosyaaİcerigii.translate(str.maketrans('', '', string.punctuation))  # Noktalama işaretlerini kaldır
            dosyaaİcerigii = [kelimee for kelimee in word_tokenize(dosyaaİcerigii) if kelimee not in sstoppwwordss]   # Stopwords'leri kaldır
            dosyaaİcerigii = [kelimeeKokuu.stem(kelimee) for kelimee in dosyaaİcerigii]  # Kelime köklerini bul

            # Tüm kelimeler listesine ekle
            kelimeeSozluguu.extend(dosyaaİcerigii)

# Tekrarlanan kelimeleri kaldır
kelimeeSozluguu = list(set(kelimeeSozluguu))

# Tüm kelimeleri MongoDB'ye tek tek ekleyin
for kelimee in kelimeeSozluguu:
    koleksiiyonn.insert_one({"word": kelimee})

# Oluşturulan veriyi yazdır
print("Tüm kelimeler MongoDB'ye kaydedildi.")
