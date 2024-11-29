import requests

class SecureAPIClient:
    def __init__(self, base_url, token):
        self.session = requests.Session()
        self.base_url = base_url
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Token {token}"
        })

    def post(self, endpoint, payload):
        try:
            url = f"{endpoint}"
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud POST: {e}", flush=True)
            return None

def consulta_api(url, datos):
    print(f"Consultando {url} con datos {datos}...", flush=True)
    try:
        client = SecureAPIClient(base_url="", token="8cdfbd8e20bd49ab0e5a271bde6101d48f0a5d9d")
        resultado_busqueda = client.post(url, datos)
        return resultado_busqueda
    except requests.exceptions.RequestException as e:
        return f"Error al consultar {url}: {e}"

def respuesta(resultado_busqueda):
    cadena = ""

    if resultado_busqueda and "resultadosResmor" in resultado_busqueda:
        cadena = cadena + "*SIDIP*\n"
        resmor = resultado_busqueda['resultadosResmor']
        if resmor:
            for obj in resmor:
                cadena = cadena + "*NOMBRE*: " + str(obj['nombre']) + " " + str(obj['apellido_paterno']) + " " +str(obj['apellido_materno'])+ "\n"
                cadena = cadena + "*FECHA DE NACIMIENTO*: " + str(obj['fecha_nacimiento']) + "\n"
                cadena = cadena + "*DEPENDENCIA*: " + str(obj['dependencia']) + "\n"
                cadena = cadena + "*INSTITUCION*: " + str(obj['institucion']) + "\n\n"
        else:
            cadena=cadena+"SIN INFORMACIÓN\n\n"

    if resultado_busqueda and "resultados089" in resultado_busqueda:

        cadena = cadena+"*089*\n"

        resultados089 = resultado_busqueda['resultados089']
        cantidad = len(resultados089)
        if resultados089:
            if len(resultados089) < 5:
                for obj in resultados089:
                    cadena = cadena + "*FOLIO*:" + str(obj['folio']) + "\n\n"
            else:
                for i, obj in enumerate(resultados089):
                    if i >= 6:
                        break
                    cadena = cadena + "*FOLIO*:" + str(obj['folio']) + "\n\n"
                cadena = cadena + "NO ES POSIBLE MOSTRAR LOS " + str(cantidad) + "REGISTROS DEL 089"
        else:
            cadena=cadena+"SIN INFORMACIÓN\n\n"

    if resultado_busqueda and "resultados911" in resultado_busqueda:
        cadena = cadena + "*911*\n"
        resultados911 = resultado_busqueda['resultados911']
        cantidad = len(resultados911)
        if resultados911:
            if len(resultados911) < 5:
                for obj in resultados911:
                    cadena = cadena + "*FOLIO*:" + str(obj['folio']) + "\n\n"
            else:
                for i, obj in enumerate(resultados911):
                    if i >= 6:
                        break
                    cadena = cadena + "*FOLIO*:" + str(obj['folio']) + "\n\n"
                cadena = cadena + "NO ES POSIBLE MOSTRAR LOS " + str(cantidad) + "REGISTROS DEL 911"
        else:
            cadena=cadena+"SIN INFORMACIÓN\n\n"


    if resultado_busqueda and "resultados_ine3" in resultado_busqueda:
        cadena = cadena + "*INE*\n"
        resultadosINE = resultado_busqueda['resultados_ine3']
        cantidad = len(resultadosINE)
        if resultadosINE:
            if cantidad < 5:
                for obj in resultadosINE:
                    cadena = cadena + "NOMBRE:" + str(obj['nombre']) + " " + str(obj['paterno']) + " " + str(obj['materno']) +"\n"
                    cadena = cadena + "ELECTOR:" + str(obj['cve']) +"\n"
                    cadena = cadena + "CURP:" + str(obj['curp']) +"\n"
                    cadena = cadena + "CALLE:" + str(obj['calle']) +"\n"
                    if obj['inte']:
                        no_int = obj['inte']
                    else:
                        no_int = ""
                    cadena = cadena + "NO. INT.:" + str(no_int) +"\n"
                    if obj['ext']:
                        no_ext = obj['ext']
                    else:
                        no_ext = ""
                    cadena = cadena + "NO. EXT.:" + str(no_ext) +"\n"
                    cadena = cadena + "COLONIA:" + str(obj['colonia']) +"\n"
                    cadena = cadena + "CÓDIGO POSTAL:" + str(obj['cp']) +"\n\n"
            else:
                for i, obj in enumerate(resultadosINE):
                    if i>=6:
                        break
                    cadena = cadena + "NOMBRE:" + str(obj['nombre']) + " " + str(obj['paterno']) + " " + str(obj['materno']) +"\n"
                    cadena = cadena + "ELECTOR:" + str(obj['cve']) +"\n"
                    cadena = cadena + "CURP:" + str(obj['curp']) +"\n"
                    cadena = cadena + "CALLE:" + str(obj['calle']) +"\n"
                    if obj['inte']:
                        no_int = obj['inte']
                    else:
                        no_int = ""
                    cadena = cadena + "NO. INT.:" + str(no_int) +"\n"
                    if obj['ext']:
                        no_ext = obj['ext']
                    else:
                        no_ext = ""
                    cadena = cadena + "NO. EXT.:" + str(no_ext) +"\n"
                    cadena = cadena + "COLONIA:" + str(obj['colonia']) +"\n"
                    cadena = cadena + "CÓDIGO POSTAL:" + str(obj['cp']) +"\n\n"
                cadena = cadena + "NO ES POSIBLE MOSTRAR LOS " + str(cantidad) + "REGISTROS DEL INE"
        else:
            cadena=cadena+"SIN INFORMACIÓN\n\n"
    return cadena