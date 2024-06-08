from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def enn_yakiinn_bess_makalee_scibert(sorguuVektoruu, koleksiiyonn, toppBess=5):
    # En yakın belgelerin bilgilerini tutacak boş bir liste oluşturulur
    ennYakiinn_Makalelerr_Listesii = []
    
    # Koleksiyon içindeki her belge için dönülür
    for belgee in koleksiiyonn.find({}, {"_id": 0, "name": 1, "title": 1, "vektorler": 1}):
        # Belgenin vektörü alınır
        vekttorr = np.array(belgee.get('vektorler'))
        
        # Sorgu vektörü ile belge vektörü arasındaki benzerlik hesaplanır (kosinüs benzerliği)
        benzerliikk = cosine_similarity([sorguuVektoruu], [vekttorr])[0][0]
        
        # Belge adı, başlığı ve benzerlik skoru bir demet içinde listeye eklenir
        ennYakiinn_Makalelerr_Listesii.append((belgee.get('name'), belgee.get('title'), benzerliikk))

    # Benzerlik skoruna göre listeyi azalan şekilde sırala
    ennYakiinn_Makalelerr_Listesii.sort(key=lambda x: x[2], reverse=True)
    
    # En yakın 5 belgeyi döndür
    return ennYakiinn_Makalelerr_Listesii[:toppBess]


def enn_yakiinn_bess_makalee_fasttext(sorguuVektoruu, koleksiiyonn, toppBess=5):

    # En yakın belgelerin bilgilerini tutacak boş bir liste oluşturulur
    ennYakiinn_Makalelerr_Listesii = []

    # Koleksiyon içindeki her belge için dönülür
    for belgee in koleksiiyonn.find({}, {"_id": 0, "name": 1, "title": 1, "vektorler": 1}):

        # Belgenin vektörü alınır
        vekttorr = np.array(belgee.get('vektorler'))

        # Sorgu vektörü ile belge vektörü arasındaki benzerlik hesaplanır (kosinüs benzerliği)
        benzerliikk = cosine_similarity([sorguuVektoruu], [vekttorr])[0][0]

        # Belge adı, başlığı ve benzerlik skoru bir demet içinde listeye eklenir
        ennYakiinn_Makalelerr_Listesii.append((belgee.get('name'), belgee.get('title'), benzerliikk))

    # Benzerlik skoruna göre listeyi azalan şekilde sırala
    ennYakiinn_Makalelerr_Listesii.sort(key=lambda x: x[2], reverse=True)

    # En yakın 5 belgeyi döndür
    return ennYakiinn_Makalelerr_Listesii[:toppBess]

@app.route('/scibertt_dataa')
def scibertt_dataa():
    clientiistemcii = MongoClient('localhost', 27017)
    veriitabanii = clientiistemcii['yazlab']
    ilgivektor_koleksiyonuu = veriitabanii['ilgivektor']
    inspecvektor_koleksiyonuu = veriitabanii['vektorscibert']

    # İlgili vektör koleksiyonunda bulunan ilk belge (document) alınıyor
    sorguuBelgesii = ilgivektor_koleksiyonuu.find_one()

    # Bu belgeden 'vektor_ortalamasi' alanı alınarak numpy array'e dönüştürülüyor
    sorguuVektoruu = np.array(sorguuBelgesii.get('vektor_ortalamasi'))

    # 'enn_yakiinn_bess_makalee_scibert' fonksiyonu çağrılarak, sorgu vektörüne en yakın beş makale bulunuyor
    ennYakiinn_Makalelerr_Listesii = enn_yakiinn_bess_makalee_scibert(sorguuVektoruu, inspecvektor_koleksiyonuu)

    # En yakın beş makalenin listesi JSON formatında döndürülüyor
    return jsonify(ennYakiinn_Makalelerr_Listesii)

@app.route('/fasttextt_dataa')
def fasttextt_dataa():
    clientiistemcii = MongoClient('localhost', 27017)
    veriitabanii = clientiistemcii['yazlab']
    ilgivektorfast_koleksiyonuu = veriitabanii['ilgivektorfast']
    vektorfast_koleksiyonuu = veriitabanii['vektorfasttext']

    # İlgili vektör koleksiyonunda bulunan ilk belge (document) alınıyor
    sorguuBelgesii = ilgivektorfast_koleksiyonuu.find_one()

    # Bu belgeden 'vektor_ortalamasi' alanı alınarak numpy array'e dönüştürülüyor
    sorguuVektoruu = np.array(sorguuBelgesii.get('vektor_ortalamasi'))

    # 'enn_yakiinn_bess_makalee_fasttext' fonksiyonu çağrılarak, sorgu vektörüne en yakın beş makale bulunuyor
    ennYakiinn_Makalelerr_Listesii = enn_yakiinn_bess_makalee_fasttext(sorguuVektoruu, vektorfast_koleksiyonuu)

    # En yakın beş makalenin listesi JSON formatında döndürülüyor
    return jsonify(ennYakiinn_Makalelerr_Listesii)

clientiistemcii = MongoClient('mongodb://localhost:27017/')  
veriitabanii = clientiistemcii['yazlab']  


@app.route('/makalee_detaylarii')
def get_article_details():
    belgeeAdii = request.args.get('belgeeİsmii')

    # İlgili makaleyi veritabanından bul
    makaalee = veriitabanii['inspec'].find_one({'name': belgeeAdii}, {'_id': 0, 'name': 1, 'keys': 1, 'abstract': 1})

    # Makale bulunduysa
    if makaalee:
        # Makale detaylarını konsola yazdırır
        print('Makale Detayları:', makaalee)  # Makaleyi konsola yazdır

        # Anahtar bilgilerini \t karakterine göre ayırarak listeye dönüştür
        anahtarKelimelerr_listesii = makaalee.get('keys', '').split('\t')

        # 'makaleDetaylari.html' adlı HTML şablonunu, makale detayları ve anahtar kelimeler listesi ile render eder
        rendered_template = render_template('makaleDetaylari.html', makaalee=makaalee, anahtarKelimelerr_listesii=anahtarKelimelerr_listesii)

        # SciBERT vektörünü bul
        scibertt_vektorr_belgesii = veriitabanii['vektorscibert'].find_one({'name': belgeeAdii}, {'_id': 0, 'vektorler': 1})
        if scibertt_vektorr_belgesii:
            # Vektörü numpy array'e dönüştürür
            scibertt_vektorr = np.array(scibertt_vektorr_belgesii.get('vektorler'))

            # SciBERT vektor_ortalamasi güncelleme
            ilgivektor_koleksiyonuu = veriitabanii['ilgivektor']
            ilgivektorBelgesii = ilgivektor_koleksiyonuu.find_one()
            if ilgivektorBelgesii:

                # Eski vektör ortalamasını numpy array'e dönüştürür
                eskii_vektorr_ortalamasii = np.array(ilgivektorBelgesii['vektor_ortalamasi'])

                # Yeni vektör ortalamasını hesaplar (eski ve yeni vektörlerin ortalaması)
                yenii_vektorr_ortalamasii = (eskii_vektorr_ortalamasii + scibertt_vektorr) / 2

                # 'ilgivektor' koleksiyonundaki belgeyi günceller, yeni vektör ortalamasını set eder
                ilgivektor_koleksiyonuu.update_one({}, {'$set': {'vektor_ortalamasi': yenii_vektorr_ortalamasii.tolist()}})
            else:
                # İlgili vektör belgesi yoksa, yeni bir belge oluşturur ve vektör ortalamasını set eder
                ilgivektor_koleksiyonuu.insert_one({'vektor_ortalamasi': scibertt_vektorr.tolist()})

        # FastText vektörünü bul
        fasttextt_vektorr_belgesii = veriitabanii['vektorfasttext'].find_one({'name': belgeeAdii}, {'_id': 0, 'vektorler': 1})
        if fasttextt_vektorr_belgesii:
            fasttextt_vektorr = np.array(fasttextt_vektorr_belgesii.get('vektorler'))

            # FastText vektor_ortalamasi güncelleme
            ilgivektorfast_koleksiyonuu = veriitabanii['ilgivektorfast']
            ilgivektorfastBelgesii = ilgivektorfast_koleksiyonuu.find_one()
            if ilgivektorfastBelgesii:
                # Eski vektör ortalamasını numpy array'e dönüştürür
                eskii_vektorr_ortalamasii = np.array(ilgivektorfastBelgesii['vektor_ortalamasi'])

                # Yeni vektör ortalamasını hesaplar (eski ve yeni vektörlerin ortalaması)
                yenii_vektorr_ortalamasii = (eskii_vektorr_ortalamasii + fasttextt_vektorr) / 2

                # 'ilgivektorfast' koleksiyonundaki belgeyi günceller, yeni vektör ortalamasını set eder
                ilgivektorfast_koleksiyonuu.update_one({}, {'$set': {'vektor_ortalamasi': yenii_vektorr_ortalamasii.tolist()}})
            else:

                # İlgili vektör belgesi yoksa, yeni bir belge oluşturur ve vektör ortalamasını set eder
                ilgivektorfast_koleksiyonuu.insert_one({'vektor_ortalamasi': fasttextt_vektorr.tolist()})

        return rendered_template  # Render edilmiş HTML şablonunu döndür
    else:
        print('Makale bulunamadı')  # Hata durumunda konsola mesaj yazdır
        return jsonify({'error': 'Makale bulunamadı'}), 404


# TP ve FP değerlerini hesaplamak için sayaçlar
truee_pozitiff_scibert = 0
falsee_pozitiff_scibert = 0
truee_pozitiff_fasttext = 0
falsee_pozitiff_fasttext = 0
toplamm_truee_pozitiff = 0
toplamm_falsee_pozitiff = 0
toplamm_geriDonuslerr = 0

@app.route('/guncellee', methods=['POST'])
def guncellee():
    global truee_pozitiff_scibert, falsee_pozitiff_scibert, truee_pozitiff_fasttext, falsee_pozitiff_fasttext, toplamm_truee_pozitiff, toplamm_falsee_pozitiff, toplamm_geriDonuslerr


    # İstekten JSON verisini alır
    verii = request.json
    belgee_ismii = verii.get('belgee_ismii')
    geriiBildirimm = verii.get('geriiBildirimm')  # 'uygun' veya 'uygun değil'
    modell_turuu = verii.get('modell_turuu')  # 'scibert' veya 'fasttext'

    clientiistemcii = MongoClient('localhost', 27017)
    veriitabanii = clientiistemcii['yazlab']

    # Eğer geri bildirim 'uygun' ise
    if geriiBildirimm == 'uygun':

        # Kaynak ve hedef koleksiyon adlarını belirler
        kaynakk_koleksiyonnlarii_adlarii = ['vektorscibert', 'vektorfasttext']
        hedeff_koleksiyonnlarii_adlarii = ['ilgivektor', 'ilgivektorfast']

        # Her bir kaynak ve hedef koleksiyon çifti için
        for kaynakk_koleksiyonuu_adii, hedeff_koleksiyonuu_adii in zip(kaynakk_koleksiyonnlarii_adlarii, hedeff_koleksiyonnlarii_adlarii):
            kaynakk_koleksiyonuu = veriitabanii[kaynakk_koleksiyonuu_adii]   # Kaynak koleksiyonu seçer
            hedeff_koleksiyonuu = veriitabanii[hedeff_koleksiyonuu_adii]  # Hedef koleksiyonu seçer
            belgee = kaynakk_koleksiyonuu.find_one({'name': belgee_ismii})   # Kaynak koleksiyondan belgeyi bulur
            if belgee:
                # Belgeden vektörleri numpy array'e dönüştürür
                vektorlerr_belgee = np.array(belgee.get('vektorler'))

                # Hedef koleksiyondan herhangi bir belgeyi bulur
                hedeff_belgee = hedeff_koleksiyonuu.find_one()

                # Hedef belgeden vektör ortalamasını alır
                hedeff_vektoruu = np.array(hedeff_belgee.get('vektor_ortalamasi'))

                # Yeni vektör ortalamasını hesaplar
                yenii_vektorr_ortalamasii = (hedeff_vektoruu + vektorlerr_belgee) / 2

                # Yeni vektör ortalamasını listeye dönüştürür
                yenii_ortalmaaVektorr_listesii = yenii_vektorr_ortalamasii.tolist()

                # Hedef koleksiyonunu günceller
                hedeff_koleksiyonuu.update_one({}, {'$set': {'vektor_ortalamasi': yenii_ortalmaaVektorr_listesii}})

        # Model türüne göre true pozitif sayısını arttırır
        if modell_turuu == 'scibert':
            truee_pozitiff_scibert += 1
        elif modell_turuu == 'fasttext':
            truee_pozitiff_fasttext += 1
        toplamm_truee_pozitiff += 1

    elif geriiBildirimm == 'uygun değil':
        kaynakk_koleksiyonnlarii_adlarii = ['vektorscibert', 'vektorfasttext']
        hedeff_koleksiyonnlarii_adlarii = ['ilgivektor', 'ilgivektorfast']
        for kaynakk_koleksiyonuu_adii, hedeff_koleksiyonuu_adii in zip(kaynakk_koleksiyonnlarii_adlarii, hedeff_koleksiyonnlarii_adlarii):
            kaynakk_koleksiyonuu = veriitabanii[kaynakk_koleksiyonuu_adii]
            hedeff_koleksiyonuu = veriitabanii[hedeff_koleksiyonuu_adii]
            belgee = kaynakk_koleksiyonuu.find_one({'name': belgee_ismii})
            if belgee:
                # Belgeden vektörleri numpy array'e dönüştürür
                vektorlerr_belgee = np.array(belgee.get('vektorler'))

                # Hedef koleksiyondan herhangi bir belgeyi bulur
                hedeff_belgee = hedeff_koleksiyonuu.find_one()

                # Hedef belgeden vektör ortalamasını alır
                hedeff_vektoruu = np.array(hedeff_belgee.get('vektor_ortalamasi'))

                # Yeni vektör ortalamasını hesaplar
                yenii_vektorr_ortalamasii = hedeff_vektoruu - (vektorlerr_belgee / 2)

                # Yeni vektör ortalamasını listeye dönüştürür
                yenii_ortalmaaVektorr_listesii = yenii_vektorr_ortalamasii.tolist()

                # Hedef koleksiyonunu günceller
                hedeff_koleksiyonuu.update_one({}, {'$set': {'vektor_ortalamasi': yenii_ortalmaaVektorr_listesii}})

        # Model türüne göre true pozitif sayısını arttırır
        if modell_turuu == 'scibert':
            falsee_pozitiff_scibert += 1
        elif modell_turuu == 'fasttext':
            falsee_pozitiff_fasttext += 1
        toplamm_falsee_pozitiff += 1

    toplamm_geriDonuslerr += 1

    # Precision değerlerini hesapla
    precisionn_degerii__scibert = truee_pozitiff_scibert / (truee_pozitiff_scibert + falsee_pozitiff_scibert) if truee_pozitiff_scibert + falsee_pozitiff_scibert > 0 else 0
    precisionn_degerii__fasttext = truee_pozitiff_fasttext / (truee_pozitiff_fasttext + falsee_pozitiff_fasttext) if truee_pozitiff_fasttext + falsee_pozitiff_fasttext > 0 else 0
    precisionn_degerii__toplamm = toplamm_truee_pozitiff / (toplamm_truee_pozitiff + toplamm_falsee_pozitiff) if toplamm_truee_pozitiff + toplamm_falsee_pozitiff > 0 else 0

    # İşlem tamamlandıktan sonra geri bildirimi konsola yazdır
    print(f"Document: {belgee_ismii}, Feedback: {geriiBildirimm}, Model: {modell_turuu}")
    print("Total Feedbacks:", toplamm_geriDonuslerr)
    print("SciBERT Precision:", precisionn_degerii__scibert)
    print("FastText Precision:", precisionn_degerii__fasttext)
    print("Total Precision:", precisionn_degerii__toplamm)

    # Eğer tüm geri bildirimler tamamlandıysa, sayaçları sıfırla
    if toplamm_geriDonuslerr == 10:
        truee_pozitiff_scibert = 0
        falsee_pozitiff_scibert = 0
        truee_pozitiff_fasttext = 0
        falsee_pozitiff_fasttext = 0
        toplamm_truee_pozitiff = 0
        toplamm_falsee_pozitiff = 0
        toplamm_geriDonuslerr = 0

    # Yanıt olarak JSON formatında güncellemenin başarılı olduğunu ve precision değerlerini döner
    return jsonify({'message': 'Update successful', 'precisionn_degerii__scibert': precisionn_degerii__scibert, 'precisionn_degerii__fasttext': precisionn_degerii__fasttext, 'precisionn_degerii__toplamm': precisionn_degerii__toplamm})


@app.route('/aramaa', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    clientiistemcii = MongoClient('localhost', 27017)
    veriitabanii = clientiistemcii['yazlab']

    aramascibert_koleksiyonuu = veriitabanii['aramascibert']
    aramafasttext_koleksiyonuu = veriitabanii['aramafasttext']
    ilgivektor_koleksiyonuu = veriitabanii['ilgivektor']
    ilgivektorfast_koleksiyonuu = veriitabanii['ilgivektorfast']

    # SciBERT koleksiyonunda arama
    scibertt_vektorr = aramascibert_koleksiyonuu.find_one({'kelime': keyword}, {'_id': 0, 'vektor': 1})
    if scibertt_vektorr:
        # Var olan belgeyi güncelle ve içine ekle
        ilgivektorBelgesii = ilgivektor_koleksiyonuu.find_one({})
        if ilgivektorBelgesii:
            yenii_vektorr_ortalamasii = scibertt_vektorr['vektor']  # Yeni vektörü alır
            eskii_vektorr_ortalamasii = ilgivektorBelgesii['vektor_ortalamasi']  # Eski vektör ortalamasını alır

            # Yeni ve eski vektörlerin ortalamasını hesaplar
            guncellenenn_ortalamaVektoruu = [(x + y) / 2 for x, y in zip(yenii_vektorr_ortalamasii, eskii_vektorr_ortalamasii)]

            # Güncellenmiş ortalama vektörü veritabanına yazar
            ilgivektor_koleksiyonuu.update_one({}, {'$set': {'vektor_ortalamasi': guncellenenn_ortalamaVektoruu}})
        else:

            # Eğer ilgili belge bulunamazsa, yeni bir belge ekler
            ilgivektor_koleksiyonuu.insert_one({'vektor_ortalamasi': scibertt_vektorr['vektor']})

    # FastText koleksiyonunda arama
    fasttextt_vektorr = aramafasttext_koleksiyonuu.find_one({'kelime': keyword}, {'_id': 0, 'vektor': 1})
    if fasttextt_vektorr:
        # Var olan belgeyi güncelle ve içine ekle
        ilgivektorfastBelgesii = ilgivektorfast_koleksiyonuu.find_one({})
        if ilgivektorfastBelgesii:
            yenii_vektorr_ortalamasii = fasttextt_vektorr['vektor']  # Yeni vektörü alır
            eskii_vektorr_ortalamasii = ilgivektorfastBelgesii['vektor_ortalamasi']  # Eski vektör ortalamasını alır

            # Yeni ve eski vektörlerin ortalamasını hesaplar
            guncellenenn_ortalamaVektoruu = [(x + y) / 2 for x, y in zip(yenii_vektorr_ortalamasii, eskii_vektorr_ortalamasii)]

            # Güncellenmiş ortalama vektörü veritabanına yazar
            ilgivektorfast_koleksiyonuu.update_one({}, {'$set': {'vektor_ortalamasi': guncellenenn_ortalamaVektoruu}})
        else:

            # Eğer ilgili belge bulunamazsa, yeni bir belge ekler
            ilgivektorfast_koleksiyonuu.insert_one({'vektor_ortalamasi': fasttextt_vektorr['vektor']})

    return jsonify({'message': 'Vectors inserted/updated successfully'})


@app.route('/')
def index():
    return render_template('benzerlik.html')

if __name__ == "__main__":
    app.run(debug=True)
