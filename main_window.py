import subprocess, sys
from datetime import datetime
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton,
                               QVBoxLayout, QHBoxLayout, QPushButton,QStackedWidget, QFrame, 
                               QGroupBox,  QSpacerItem, QSizePolicy, QLineEdit)
from django_manager import DjangoManager
from opc_manager import OpcManager
from PySide6.QtCore import Qt

from orden_produccion import OrdenProduccion
from utilidad_general import UtilidadGeneral


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    
        printers_info = [
            (f'Linea 1', 0,0,0,0,'Error'),
            (f'Linea 2', 0,0,0,0,'Error'),
            (f'Linea 3', 0,0,0,0,'Error'),
            (f'Linea 4', 0,0,0,0,'Error'),
            (f'Linea 5', 0,0,0,0,'Error'),
        ]
        self.setWindowTitle(f'Sinconizacion en cargar palets a Django')
        #Cambiar de 0, 400, 800
       
        self.setGeometry(0, 30, 900, 250)
         # Información de las impresoras
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.opc_url="opc.tcp://192.168.100.112:49320"
        self.django_manager = DjangoManager()
        self.opc_manager = OpcManager(opc_url=self.opc_url)
        UtilidadGeneral.inicializar_managers(self.django_manager, self.opc_manager)       
        UtilidadGeneral.suscribir(self)

        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 20, 10, 10)

        self.printer_widgets = {}  # Diccionario para mantener las referencias
        printers_container = QFrame()
        printers_layout = QGridLayout()  # Usamos QGridLayout
        

        # Ancho fijo para la sección de impresoras
        # printers_container.setFixedWidth(self.width-50)  

        numero_de_columnas = 3

        for index, (name, orden, contador, turno, tigger, status) in enumerate(printers_info):
            fila = index // numero_de_columnas
            columna = index % numero_de_columnas
         
        # for name, orden, contador, turno, tigger in printers_info:
            group_box = QGroupBox(name)
            group_box.setStyleSheet("""
                QGroupBox {
                    font-size: 14pt; /* Tamaño de la fuente del título */
                    color: #000080; /* Color del texto del título */
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px; /* Desplazamiento a la izquierda del título */
                    padding: 0 3px 0 3px; /* Padding alrededor del texto: arriba derecha abajo izquierda */
                    background-color: rgb(240, 240, 240); /* Ajusta esto al color de fondo de tu ventana o widget */
                }
            """)

            group_layout = QVBoxLayout(group_box)
            group_layout.setSpacing(5)

            orden_label = QLabel(f"# Orden: {orden}")
            orden_label.setStyleSheet("""
                QLabel {
                    font-size: 12pt; /* Cambia el tamaño de la fuente */
                    color: #555555; /* Cambia el color del texto */
                    font-weight: bold; /* Hace el texto en negrita */
                }
            """)
            group_layout.addWidget(orden_label)


            job_tigger_label = QLabel(f"Tigger: {tigger}")
            job_tigger_label.setStyleSheet("""
                QLabel {
                    font-size: 12pt; /* Cambia el tamaño de la fuente */
                    color: #555555; /* Cambia el color del texto */
                    font-weight: bold; /* Hace el texto en negrita */
                }
            """)
            group_layout.addWidget(job_tigger_label)


            

            contador_label = QLabel(f"Contador: {contador}")
            contador_label.setStyleSheet("""
                QLabel {
                    font-size: 12pt; /* Cambia el tamaño de la fuente */
                    color: #555555; /* Cambia el color del texto */
                    font-weight: bold; /* Hace el texto en negrita */
                }
            """)
            group_layout.addWidget(contador_label)

            status_label = QLabel(f"Status: {status}")
            status_label.setStyleSheet("""
                QLabel {
                    font-size: 12pt; /* Cambia el tamaño de la fuente */
                    color: #555555; /* Cambia el color del texto */
                    font-weight: bold; /* Hace el texto en negrita */
                }
            """)
            group_layout.addWidget(status_label)


            turno_label = QLabel(f"Turno: {turno}")
            turno_label.setStyleSheet("""
                QLabel {
                    font-size: 12pt; /* Cambia el tamaño de la fuente */
                    color: #555555; /* Cambia el color del texto */
                    font-weight: bold; /* Hace el texto en negrita */
                }
            """)
            group_layout.addWidget(turno_label)

           
            printers_layout.addWidget(group_box, fila, columna)

            self.printer_widgets[name] = (name, orden_label, contador_label, turno_label, job_tigger_label, status_label)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # printers_layout.addSpacerItem(spacer)
        printers_container.setLayout(printers_layout)

        
      

        # Añadir elementos al layout principal
        main_layout.addWidget(printers_container)
        main_layout.addSpacing(5) 
        self.setup_signals()


    def setup_signals(self):
        self.opc_manager.data_changed.connect(self.on_data_changed)


    def on_data_changed(self, node_id, val):
        UtilidadGeneral.on_data_changed_opc_manager(node_id, val)

        


    def update_linea_status(self, name, orden, contador, turno, tigger, status):
       
        if name in self.printer_widgets:
            name, orden_label, contador_label, turno_label, job_tigger_label, status_label = self.printer_widgets[name]
            # Si se proporciona un nuevo estado, actualizar el texto del estado y el color del indicador
            if orden is not None:
                orden_label.setText(f"# Orden: {orden}")

            if contador is not None:
                contador_label.setText(f"Contador: {contador}")

            if turno is not None:
                turno_label.setText(f"Turno: {turno}")

            if tigger is not None:
                job_tigger_label.setText(f"Tigger: {tigger}")

            if status is not None:
                status_label.setText(f"Status: {status}")

            
    def actualizar_con_datos(self):

        for i in range(1,6):
            self.update_linea_status(f'Linea {i}',
                                    UtilidadGeneral.datos_compartidos[f'job_trigger_l{i}'], 
                                    UtilidadGeneral.datos_compartidos[f'terciaria_counter1_l{i}'],
                                    UtilidadGeneral.datos_compartidos[f'turno_l{i}'],
                                    UtilidadGeneral.datos_compartidos[f'terciaria_job_id_l{i}'],
                                    UtilidadGeneral.datos_compartidos[f'terciaria_status_l{i}'])
    def closeEvent(self, event):
        print("Limpiando antes de cerrar...")
        UtilidadGeneral.datos_compartidos["opc_manager"].disconnect_opcua()
        event.accept()
            


def cleanup():
    print("Limpiando antes de cerrar...")
    # main_window.opc_manager.disconnect_opcua()
    print("Cerrando la aplicación...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    # Conectar la señal aboutToQuit a la función de limpieza
    app.aboutToQuit.connect(cleanup)
    sys.exit(app.exec())
