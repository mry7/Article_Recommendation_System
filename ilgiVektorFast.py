#________________"ilgivektorfast" koleksiyonu____________________
#"ilgialani" koleksiyonundan ilgi alanlarını çekiyor sonra ortalamasını alıyor
#ardından fasttext kullanarak vektörleirn ortalamasını "ilgivektorfast" koleksiyonuna kaydediyor (300)

from pymongo import MongoClient
import fasttext
import numpy as np

# FastText modelini yükle
modeell = fasttext.load_model('C:/Users/meryem/Downloads/cc.en.300.bin')

# MongoDB istemcisini oluştur
clientiistemcii = MongoClient('mongodb://localhost:27017/')
veriitabanii = clientiistemcii['yazlab']  # Veritabanı adını yazın
koleksiiyonn = veriitabanii['ilgialani']  # Koleksiyon adını yazın

# Alınan ilgi alanlarını MongoDB'den çekin
veritabaniiNesnesii = koleksiiyonn.find({}, {"_id": 0, "ilgi_alani": 1})

# Her bir belge için işlemleri gerçekleştir
for veritabaniiBelgesii in veritabaniiNesnesii:
    ilgi_alani = veritabaniiBelgesii['ilgi_alani']
    # İlgili alanları vektörlere dönüştürmek için FastText kullanılır
    vektorrlerr = []
    for ilgiiAlanii in ilgi_alani:
        # Her ilgi alanı için FastText vektörü al
        vektorr = modeell.get_sentence_vector(ilgiiAlanii)
        # Vektörü listeye ekle
        vektorrlerr.append(vektorr)

    # Vektörlerin ortalamasını al
    if vektorrlerr:
        # Vektörlerin ortalamasını hesapla ve listeye dönüştür
        vektor_ortalamasi = np.mean(vektorrlerr, axis=0).tolist()

        # Vektörü konsola yazdır
        print("ilgiiAlanii:", ilgi_alani)
        print("vektorr ortalamasii:", vektor_ortalamasi)

        # Vektörü MongoDB'ye kaydet
        vektorVerilerii = {'ilgi_alani': ilgi_alani, 'vektor_ortalamasi': vektor_ortalamasi}
        veriitabanii['ilgivektorfast'].insert_one(vektorVerilerii)
