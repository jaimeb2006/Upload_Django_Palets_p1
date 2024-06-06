# def rotate_array(arr, index):
#     return arr[index:] + arr[:index]

# # Ejemplo de uso
# array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# index = 8
# rotated_array = rotate_array(array, index)
# print(rotated_array)

# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
# from PySide6.QtCore import Qt

# class ArrayViewer(QWidget):
#     def __init__(self, array, index):
#         super().__init__()

#         self.array = array
#         self.index = index

#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()
        
#         # Crear y configurar el layout horizontal para los recuadros
#         h_layout = QHBoxLayout()
#         rotated_array = self.rotate_array(self.array, self.index)

#         for elem in rotated_array:
#             label = QLabel(str(elem))
#             label.setAlignment(Qt.AlignCenter)
#             label.setStyleSheet("border: 1px solid black; padding: 10px;")
#             h_layout.addWidget(label)
        
#         layout.addLayout(h_layout)
#         self.setLayout(layout)
#         self.setWindowTitle('Array Viewer')
#         self.show()

#     def rotate_array(self, arr, index):
#         return arr[index:] + arr[:index]

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     index = 6
#     viewer = ArrayViewer(array, index)
#     sys.exit(app.exec())


import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class ArrayViewer(QWidget):
    def __init__(self, array, index):
        super().__init__()

        self.array = array
        self.index = index

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Crear y configurar el layout horizontal para los recuadros
        h_layout = QHBoxLayout()
        rotated_array = self.rotate_array(self.array, self.index)

        # Definir el tamaño fijo de los recuadros
        fixed_size = 50

        for elem in rotated_array:
            label = QLabel(str(elem))
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(fixed_size, fixed_size)
            label.setStyleSheet("""border: 3px solid black; 
                                padding: 10px; 
                                font-size: 20px; color:red;
                                font-weight: bold;""")
            h_layout.addWidget(label)
        
        layout.addLayout(h_layout)
        self.setLayout(layout)
        self.setWindowTitle('Array Viewer')
        self.show()

    def rotate_array(self, arr, index):
        return arr[index:] + arr[:index]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    index = 1
    viewer = ArrayViewer(array, index)
    sys.exit(app.exec())

