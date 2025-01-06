import requests
from orden_produccion import OrdenProduccion
from requests.exceptions import ConnectionError, HTTPError
from datetime import datetime
from dateutil import parser
from concurrent.futures import ThreadPoolExecutor

from palet import Palet

class DjangoManager:
    def __init__(self):
        # self.base_url = "http://192.168.31.155:8000"
        self.base_url = "http://192.168.100.112:8001"
        # self.base_url = "http://127.0.0.1:8000"
        self.token_url = f"{self.base_url}/api/token/"
        # self.username= "jaime"
        # self.password= "InbalnoSismode0117"
        self.username= "jaimeb"
        self.password= "Benalcazar@1224"
        self.error_django = False
        self.refresh_url = f"{self.token_url}/refresh/"
        self.access_token = ""
        self.refresh_token = ""
        self.authenticate()
        self.productos =[]
        self.executor = ThreadPoolExecutor(max_workers=5) 
        # Inicializar gestores
        
        # self.api_manager = ApiManager(BASE_URL, auth_manager)


    def _send_request(self, method, url, data=None, json=None, headers=None):
        if not headers:
            headers = {'Authorization': f'Bearer {self.access_token}'}
        try:
            if method.upper() == "POST":
                return requests.post(url, data=data, json=json, headers=headers)
            elif method.upper() == "PUT":
                return requests.put(url,  json=json, headers=headers)
            elif method.upper() == "GET":
                return requests.get(url, headers=headers)
            elif method.upper() == "PATCH":
                return requests.patch(url, json=data, headers=headers)  
            else:
                raise ValueError("Unsupported HTTP method.")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
    def authenticate(self):
        try:
            response = self._send_request("POST", self.token_url, data={'username': self.username, 'password': self.password})
            if response.status_code == 200:
                tokens = response.json()
                self.access_token, self.refresh_token = tokens['access'], tokens['refresh']
            else:
                print(f"Error en la autenticación: {response.status_code}, {response.text}")
        except Exception as e:
            self.error_django = True
            print(f"Error al autenticar: {e}")

            
        

    def get_access_token(self):
        return self.access_token
    
    
    
    def _convertir_a_orden(self, data):
        try:
            fecha_creacion_str = data['fecha_creacion']
            data['fecha_creacion'] = parser.parse(fecha_creacion_str)
            return OrdenProduccion(**data)
        except Exception as e:
            print(f"Error al obtener orden produccion l1 {e}")
            return OrdenProduccion.default()
    
    def _convertir_a_palet(self, data):
    
        return Palet(**data)
        

    def get_current_date(self):
        now = datetime.now()
        now_t =  now.strftime('%y-%m-%d')
        try:
            url = f"{self.base_url}/api/current-date/"
            response = self._send_request("GET", url)
            if response.status_code == 200:
                now_t = response.json()['current_date']
            
        except Exception as e:
            print(f"Error al obtener fecha: {e}")
        finally:
            return now_t
        
    def set_orden_produccion(self, orden: OrdenProduccion):
        url = f"{self.base_url}/api/ordenproduccion/"
        response = self._send_request("POST", url, json=orden.to_dict())
        return self._convertir_a_orden(response.json())
    
    def get_orden_produccion(self, id):
        url = f"{self.base_url}/api/ordenproduccion/{id}/"
        response = self._send_request("GET", url)
        return self._convertir_a_orden(response.json())
    

    def get_orden_produccion_continuar(self, orden: OrdenProduccion):
        url = f"{self.base_url}/api/ordenproduccion/?turno={orden.turno}&lote_completo={orden.lote_completo}&id_producto={orden.id_producto}&linea={orden.linea}&ordering=-id"
        response = self._send_request("GET", url)
        if response.status_code == 200:
            res = response.json()
            if len(res) >0:
                return [self._convertir_a_orden(res[0])]
           
        return []
    

    def update_orden_produccion(self, id, fecha_final, fin_contador_general, fin_contador, estado):
        url = f"{self.base_url}/api/ordenproduccion/{id}/"
        data = {
        "estado":estado,
        "fecha_final": fecha_final.isoformat(),
        "fin_contador_general": fin_contador_general,
        "fin_contador": fin_contador,
        }

        response = self._send_request("PATCH", url, data=data)
        return self._convertir_a_orden(response.json())
    
    def update_counter_orden_produccion(self, id,fin_contador_general,  fin_contador):
        url = f"{self.base_url}/api/ordenproduccion/{id}/"
        data = {
        "fin_contador_general": fin_contador_general,
        "fin_contador": fin_contador,
        }

        response = self._send_request("PATCH", url, data=data)
        return self._convertir_a_orden(response.json())
    
    def update_counter_orden_produccion_async(self, id, fin_contador_general, fin_contador):
        self.executor.submit(self.update_counter_orden_produccion, id, fin_contador_general, fin_contador)
        print("update_counter_orden_produccion_async", fin_contador_general)

    

    def set_palet(self, palet: Palet):
        url = f"{self.base_url}/api/palets/"
        try:
            response = self._send_request("POST", url, json=palet.to_dict())
            if response.ok:
                return self._convertir_a_palet(response.json())
            else:
                if response.status_code == 400 and 'sscc' in response.json() and 'already exists' in response.json()['sscc'][0]:
                    print("Error: Un palet con este SSCC ya existe.")
                    return "SSCC_EXISTS"
                else:
                    print(f"Error en la respuesta: Código de estado {response.status_code}, Respuesta: {response.text}")
                    return None
        except Exception as e:
            print(f"Error al enviar palet: {e}")
            return None
        
    def get_palets_pendientes_mas_bajos(self, linea: str):
        url = f"{self.base_url}/api/palets/?linea={linea}&subido_a_firebase=False&ordering=id&limit=5"
        try:
            response = self._send_request("GET", url)
            if response.status_code == 200:
                palets_data = response.json()
                if len(palets_data) > 0:
                    return [self._convertir_a_palet(palet) for palet in palets_data]
                else:
                    print("No pending palets found with the specified conditions.")
                    return []
            else:
                print(f"Error in response: Status code {response.status_code}, Response: {response.text}")
                return []
        except Exception as e:
            print(f"Error while fetching pending palets: {e}")
            return []
        

    def get_palets_pendientes_mas_bajos_gema(self, linea: str):
        url = f"{self.base_url}/api/palets/?linea={linea}&subido_a_vitacontrol=False&ordering=id&limit=5"
        try:
            response = self._send_request("GET", url)
            if response.status_code == 200:
                palets_data = response.json()
                if len(palets_data) > 0:
                    return [self._convertir_a_palet(palet) for palet in palets_data]
                else:
                    print("No pending palets found with the specified conditions.")
                    return []
            else:
                print(f"Error in response: Status code {response.status_code}, Response: {response.text}")
                return []
        except Exception as e:
            print(f"Error while fetching pending palets: {e}")
            return []


        
    def update_palet_firebase(self, id, ref_firebase):
        url = f"{self.base_url}/api/palets/{id}/"
        data = {
        "subido_a_firebase":True,
        "id_fb": ref_firebase,

        }
        response = self._send_request("PATCH", url, data=data)
        return self._convertir_a_palet(response.json())
    

    def update_palet_gema(self, id, id_gema):
        url = f"{self.base_url}/api/palets/{id}/"
        data = {
        "subido_a_vitacontrol":True,
        "id_vitacontrol": id_gema,

        }
        response = self._send_request("PATCH", url, data=data)
        return self._convertir_a_palet(response.json())
    
    def update_palet_vitacontrol(self, id ):
        url = f"{self.base_url}/api/palets/{id}/"
        data = {
        "subido_a_vitacontrol":True,
        }
        response = self._send_request("PATCH", url, data=data)
        return self._convertir_a_palet(response.json())

        






