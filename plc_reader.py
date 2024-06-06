import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal
from pycomm3 import CommError, SLCDriver
import time
from orden_produccion import OrdenProduccion
from utilidad_general import UtilidadGeneral, check_orden_and_update  # Asegúrate de que esta importación esté correcta


class PLCReader(QThread):
    data_received = Signal(int)  # Señal para enviar datos al hilo principal
    
    def __init__(self, plc_ip, parent=None):
        super().__init__(parent)
        self.plc_ip = plc_ip
        self.running = True
        self.plc = None
    
    def run(self):
        while self.running:
            try:
                if self.plc is None or not self.plc.connected:
                    self.plc = SLCDriver(self.plc_ip)
                    print("PLC IP:", self.plc_ip)
                    self.plc.open()
                    print("Conectado al PLC")
                
                try:

                    tag_C1 = self.plc.read('C5:1.ACC').value
                    tag_C2 = self.plc.read('C5:2.ACC').value
                    changes = False

                    
                    if UtilidadGeneral.datos_compartidos.get("C1") != tag_C1:
                        UtilidadGeneral.datos_compartidos["C1"] = tag_C1
                        print("Contador Izquierda:", tag_C1)
                        orden:OrdenProduccion = UtilidadGeneral.datos_compartidos['orden_produccion_actual_izquierda']
                        changes = True

                        try:
                            c0_actual = self.read_value_plc('C5:0.ACC')
                            if c0_actual <10:
                                n7_total = f'10{c0_actual}'
                            else:
                                n7_total = f'1{c0_actual}'
                            addres_job_trigger = f'L9:{c0_actual}'
                            addres_linea_string = f'N7:{n7_total}'
                            check_orden_and_update(orden, tag_C1, addres_job_trigger, addres_linea_string)
                        except Exception as e:
                            print(f' 😵‍💫Error al obtener valor C0: {e}')


                    if UtilidadGeneral.datos_compartidos.get("C2") != tag_C2:
                        UtilidadGeneral.datos_compartidos["C2"] = tag_C2
                        print("Contador Derecha:", tag_C2)
                        changes = True
                        orden: OrdenProduccion = UtilidadGeneral.datos_compartidos['orden_produccion_actual_derecha']
                        try:
                            c0_actual = self.read_value_plc('C5:0.ACC')
                            if c0_actual <10:
                                n7_total = f'10{c0_actual}'
                            else:
                                n7_total = f'1{c0_actual}'
                            addres_job_trigger = f'L9:{c0_actual}'
                            addres_linea_string = f'N7:{n7_total}'
                            check_orden_and_update(orden, tag_C2, addres_job_trigger, addres_linea_string)
                        except:
                            print(f' 😵‍💫Error al obtener valor C0: {e}')


                    if changes:
                        self.data_received.emit(1)
                
                
                
                except CommError as e:
                    print(f"Error reading PLC: {e}")
                    self.handle_comm_error()

            except Exception as e:
                print(f"Error connecting to PLC: {e}")
                self.handle_comm_error()

            time.sleep(0.5)  # Leer datos cada 500 ms

    def handle_comm_error(self):
        if self.plc is not None:
            try:
                self.plc.close()
            except CommError as e:
                print(f"Error closing PLC connection: {e}")
            finally:
                self.plc = None
        time.sleep(5)  # Esperar 5 segundos antes de intentar reconectar
    

    def stop(self):
        self.running = False
        self.wait()
        if self.plc is not None:
            try:
                self.plc.close()
            except CommError as e:
                print(f"Error closing PLC connection: {e}")


    def write_value_plc(self,  value):
        try:
            if self.plc is None or not self.plc.connected:
                self.plc = SLCDriver(self.plc_ip)
                self.plc.open()
                print("Conectado al PLC para escritura")
            
            self.plc.write(value)
            print(f"Escrito : {value} ")
        except CommError as e:
            print(f"Error writing to PLC: {e}")
            self.handle_comm_error()
        except Exception as e:
            print(f"Error writing to PLC: {e}")

    def read_value_plc(self, address):
        try:
            if self.plc is None or not self.plc.connected:
                self.plc = SLCDriver(self.plc_ip)
                self.plc.open()
                print("Conectado al PLC para lectura")
            
            value = self.plc.read(address).value
            print(f"Leído de {address}: {value}")
            return value
        except CommError as e:
            print(f"Error reading from PLC: {e}")
            self.handle_comm_error()
            return None
        except Exception as e:
            print(f"Error reading from PLC: {e}")
            return None