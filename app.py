import json
import http.client
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#Configuración de la Base de Datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///log.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Modelo para la tabla de Log
class Log(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now) 
    texto = db.Column(db.TEXT)

#Crea Tabla si no Existe
with app.app_context():
    db.create_all()

#Funcion para ordenar registros de fecha y hora
def ordenar_fecha_hora(reg):
    return sorted(reg, key=lambda x: x.fecha, reverse=True)

@app.route('/')
def home():
    #obtener todos los registros de la base de datos log
    reg = Log.query.all()
    order_reg = ordenar_fecha_hora(reg)
    return render_template('home.html', reg=order_reg)

log_msgs = []
#Funcion para agregar mensajes y guardar en el Log
def add_log_message(texto):
    log_msgs.append(texto)
    
    #Guarda el mensaje en la base de datos
    new_reg = Log(texto=texto)
    db.session.add(new_reg)
    db.session.commit()

#Token de verificacion para la configuracion
TOKEN_VERIFY = 'Shinnosuke_6654*'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        challenge = verify_token(request)
        return challenge
    elif request.method == 'POST':
        response = recibir_mensaje(request)
        return response

def verify_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_VERIFY:
        return challenge
    else:
        return  jsonify({'error': 'Token Invalido'}), 401

def recibir_mensaje(req):
    req = request.get_json()
    add_log_message(json.dumps(req, ensure_ascii=False)) #Guarda en el log el mensaje con los datos recibidos
    
    try:
        entry = req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        messages = value['messages']
        if messages:
            message = messages[0]
            
            if 'type' in messages:
                tipo = message['type']
                if tipo == 'interactive':
                    ...
                
                if 'text' in messages:
                    numero = message['from']
                    texto = messages['text']['body']
                    print(numero)
                enviar_mensaje(texto, numero)
    except Exception as e:
        return json.dumps({'message': 'EVENT_RECEIVED'})
    return jsonify({'message': 'EVENT_RECEIVED'})

def enviar_mensaje(texto, numero):
    texto = texto.lower()
    print(numero)
    if "hola" in texto:
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": nomber,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hola , como estas Bienvenido al chatbootsito.\n¿Que es lo que deseas hacer?\n 1) Una consulta\n2) Una busqueda"
            }
        }
    else:
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": nomber,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hola , para mas informacion envia un *Hola* nada más"
            }
        }

    #Convertir el diccionario a formato json
    data = json.dumps(data, ensure_ascii=False)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer EAAEe3rnxKxABO1r6it9z8PC1BZBGl9tEX88gasU7vPlmXin4bL9yrPjzNWLeq1wjjGuO8jGgyXSNPTliApNDvZBK8qOvR1BdNvtVbnSCdfDN6GZBF00GB1UQHSvLkOSxiK5GA9Cs4D6mdX9HMwmemkRPczY4aC9QAkrWAaCQjrNr3egZAEuIgi1W8w2ZCZBHo4AgZDZD'
    }
    
    connection = http.client.HTTPSConnection('graph.facebook.com')
    try:
        connection.request("POST", '/v21.0/143633982157349/messages', data, headers)
        response = connection.getresponse()
        print(response.status, response.reason)
    except:
        ...
    finally:
        connection.close()
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)