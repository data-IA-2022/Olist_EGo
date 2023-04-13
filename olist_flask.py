from flask import Flask, jsonify, render_template, request, redirect, url_for, Response
from olist_model import *
from sqlalchemy.orm import Session
import yaml, os
from sqlalchemy import create_engine, text

app = Flask(__name__)
secret="ee55f77145dc4e62b3d480efbdec7589" # Clé d'accès à l'API - sécurité
'''
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
OLIST=config['olist_writer']
'''
OLIST=os.environ['OLIST'] # Variable d'environnement
print('OLIST=', OLIST)
engine = create_engine(OLIST)
print(engine)


@app.route("/")
def hello_world():
    with Session(engine) as session:
        it = session.query(ProductCategory).all()
    return render_template('olist_trad.html', it=it, key=secret)


@app.route("/api/categories", methods=['GET'])
def cat_list():
    # Vérification que la requète est authentifiée
    key=''
    if 'key' in request.form:
        key=request.form['key']
    if 'Subscription-Key' in request.headers:
        key=request.headers['Subscription-Key']
    if key != secret:
        return Response('Pas OK', 401)
    # Récupère la liste des ProductCategory
    with Session(engine) as session:
        it = session.query(ProductCategory).all()
    #print(it)
    return jsonify([pc.to_json() for pc in it]) # Retourne une liste JSON

@app.route("/api/category", methods=['POST'])
def cat_update():
    # Vérification que la requête est authentifiée
    key=''
    if 'key' in request.form:
        key=request.form['key']
    if 'Subscription-Key' in request.headers:
        key=request.headers['Subscription-Key']
    if key != secret:
        return Response('Pas OK', 401)
    # Récupère les paramètres 'cat' et 'fr' de la requète
    pk=request.form['cat']
    fr=request.form['fr']
    #print('HEADERS', request.headers)
    #print('cat_update: ', pk, fr)
    # Mise à jour de l'objet ProductCategory correspondant
    with Session(engine) as session:
        pc = session.query(ProductCategory).get(pk)
        pc.set_FR(fr)
        session.commit()
    return redirect(url_for('hello_world')) # Redirection vers chemin "/"
