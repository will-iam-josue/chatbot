import requests

class SecureAPIClient:
    def __init__(self, base_url, token):
        self.session = requests.Session()
        self.base_url = "https://resmor.cesmorelos.gob.mx/ef/ojo/api/"
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Token {token}"
        })
    
    def post(self, endpoint, payload):
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud POST: {e}")
            return None

# Uso
''' if __name__ == "__main__":

    client = SecureAPIClient("", "95eeed0496e5612455ef21a1cbfbcecd7989d3a7")
    resultado_busqueda = client.post("vista1/", {
        "busqueda": "HECTOR ROSALES GARCIA",
        "req": "req"
    })
    print("Resultado de la búsqueda:", resultado_busqueda) '''