#____________________________________"ilgivektor" koleksiyonu______________________________
#"ilgialani" koleksiyonundan ilgi alanlarını çekiyor sonra ortalamasını alıyor
#ardından scibert kullanarak vektörleirn ortalamasını "ilgivektor" koleksiyonuna kaydediyor (768)

from transformers import AutoTokenizer, AutoModel
from pymongo import MongoClient
import torch

# Scibert modeli ve tokenizer yüklenir
modeellAdii = "allenai/scibert_scivocab_uncased"
tokenizer = AutoTokenizer.from_pretrained(modeellAdii)
modeell = AutoModel.from_pretrained(modeellAdii)

# MongoDB istemcisini oluştur
clientiistemcii = MongoClient('mongodb://localhost:27017/')
veriitabanii = clientiistemcii['yazlab']  # Veritabanı adını yazın
koleksiiyonn = veriitabanii['ilgialani']  # Koleksiyon adını yazın

# Alınan ilgi alanlarını MongoDB'den çekin
veritabaniiNesnesii = koleksiiyonn.find({}, {"_id": 0, "ilgi_alani": 1})

#her belgeyi döngüye alır ve ilgi_alani alanını çıkarır.
for veritabaniiBelgesii in veritabaniiNesnesii:
    ilgi_alani = veritabaniiBelgesii['ilgi_alani']
    # İlgili alanları vektörlere dönüştürmek için Scibert kullanılır
    vektorrlerr = []  # Vektörleri tutmak için boş bir liste
    for ilgiiAlanii in ilgi_alani:
        inputs = tokenizer(ilgiiAlanii, return_tensors="pt")  # Metni tokenlere dönüştür
        # Hesaplamalar sırasında gradyan hesaplamasını devre dışı bırak
        with torch.no_grad():
            outputs = modeell(**inputs)  # Modelden çıktıları al
        vektorr = outputs.last_hidden_state.mean(dim=1).squeeze()  # Son gizli durumun ortalamasını al
        vektorrlerr.append(vektorr.tolist())   # Vektörü listeye ekle

    # Vektörlerin ortalamasını al
    if vektorrlerr:
        # Vektörlerin ortalamasını hesapla ve listeye çevir
        vektor_ortalamasi = torch.tensor(vektorrlerr).mean(dim=0).tolist()

        # Vektörü konsola yazdır
        print("ilgiiAlanii:", ilgi_alani)
        print("vektorr ortalamasii:", vektor_ortalamasi)

        # Vektörü MongoDB'ye kaydet
        vektorVerilerii = {'ilgi_alani': ilgi_alani, 'vektor_ortalamasi': vektor_ortalamasi}
        veriitabanii['ilgivektor'].insert_one(vektorVerilerii)
