import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, jsonify
from flask import make_response
from flask import request


 
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
 
@app.route('/api/universite/<path:page_index>', methods=['GET'])
def sonuc(page_index):
    url = "https://www.tercihrobotu.com.tr/bolumler/?Devlet=True&Vakif=True&Yurtdisi=False&Lisans=True&Onlisans=True&NormalOgretim=True&IkinciOgretim=True&Ucretsiz=True&Ucretli=True&TamBurslu=True&Burslu75=True&Burslu50=True&Burslu25=True&PageIndex="+ str(page_index)
    req = requests.get(url)
    context = req.content
    soup = BeautifulSoup(context, "lxml")
    str(soup).replace("</br>", "")
    item = []
    for i in soup.find_all("td",{"class": "Text"}):
        data = {}
        data['meslek'] = i.a.strong.find_all(text =re.compile('[a-zA-Z.]*'))[0].strip()
        #print("bolum: ", i.strong.text)
        post_content = i.a.find_all(text =re.compile('\s{1,}.{1,}$'))
        last_div = None
        for last_div in post_content:pass
        if last_div:
            content = last_div.strip()
            data['fakulte'] =  content
        data['uni_adi'] =  i.a.find_all(text =re.compile('\n.{1,}[a-zA-Z]'))[0].strip()
        item.append(data)
    return jsonify({'universiteler': item})
    
page = 0
while True:
    try:
        page += 1
        sonuc(page)
    except Exception as ex:
        print(ex)
        print("probably last page:", page)
        break # exit `while` loop

if __name__ == '__main__':
    app.run(debug=True)#!flask/bin/python
    app.config['JSON_AS_ASCII'] = False
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'HTTP 404 Error': 'The content you looks for does not exist. Please check your request.'}), 404)
