import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui

# Platform-specific configuration
if sys.platform == 'linux':
    os.environ["QT_QPA_PLATFORM"] = "linuxfb:fb=/dev/fb0"
    os.environ["QT_QPA_EVDEV_TOUCHSCREEN_PARAMETERS"] = "/dev/input/event0:rotate=270"
    os.environ["QT_QPA_GENERIC_PLUGINS"] = "evdevtouch:/dev/input/event0"
    os.environ["QT_QPA_FB_TSLIB"] = "1"
    os.environ["QT_QPA_FB_NO_LIBINPUT"] = "1"
    IS_RASPBERRY_PI = True
else:
    IS_RASPBERRY_PI = False

class Code:
    def __init__(self):
        self.code = ""
    
    def input(self, value):
        self.code += value
    
    def reset(self):
        self.code = ""

    def __eq__(self, value):
        if isinstance(value, Code):
            return self.code == value.code
        return self.code == value

class CodeIndex:
    INDEX = {
        "UUDDLRLR": lambda: QtWidgets.QApplication.quit()
    }
    
    @staticmethod
    def handle(code):
        if code in CodeIndex.INDEX:
            CodeIndex.INDEX[code]()


class Hellpad(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.code = Code()

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
            button.setFocusPolicy(QtCore.Qt.NoFocus)
            button.clicked.connect(lambda checked, btn=button: self.pressButton(btn))

            
        self.container = QtWidgets.QFrame(self)
        self.container.setFixedSize(480, 320)
        self.container.setObjectName("Hellpad")

        self.layout = QtWidgets.QGridLayout(self.container)

        for i, button in enumerate(self.buttons):
            row = i // 3
            col = i % 3
            self.layout.addWidget(button, row, col)
        self.layout.setVerticalSpacing(12)
        self.layout.setHorizontalSpacing(26)

        for i in range(3):
            self.layout.setColumnStretch(i, 1)
        for i in range(2):
            self.layout.setRowStretch(i, 1)

        self.setObjectName("Hellpad")
        self.setStyleSheet("""
            #Hellpad {
                background-image: url("hellpad-background.png");
                padding: 85 54 14 54;
            }
            QPushButton {
                background-color: rgba(142, 143, 136, 0.3);
                border: 2px solid #d9d68b;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: rgba(240, 240, 250, 0.8);
            }
        """)

        # After creating all buttons and layouts, clear the tab chain
        self.setTabOrder(self.buttons[-1], self.buttons[0])
        self.setFocusProxy(None)

    def pressButton(self, button):
        if button.text() == "❌":
            self.code.reset()
        elif button.text() == "✔️":
            CodeIndex.handle(self.code)
            self.code.reset()
        elif button.text() == "↑":
            self.code.input("U")
        elif button.text() == "↓":
            self.code.input("D")
        elif button.text() == "←":
            self.code.input("L")
        elif button.text() == "→":
            self.code.input("R")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    if IS_RASPBERRY_PI:
        widget = Hellpad()
        widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        widget.showFullScreen()
    else:
        widget = Hellpad()
        widget.resize(480, 320)
        widget.show()

    sys.exit(app.exec())