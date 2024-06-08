#________________"inspec" koleksiyonu____________________
#inspec veri setinde bulunan makalelerin ön işlemesini yapıyor ardından
#makalelerin numarası,anahtar kelimeleri,özetini "inspec" koleksiyonuna kaydeder.

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
koleksiiyonn = veriitabanii['inspec']

# İngilizce stopwords'leri yükle
nltk.download('stopwords')
nltk.download('punkt')

# Stopwords'leri yükle
sstoppwwordss = set(stopwords.words('english'))

# Anahtar kelimelerin bulunduğu klasör yolu
keyssklasorrYoluu = "inspec/keys"

# Metin dosyalarının bulunduğu klasör yolu
docsklasorrYoluu = "inspec/docsutf8"

# Anahtar kelimeleri ve abstract kısımları depolamak için boş bir sözlük oluştur
makaleeSozluguu = {}

# Anahtar kelimeleri oku
for rootdizinii, root_icindeki_dizinlerr, dosyalaarr in os.walk(keyssklasorrYoluu):
    for dosyaaAdii in dosyalaarr:
        # Dosya adı .key ile bitiyorsa
        if dosyaaAdii.endswith(".key"):
            # Dosya adını ve rootdizinii yolunu birleştirerek tam dosya yolunu oluştur
            key_dosya_yoluu = os.path.join(rootdizinii, dosyaaAdii)
            with open(key_dosya_yoluu, "r", encoding="utf-8") as key_dosyasii:
                # Dosyayı oku ve satırları liste olarak al
                anahtarrKelimelerr = key_dosyasii.read().splitlines()
            # Anahtar kelimelerin birleştirilmesi
            anahtarrKelimelerr = " ".join(anahtarrKelimelerr)

            # Makalenin adını al
            # os.path.splitext: Dosya adının uzantısını kaldırır
            makaleeAdii = os.path.splitext(dosyaaAdii)[0]

            # Makalenin abstract kısmını oku
            doc_dosya_yoluu = os.path.join(docsklasorrYoluu, makaleeAdii + ".txt")
            # Dosya adını ve doc_dosya_yoluu  birleştirerek tam dosya yolunu oluştur
            with open(doc_dosya_yoluu, "r", encoding="utf-8") as doc_dosyasii:
                # Dosyayı oku
                abstract = doc_dosyasii.read()

            # Anahtar kelimeler ve abstract kısmını sözlüğe ekle
            makaleeSozluguu[makaleeAdii] = {"keys": anahtarrKelimelerr, "abstract": abstract}

# Oluşturulan veriyi MongoDB'ye kaydet
for makaleeAdii, verii in makaleeSozluguu.items():
    makaalee = {"name": makaleeAdii, "keys": verii["keys"], "abstract": verii["abstract"]}
    koleksiiyonn.insert_one(makaalee)
