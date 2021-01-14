import sys
import os
import pymongo

from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# uri = 'mongodb+srv://canal:canal@cluster0.vodgj.mongodb.net/appsNube?retryWrites=true&w=majority'

uri = os.environ['MONGODB_URI'] + '?retryWrites=true&w=majority' 

client = pymongo.MongoClient(uri)

db = client.get_default_database()  

ads = db['ads']

# Definicion de metodos para endpoints

@app.route('/', methods=['GET'])
def showAds():
    
    return render_template('ads.html', ads = list(ads.find().sort('date',pymongo.DESCENDING)))
    
@app.route('/new', methods = ['GET', 'POST'])
def newAd():

    if request.method == 'GET' :
        return render_template('new.html')
    else:
        ad = {'author': request.form['inputAuthor'],
              'text': request.form['inputText'], 
              'priority': int(request.form['inputPriority']),
              'date': datetime.now()
             }
        ads.insert_one(ad)
        return redirect(url_for('showAds'))

@app.route('/edit/<_id>', methods = ['GET', 'POST'])
def editAd(_id):
    
    if request.method == 'GET' :
        ad = ads.find_one({'_id': ObjectId(_id)})
        return render_template('edit.html', ad = ad)
    else:
        ad = { 'author': request.form['inputAuthor'],
               'text': request.form['inputText'],
               'priority' : int(request.form['inputPriority'])
             }
        ads.update_one({'_id': ObjectId(_id) }, { '$set': ad })    
        return redirect(url_for('showAds'))

@app.route('/delete/<_id>', methods = ['GET'])
def deleteAd(_id):
    
    adds.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('showAds'))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App Engine
    # or Heroku, a webserver process such as Gunicorn will serve the app. In App
    # Engine, this can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
