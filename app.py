import json
import logging
import http.client
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from api import SecureAPIClient, consulta_api, respuesta
from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
white_list = ['525650835953','527777877176','527775006263', '527771495695', '522291881930']

user_states = {}  # Diccionario: {numero: estado}
auth = 'Bearer EAAEe3rnxKxABO1r6it9z8PC1BZBGl9tEX88gasU7vPlmXin4bL9yrPjzNWLeq1wjjGuO8jGgyXSNPTliApNDvZBK8qOvR1BdNvtVbnSCdfDN6GZBF00GB1UQHSvLkOSxiK5GA9Cs4D6mdX9HMwmemkRPczY4aC9QAkrWAaCQjrNr3egZAEuIgi1W8w2ZCZBHo4AgZDZD'
# Lista de URLs a consultar
urls = [
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda/v1/',
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda2/v1/',
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda3/v1/',
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda4/v1/',
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda5/v1/',
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda6/v1/',
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda7/v1/',
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda8/v1/',
    'https://resmor.cesmorelos.gob.mx/ef/ojo/api/busqueda9/v1/'
]

logging.basicConfig(level=logging.DEBUG)
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

def menu(numero):
    connection = http.client.HTTPSConnection('graph.facebook.com')

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "*Hola 👋, ¿qué te gustaría hacer?*"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "cons_folio",
                            "title": "Consultar Folio"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "cons_nomb",
                            "title": "Busqueda nombre"
                        }
                    },
                ]
            }
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }

    data = json.dumps(data)

    if numero in white_list:
        connection.request("POST", '/v21.0/143633982157349/messages', data, headers)
        response = connection.getresponse()
        print(response.read().decode(), flush=True)
    connection.close()

def otra_consulta(numero):
    connection = http.client.HTTPSConnection('graph.facebook.com')

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "*¿Deseas realizar otra consulta?*"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "otra_si",
                            "title": "Si"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "otra_no",
                            "title": "No"
                        }
                    },
                ]
            }
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }

    data = json.dumps(data)

    if numero in white_list:
        connection.request("POST", '/v21.0/143633982157349/messages', data, headers)
        response = connection.getresponse()
        print(response.read().decode(), flush=True)
    connection.close()
    return jsonify({'message': 'EVENT_RECEIVED'})

def cons_folio911(folio, numero):
    print(folio, flush=True)
    print(numero, flush=True)
    datos = {
        "busqueda": folio,
        "req": "req"
    }
    rs = consulta_api('https://resmor.cesmorelos.gob.mx/ef/ojo/api/busquedafolio/911/', datos)
    print(rs, flush=True)
    texto = f'*Folio 911 - {folio}*\n'
    if rs and rs['resultadosFolio911']:
        for fol in rs['resultadosFolio911']:
            print(fol, flush=True)
            texto += f'*Folio:* {fol["Folio"]}\n*Municipio:* {fol["Municipio"]}\n*Fecha:* {fol["Fecha"]}\n*Incidente:* {fol["Tipo_incidente"]}'
    else:
        texto += '*NO SE ENCONTRO EL FOLIO FAVOR DE VERIFICARLO*'
    print(texto, flush=True)
    try:
        connection = http.client.HTTPSConnection('graph.facebook.com')
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": texto
            }
        }
            #Convertir el diccionario a formato json
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth
        }
        data = json.dumps(data)
        print(data, flush=True)
        if numero in white_list:
            connection.request("POST", '/v21.0/143633982157349/messages', data, headers)
            response = connection.getresponse()
            print(response.read().decode(), flush=True)
    except Exception as e:
        print(f"Error en {url}: {e}", flush=True)
    finally:
        connection.close()
    otra_consulta(numero)

def mensaje(numero, mensaje):
    print(numero, flush=True)
    print(mensaje, flush=True)
    try:
        connection = http.client.HTTPSConnection('graph.facebook.com')
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": mensaje
            }
        }
            #Convertir el diccionario a formato json
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth
        }
        data = json.dumps(data)
        
        if numero in white_list:
            connection.request("POST", '/v21.0/143633982157349/messages', data, headers)
            response = connection.getresponse()
        return jsonify({'message': 'EVENT_RECEIVED'})
    except Exception as e:
        print(f"Error en {url}: {e}", flush=True)
        return jsonify({'message': 'EVENT_RECEIVED'})
    finally:
        connection.close()
        return jsonify({'message': 'EVENT_RECEIVED'})

def respuestas(rs_id, numero):
    if rs_id == 'cons_folio':
        user_states[numero] = 'esperando_folio'
        mensaje(numero, '*Introduce el folio de 911 a consultar*')
    elif rs_id == 'cons_nomb':
        user_states[numero] = 'esperando_nombre'
        mensaje(numero, '*Introduce el nombre a buscar*')
    elif rs_id == 'otra_si':
        menu(numero)
    elif rs_id == 'otra_no':
        mensaje(numero, '*Gracias por utilizar el bot!...*')
        #enviar_mensaje(texto, numero)

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
            if 'type' in message:
                
                tipo = message['type']
                if tipo == 'interactive':
                    numero = message['from']
                    numero = f'{numero[0:2]}{numero[3:]}'
                    msg_type = message['interactive']['type']

                    if msg_type == 'button_reply':
                        res = message['interactive']['button_reply']['id']
                        print(res, flush=True)
                        respuestas(res, numero)
                    
                if 'text' in message:
                    numero = message['from']
                    numero = f'{numero[0:2]}{numero[3:]}'
                    texto = message['text']['body']
                    
                    estado = user_states.get(numero)
                    print(estado, flush=True)
                    if estado == 'esperando_nombre':
                        user_states.pop(numero, None)
                        enviar_mensaje(texto, numero)
                    elif estado == 'esperando_folio':
                        user_states.pop(numero, None)
                        cons_folio911(texto, numero)
                    elif texto.lower() in['hola', 'menu', 'inicio', 'empezar', 'buenas']:
                        menu(numero)
                    else:
                        enviar_mensaje(texto, numero)
                        
        return jsonify({'message': 'EVENT_RECEIVED'})
    except Exception as e:
        return json.dumps({'message': 'EVENT_RECEIVED'})

def enviar_mensaje(texto, numero):
    texto = texto.lower()
    # Datos comunes para todas las solicitudes
    datos = {
        "busqueda": texto,
        "req": "req"
    }
    # Crear un ejecutor de hilos
    with ThreadPoolExecutor() as executor:
        # Enviar las tareas al executor
        futures = {executor.submit(consulta_api, url, datos): url for url in urls}
        # Procesar las respuestas conforme estén listas
        for future in as_completed(futures):
            url = futures[future]
            connection = http.client.HTTPSConnection('graph.facebook.com')
            try:
                cadena = f"*{texto.upper()}:*\n\n"
                resultado_busqueda = future.result()
                if resultado_busqueda:
                    cadena += respuesta(resultado_busqueda)
                    data = {
                        "messaging_product": "whatsapp",    
                        "recipient_type": "individual",
                        "to": numero,
                        "type": "text",
                        "text": {
                            "preview_url": False,
                            "body": cadena
                        }
                    }
                    #Convertir el diccionario a formato json
                    data = json.dumps(data,)
                    
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': auth
                    }
                    if numero in white_list:
                        connection.request("POST", '/v21.0/143633982157349/messages', data, headers)
                        response = connection.getresponse()
            except Exception as e:
                print(f"Error en {url}: {e}", flush=True)
            finally:
                connection.close()
    otra_consulta(numero)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)