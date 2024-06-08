##________________"vektorscibert" koleksiyonu____________________
#"kelimeler" koleksiyonundan işlenmiş kelimeleri al ve onları scibert modelinden geçir
#kelimelerin tek tek vektörlerini çıkarır ve "vektorler" koleksiyonuna kaydeder.

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

# MongoDB'ye bağlan
clientiistemcii = MongoClient('mongodb://localhost:27017/')

# Veritabanı ve koleksiyonları seç
veriitabanii = clientiistemcii['yazlab']
kelimeler_Kolekisyonuu = veriitabanii['kelimeler']
inspec_Kolekisyonuu = veriitabanii['inspec']
vektorler_Kolekisyonuu = veriitabanii['vektorscibert']

# SciBERT modelini yükle
modeell = SentenceTransformer('allenai/scibert_scivocab_uncased')

# Tüm belgeleri al
#kelimeler koleksiyonundan tüm belgeler find() metodu ile alınıyor.
belgeleerr = kelimeler_Kolekisyonuu.find()

# Her bir belgee için vektörler oluştur ve veritabanına kaydet
for belgee in belgeleerr:
    belgeeAdii = belgee["name"]
    # "inspec" koleksiyonundan belgeye ait abstract alanını al
    inspecc_belgesii = inspec_Kolekisyonuu.find_one({"name": belgeeAdii})
    if inspecc_belgesii:
        abstractt = inspecc_belgesii.get("abstract", "")
        # Abstract'in ilk satırını başlık olarak kullan
        belgeeBasligii = abstractt.split('\n')[0]
    else:
        belgeeBasligii = ""  # Başlık bilgisi bulunamazsa boş bir başlık kullan


    #Her kelimenin scibert modelinden vektörü alınıyor ve kelime_vektorleri listesine ekleniyor.
    tummKelimelerr = belgee["Allwords"]
    kelimeeVektorleriiListesii = []
    for kelimee in tummKelimelerr:
        # scibert modelinden kelimenin vektörünü al
        kelimeeVektoruu = modeell.get_word_vector(kelimee)
        kelimeeVektorleriiListesii.append(kelimeeVektoruu)
    # Belgenin vektörlerinin ortalamasını al
    belgeeVektoruu = np.mean(kelimeeVektorleriiListesii, axis=0)
    # Belgeyi MongoDB'ye kaydet
    verileriiKaydett = {
        "name": belgeeAdii,
        "title": belgeeBasligii,
        "vektorler": belgeeVektoruu.tolist()
    }
    vektorler_Kolekisyonuu.insert_one(verileriiKaydett)

print("Vektörler başarıyla kaydedildi.")
