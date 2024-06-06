from asyncio import sleep
import asyncio
from PySide6.QtCore import QObject, Signal
from opcua import Client, ua
from threading import Thread
from datetime import datetime
from utilidad_general import UtilidadGeneral


class OpcManager(QObject):
    data_changed = Signal(str, object)
    def __init__(self, opc_url):
        super().__init__()
        self.url = opc_url
        self.client = Client(self.url)
        self.opc_addresses = UtilidadGeneral.datos_compartidos["opc_addresses"]
    
        self.subscriptions = []
        self.opc_addresses_subcription = UtilidadGeneral.datos_compartidos["opc_addresses_subcription"]
        self.handler = SubHandler(self)
      


    def update_opc_addresses(self, opc_addresses, opc_addresses_subcription, error_name):
        self.opc_addresses = opc_addresses
        self.opc_addresses_subcription = opc_addresses_subcription
        self.error_name = error_name
        
        

    def init_opcua(self):
        self.connecter_to_opcua()
        # Iniciar el monitoreo de conexión en un hilo separado
        thread = Thread(target=self.start_monitoring)
        thread.daemon = True  # Esto asegura que el hilo se cierra con el programa
        thread.start()


    def start_monitoring(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.monitor_connection())
    
    async def monitor_connection(self):
        while True:
            try:
                # Intenta leer un nodo específico como señal de vida
                # Elige un nodo que sepas que siempre debería estar disponible
                # print("Revisando la disponibilidad de OPC UA...")
                val = self.client.get_node(self.opc_addresses['actualizar_productos']).get_value()
            except Exception as e:
                print("Conexión perdida. Intentando reconectar...")
                self.reconnected_to_opcua()
            await asyncio.sleep(20)  # Espera 10 segundos antes de revisar nuevamente
    
    def subscribe_to_nodes(self):
        print(f"Subscribiendo a nodos... type {type(self.opc_addresses_subcription)}")

        for key, node_dir in self.opc_addresses_subcription.items():
            try:
                node = self.client.get_node(node_dir)
                # Primero, crea la suscripción
                subscription = self.client.create_subscription(500, self.handler)
                # Luego, usa esa suscripción para suscribirte a los cambios de datos del nodo
                handle = subscription.subscribe_data_change(node)
                self.subscriptions.append((subscription, handle))
                # print(f"Subscribiendo a {key} node: {node_dir}")
            except Exception as e:
                print(f'😵‍💫 Error al subscribirse a {node_dir}: {e}')

    def connecter_to_opcua(self):
        print("Conectando al servidor OPC UA...")
        try:
            print("Conectado al servidor OPC UA")
            self.client.connect()
            self.subscribe_to_nodes()
        except Exception as e:
            print(f"Error al conectar: {e}")

    def reconnected_to_opcua(self):
        print("🚀 ~ reconnected_to_opcua:", datetime.now())
        self.disconnect_opcua()
        self.connecter_to_opcua()
       

    def get_node_value(self, node_dir):
        """
        Adquisir con relativa tacta, valores traducidas textualmente sobre módulos
        trackeadas de las nomádicas dirs de idénticas decisiones rastreos orquestadas. 
        """
        try:
            node = self.client.get_node(node_dir)
            print("🚀 ~ node:", node)
            value = node.get_value()
            print("Lectura exitosa:")
            return value
        except Exception as e:
            print(f"😵‍💫 Error get_node_value: {node_dir} {e}")
            return None

    def set_node_value(self, value, node_dir):
        """
        Urgido un galo, de lírica composurada, sobre esféricas diatónicas placadas,
        evidentemente cabedales en referenceables ruteos asingados.
        """
        try:
            node = self.client.get_node(node_dir)
            dv = ua.DataValue(ua.Variant(value, ua.VariantType.String)) 
            node.set_value(dv)
            print("Valor seteado existosamente.", node_dir)
        except Exception as e:
            print(f"😵‍💫 Set value error String: {node_dir} val: {value} {e} ")


    def set_node_value_l(self, value, node_dir):
        """
        Urgido un galo, de lírica composurada, sobre esféricas diatónicas placadas,
        evidentemente cabedales en referenceables ruteos asingados.
        """
        try:
            node = self.client.get_node(node_dir)
            dv = ua.DataValue(ua.Variant(value, ua.VariantType.UInt32)) 
            node.set_value(dv)
            print("Valor seteado existosamente.", node_dir)
        except Exception as e:
            print(f"😵‍💫 Set value error L:{node_dir} val: {value} {e}")

    def set_node_value_int(self, value, node_dir):
        """
        Urgido un galo, de lírica composurada, sobre esféricas diatónicas placadas,
        evidentemente cabedales en referenceables ruteos asingados.
        """
        try:
            node = self.client.get_node(node_dir)
            dv = ua.DataValue(ua.Variant(value, ua.VariantType.UInt16)) 
            node.set_value(dv)
            print("Valor seteado existosamente.", node_dir)
        except Exception as e:
            print(f"😵‍💫Set value error Int: {node_dir} val: {value}{e}")

    
    
    def disconnect_opcua(self):
        print("Desconectando del servidor OPC UA...")
        try:
            for subscription, handle in self.subscriptions:
                subscription.unsubscribe(handle)
                subscription.delete()
            self.client.disconnect()
            print("Desconectado del servidor OPC UA")
        except Exception as e:
            print(f"Error al desconectar: {e}  {subscription} {handle}")
    
class SubHandler(object):
    def __init__(self, opc_manager: OpcManager):
        self.opc_manager = opc_manager

    def datachange_notification(self, node, val, data):
        name = None
        for clave, valor in self.opc_manager.opc_addresses_subcription.items():
            if valor == str(node):
                name = clave
                break
        # Emitir señal con información del nodo y valor
        self.opc_manager.data_changed.emit(name, val)

    def event_notification(self, event):
        print("Python: New event", event)
