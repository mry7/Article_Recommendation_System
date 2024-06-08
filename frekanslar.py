#________________"frekanslar" koleksiyonu____________________
#insep veri kümesinde bulunan anahtar kelimelerin frekansını hesaplayıp en yüksek değer sahip
# 300 anahtar kelime (ilgi alani) yazdırıyor ve bunu "freknaslar" koleksiyonuna kaydediyor.


import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from pymongo import MongoClient
import fasttext
from sentence_transformers import SentenceTransformer

# MongoDB'ye bağlan
clientiistemcii = MongoClient('mongodb://localhost:27017/')

# Veritabanı ve koleksiyon seç
veriitabanii = clientiistemcii['yazlab']
ffrekanslar_koleksiyonuu = veriitabanii['frekanslar']
aaramaafasttext_koleksiyonuu = veriitabanii['aramafasttext']
aaramaascibert_koleksiyonuu = veriitabanii['aramascibert']

# İngilizce stopwords'leri yükle
nltk.download('stopwords')
nltk.download('punkt')

# Stopwords'leri yükle
sstoppwwordss = set(stopwords.words('english'))

# Tüm kelimelerin bulunduğu koleksiyon
kelime_frekanslari_sozlugu = {}

# Anahtar kelimelerin bulunduğu klasör yolu
klasorrYoluu = "Inspec/keys"

# Anahtar kelimeleri ve frekanslarını hesapla
#root:mevcut ana dizin, dirs: root içindeki alt dizinler
for rootdizinii, root_icindeki_dizinlerr, dosyalaarr in os.walk(klasorrYoluu):
    for dosyaaAdii in dosyalaarr:
        # Dosya adı .key ile bitiyorsa
        if dosyaaAdii.endswith(".key"):
            # Dosya adını ve root yolunu birleştirerek tam dosya yolunu oluştur
            dosyaaYoluu = os.path.join(rootdizinii, dosyaaAdii)
            with open(dosyaaYoluu, "r", encoding="utf-8") as keyDosyalarii:
                # Dosyayı oku ve satırları liste olarak al
                anahtarrKelimeeleerr = keyDosyalarii.read().splitlines()
            # Anahtar kelimelerin birleştirilmesi ve ön işlem uygulanması
            anahtarrKelimeeleerr = " ".join(anahtarrKelimeeleerr)
            anahtarrKelimeeleerr = anahtarrKelimeeleerr.lower()  # Küçük harfe dönüştür
            # Noktalama işaretlerini kaldır
            anahtarrKelimeeleerr = anahtarrKelimeeleerr.translate(str.maketrans('', '', string.punctuation))
            # Stopwords'leri kaldır ve tokenize et
            anahtarrKelimeeleerr = [kelime for kelime in word_tokenize(anahtarrKelimeeleerr) if kelime not in sstoppwwordss]

            # Anahtar kelimelerin frekanslarını hesapla
            for kelime in anahtarrKelimeeleerr:
                kelime_frekanslari_sozlugu[kelime] = kelime_frekanslari_sozlugu.get(kelime, 0) + 1

# En yüksek frekansa sahip olan ilk 300 kelimeyi bul
ennYuksekKelimelerr = sorted(kelime_frekanslari_sozlugu.items(), key=lambda x: x[1], reverse=True)[:300]

# Sonuçları konsola yazdır
print("En yüksek frekansa sahip olan ilk 300 kelime:")
for kelime, frekans in ennYuksekKelimelerr:
    print(f"Kelime: {kelime}, Frekans: {frekans}")

# MongoDB'ye frekans verilerini kaydet
for kelime, frekans in ennYuksekKelimelerr:
    ffrekanslar_koleksiyonuu.insert_one({"kelime": kelime, "frekans": frekans})

# Veri tabanına kaydedildiğini belirt
print("Frekans verileri MongoDB'ye kaydedildi.")

# fastText modelini yükle
fasttextModelii = fasttext.load_model("C:/Users/meryem/Downloads/cc.en.300.bin")

# SentenceTransformer modelini yükle
scibertModelii = SentenceTransformer('allenai/scibert_scivocab_uncased')

# fastText vektörlerini "aramafasttext" koleksiyonuna ekle
for kelime, frekans in ennYuksekKelimelerr:
    vektor = fasttextModelii.get_word_vector(kelime).tolist()
    aaramaafasttext_koleksiyonuu.insert_one({"kelime": kelime, "vektor": vektor})

# SciBERT vektörlerini "aramascibert" koleksiyonuna ekle
for kelime, frekans in ennYuksekKelimelerr:
    vektor = scibertModelii.encode(kelime).tolist()
    aaramaascibert_koleksiyonuu.insert_one({"kelime": kelime, "vektor": vektor})

# Vektör verilerinin kaydedildiğini belirt
print("FastText ve SciBERT vektör verileri MongoDB'ye kaydedildi.")
