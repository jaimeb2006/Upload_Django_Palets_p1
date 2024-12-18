import subprocess, sys
from datetime import datetime
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton,
                               QVBoxLayout, QHBoxLayout, QPushButton,QStackedWidget, QFrame, 
                               QGroupBox,  QSpacerItem, QSizePolicy, QLineEdit)

from utilidad_general import UtilidadGeneral


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.utilidad_general = UtilidadGeneral()
        self.linea = self.utilidad_general.linea
        printer_info = (f'Línea {self.linea}', 0, 0, 0, 0)
        self.setWindowTitle(f'Sin L{self.linea}')
        posicion_x = ((self.linea)-1)*250
        self.setGeometry(posicion_x, 0, 250, 200)
        self.utilidad_general.suscribir(self)

        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 20, 10, 10)

        # Contenedor para la información de la línea
        printers_container = QFrame()
        printers_layout = QGridLayout()

        # Desempaquetar la información de una sola línea
        name, orden, contador, turno, trigger = printer_info

        # Crear un QGroupBox con la información de la línea
        group_box = QGroupBox(name)
        group_box.setStyleSheet("""
            QGroupBox {
                font-size: 14pt;
                color: #000080;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                background-color: rgb(240, 240, 240);
            }
        """)

        group_layout = QVBoxLayout(group_box)
        group_layout.setSpacing(5)

        # Widgets de información
        self.orden_label = QLabel(f"# Orden: {orden}")
        self.orden_label.setStyleSheet("font-size: 12pt; color: #555555; font-weight: bold;")
        group_layout.addWidget(self.orden_label)

        self.trigger_label = QLabel(f"Trigger: {trigger}")
        self.trigger_label.setStyleSheet("font-size: 12pt; color: #555555; font-weight: bold;")
        group_layout.addWidget(self.trigger_label)

        self.contador_label = QLabel(f"Contador: {contador}")
        self.contador_label.setStyleSheet("font-size: 12pt; color: #555555; font-weight: bold;")
        group_layout.addWidget(self.contador_label)

        self.turno_label = QLabel(f"Turno: {turno}")
        self.turno_label.setStyleSheet("font-size: 12pt; color: #555555; font-weight: bold;")
        group_layout.addWidget(self.turno_label)

        # Añadir el QGroupBox al layout
        printers_layout.addWidget(group_box, 0, 0)
        printers_container.setLayout(printers_layout)

        # Añadir el contenedor al layout principal
        main_layout.addWidget(printers_container)
        main_layout.addSpacing(5)
        print("🚀 inicializado main")

    def update_linea_status(self):
        
        print("🚀 ~ update_linea_status:",self.utilidad_general.orden_produccion_actual.id)
        self.orden_label.setText(f"# Orden: {self.utilidad_general.orden_produccion_actual.id}")
        self.trigger_label.setText(f"Trigger: {self.utilidad_general.job_trigger}")
        self.contador_label.setText(f"Contador: {self.utilidad_general.terciaria_counter1}")
        self.turno_label.setText(f"Turno: {self.utilidad_general.turno}")

    def actualizar_con_datos(self):
        print("🚀~ actualizar_con_datos" )
        self.update_linea_status()

    def closeEvent(self, event):
        print("Limpiando antes de cerrar...")
        self.utilidad_general.opc_manager.disconnect_opcua()
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
