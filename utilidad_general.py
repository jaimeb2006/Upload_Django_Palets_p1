from datetime import datetime
import socket
import time

from django_manager import DjangoManager
from firebase_manager import FirebaseManager
from opc_manager import OpcManager
from orden_produccion import OrdenProduccion
from palet import Palet


def subir_palet(orden_produccion: OrdenProduccion, numero_actual):
    palet = Palet.from_orden_produccion_to_palet(orden_produccion, numero_actual, False, False)
    result = UtilidadGeneral().django_manager.set_palet(palet)
    if(result =='SSCC_EXISTS' ):
        print("Error: Un palet con este SSCC ya existe.")
        return None
    if result is None:
        print(f"Error al subir palet")
        return None
    
    return result

def check_orden_and_update(orden: OrdenProduccion,nuevo_contador, contador_actual, fin_contador_genetal):
    print("🚀 ~ orden.id>4 and orden.inicio_contador< nuevo_contador:", orden.id>4 and orden.inicio_contador< nuevo_contador, orden.id>4 , orden.inicio_contador< nuevo_contador)
    if orden.id>4 and orden.inicio_contador< nuevo_contador and contador_actual!=-1:
        try:
            print("🚀 ~ nuevo_contador > contador_actual:", nuevo_contador > contador_actual, nuevo_contador , contador_actual)
            if nuevo_contador > contador_actual:
                for palet_numero in range(contador_actual, nuevo_contador):
                    palet:Palet = subir_palet(orden, palet_numero)
                    if palet != None:
                        print("🚀 ~ palet id:", palet.id, palet.sscc)
                        try:
                            utilidad_general = UtilidadGeneral()
                            utilidad_general.update_firebase()
                            utilidad_general.django_manager.update_counter_orden_produccion_async(orden.id,fin_contador_genetal,palet_numero)
                        except Exception as e:
                            print(f'😵‍💫Error al actualizar orden produccion', e)

        except Exception as e:
            print(f'😵‍💫Erroooooooooooor crear palet', e)
def convertir_id_string_a_int(id):
    try:
        id = int(id)
    except Exception as e:
        print(f"Error al convertir a entero {e}")
        id = 1
    return id



class UtilidadGeneral:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UtilidadGeneral, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Verificar si ya fue inicializado para evitar múltiples inicializaciones
        if hasattr(self, "initialized") and self.initialized:
            return
        self.linea = 3
        self.is_run = False
        self.actualizar_productos_addresses =  "ns=2;s=Inbalnor_OPC.generales.p1_actualizar_productos"
        # Opc addresses subscription
        self.opc_addresses_subcription = {
            'job_trigger': f'ns=2;s=Inbalnor_OPC.generales.p1_l{self.linea}_job_trigger_terciaria',
            # 'terciaria_counter1': f'ns=2;s=Printers_Inbalnor.p1_l{self.linea}_terciaria.Devices.p1_l{self.linea}_terciaria.Counter1',
            # 'terciaria_total_counter': f'ns=2;s=Printers_Inbalnor.p1_l{self.linea}_terciaria.Devices.p1_l{self.linea}_terciaria.TotalCount',
            # 'terciaria_job_id': f"ns=2;s=Printers_Inbalnor.p1_l{self.linea}_terciaria.Devices.p1_l{self.linea}_terciaria.CurrentProduct",
            'terciaria_job_id': f'ns=2;s=Inbalnor_OPC.generales.p1_l{self.linea}_terciaria_CurrentProduct',
            'terciaria_total_counter': f'ns=2;s=Inbalnor_OPC.generales.p1_l{self.linea}_terciaria_TotalCount',
            'terciaria_counter1': f'ns=2;s=Inbalnor_OPC.generales.p1_l{self.linea}_terciaria_Counter1', 
        }
        # Individual attributes
        self.job_trigger = -1
        self.turno = -1
        self.terciaria_counter1 = -1
        self.terciaria_total_counter = -1
        self.terciaria_job_id = -1
        self.orden_produccion_actual = OrdenProduccion.default()
        # Managers and subscribers
        self.opc_url="opc.tcp://192.168.100.112:49320"
        self.django_manager = DjangoManager()
        self.firebase_manager = FirebaseManager(self.django_manager, str(self.linea))
        self.opc_manager = OpcManager(self.opc_url,self.opc_addresses_subcription, self.actualizar_productos_addresses)
        self.opc_manager.init_opcua()
        self.suscriptores = []
        self.initialized = True
        self.setup_signals()

           

    def update_firebase(self):
        self.firebase_manager.set_palet_in_firebase()


    def setup_signals(self):
        self.opc_manager.data_changed.connect(self.on_data_changed)


    def on_data_changed(self, node_id, val):
        UtilidadGeneral.on_data_changed_opc_manager(self,node_id, val)


    def suscribir(self, objeto):
        self.suscriptores.append(objeto)

    def notificar_suscriptores(self):
        for objeto in self.suscriptores:
            objeto.actualizar_con_datos()

    def notificar_suscriptores_por_cambio(self, tipo_cambio):
        for objeto in self.suscriptores:
            if hasattr(objeto, 'actualizar_por_tipo'):
                objeto.actualizar_por_tipo(tipo_cambio)

    def on_data_changed_opc_manager(self, name, val):
        print("🚀 ~  name, val:",  name, val)
        if name == 'job_trigger':
            self.job_trigger = val

        if name == 'terciaria_counter1':
            contador_actual = self.terciaria_counter1
            
            if val is not None:
                try:
                    nuevo_contador = int(val)
                except:
                    nuevo_contador = self.orden_produccion_actual.inicio_contador
                self.terciaria_counter1 = nuevo_contador
                check_orden_and_update(self.orden_produccion_actual, nuevo_contador, contador_actual, self.terciaria_total_counter)

        if name == 'terciaria_job_id':
            self.terciaria_job_id = val
            val = convertir_id_string_a_int(val)
            orden = self.django_manager.get_orden_produccion(val)
            self.turno = orden.turno
            self.orden_produccion_actual = orden
            self.terciaria_counter1 = orden.inicio_contador

        if name == 'terciaria_total_counter':
            self.terciaria_total_counter = val

        self.notificar_suscriptores()
