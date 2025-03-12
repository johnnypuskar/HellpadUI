import random
import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui

# Set environment for Pi headless mode
os.environ["QT_QPA_PLATFORM"] = "eglfs"

class Hellpad(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button_labels = [
            "✔️", "↑", "❌", "←", "↓", "→"
        ]

        self.buttons = [
            QtWidgets.QPushButton(self.button_labels[i]) for i in range(6)
        ]

        button_font = QtGui.QFont()
        button_font.setPointSize(36)

        for button in self.buttons:
            button.setFont(button_font)
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                               QtWidgets.QSizePolicy.Expanding)

        self.layout = QtWidgets.QGridLayout(self)
        
        for i, button in enumerate(self.buttons):
            row = i // 3
            col = i % 3
            self.layout.addWidget(button, row, col)
            
        self.layout.setSpacing(0)
        for i in range(3):
            self.layout.setColumnStretch(i, 1)
        for i in range(2):
            self.layout.setRowStretch(i, 1)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b3b;
            }
            QPushButton {
                background-color: #2b2b3b;
                border: 1px solid grey;
                color: white;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: #1f1f2b;
            }
        """)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    app.setApplicationAttribute(QtCore.Qt.AA_DisableHighDpiScaling)
    
    widget = Hellpad()
    widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    widget.showFullScreen()

    sys.exit(app.exec())