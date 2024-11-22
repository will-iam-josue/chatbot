import requests

class SecureAPIClient:
    def __init__(self, base_url, token):
        self.session = requests.Session()
        self.base_url = "http://127.0.0.1:8000/ojo/api/"
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

    client = SecureAPIClient("", "8cdfbd8e20bd49ab0e5a271bde6101d48f0a5d9d")
    resultado_busqueda = client.post("busqueda/v1/", {
        "busqueda": "HECTOR ROSALES GARCIA",
        "req": "req"
    }) '''



    #print(resultado_busqueda)