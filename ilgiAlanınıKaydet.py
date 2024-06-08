#________________"ilgialani" koleksiyonu____________________
#"ilgiAlani.html" sayfasından alınan ilgi alanı bilgilerini alıp "ilgialani" koleksiyonuna kaydeder

from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB istemcisini oluşturun
clientiistemcii = MongoClient('mongodb://localhost:27017/')
veriitabanii = clientiistemcii['yazlab']  # Veritabanı adını yazın
koleksiiyonn = veriitabanii['ilgialani']  # Koleksiyon adını yazın


@app.route('/sec_ilgi_alani', methods=['POST'])
def sec_ilgi_alani():
    if request.method == 'POST':
        # HTML formundan gelen ilgi alanlarını alın
        ilgi_alani = request.form.getlist('ilgi_alani')

        # Alınan ilgi alanlarını MongoDB'ye kaydedin
        belgee = {'ilgi_alani': ilgi_alani}
        koleksiiyonn.insert_one(belgee)

        # Başarılı bir yanıt döndürün
        return jsonify({"message": "ilgi alanlari basariyla kaydedildi", "ilgi_alani": ilgi_alani})


if __name__ == '__main__':
    app.run(debug=True)
