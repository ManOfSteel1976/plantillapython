import sys
import os
import pymongo

from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# uri = 'mongodb+srv://canal:canal@cluster0.vodgj.mongodb.net/appsNube?retryWrites=true&w=majority'

uri = os.environ['MONGODB_URI']# + '?retryWrites=true&w=majority' 

client = pymongo.MongoClient(uri)

db = client.get_default_database()  

tesoros = db['tesoros']
encontrados = db['encontrados']
usuarios = db['usuarios']
ganador = db['ganador']
correo = "-"
numencontrados = 0

# Definicion de metodos para endpoints

@app.route('/', methods = ['GET', 'POST'])
def newUser():

    if request.method == 'GET' :
        return render_template('newuser.html')
    else:
        global correo
        correo = request.form['inputEmail']
        usr = {'email': correo, 
              'date': datetime.now()
             }
        
        if correo!="-" and usuarios.find({'email':correo}).count()==0 :
            usuarios.insert_one(usr)
        return redirect(url_for('showTesoros'))

@app.route('/tesoros', methods=['GET'])
def showTesoros():
    if ganador.count()>0 or numencontrados==tesoros.count() :
        return render_template('ganador.html', ganador = list(ganador.find()))
    else:
        return render_template('tesoros.html', tesoros = list(tesoros.find().sort('date',pymongo.ASCENDING)))    
    
@app.route('/new', methods = ['GET', 'POST'])
def newTesoro():

    if request.method == 'GET' :
        return render_template('new.html')
    else:
        tes = {'id': int(request.form['inputId']),
              'pista': request.form['inputPista'], 
              'date': datetime.now(),
             }
        tesoros.insert_one(tes)
        return redirect(url_for('showTesoros'))

@app.route('/newcaza', methods = ['GET', 'POST'])
def newCaza():
    encontrados.drop()
    ganador.drop()
    global numencontrados
    numencontrados=0
    return redirect(url_for('showTesoros'))


@app.route('/encontrado/<id>', methods = ['GET'])
def findTesoro(id):
    nuevo = {'id': id,
           'jugador': correo,
           'date': datetime.now(),
    }
    if correo!="-" and encontrados.find({'id':id,'jugador' : correo}).count()==0 :
        encontrados.insert_one(nuevo)
        global numencontrados
        numencontrados=numencontrados+1
    if numencontrados==tesoros.count() :
        ganador.insert_one({'ganador':correo})

    return redirect(url_for('showTesoros'))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App Engine
    # or Heroku, a webserver process such as Gunicorn will serve the app. In App
    # Engine, this can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
