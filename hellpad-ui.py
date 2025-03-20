import sys
import os
import time
from PySide6 import QtCore, QtWidgets, QtGui, QtMultimedia

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
        "DLDUR": "MG-43 MACHINE GUN",
        "DLRUD": "APW-1 ANTI-MATERIEL RIFLE",
        "DLDUUL": "M-105 STALWART",
        "DDLUR": "EAT-17 EXPENDABLE ANTI-TANK",
        "DLRRL": "GR-8 RECOILLESS RIFLE",
        "DLUDU": "FLAM-40 FLAMETHROWER",
        "URDDD": "EAGLE 500KG BOMB",
        "RRU": "ORBITAL PRECISION STRIKE",
        "LDRULDD": "EXO-45 PATRIOT EXOSUIT",
        "UUDDLRLR": quit
    }
    
    @staticmethod
    def handle(code_obj):
        if CodeIndex.is_valid(code_obj.code):
            value = CodeIndex.INDEX[code_obj.code]
            if callable(value):
                return value()
            return value
        return None
    
    @staticmethod
    def is_valid(code):
        return code in CodeIndex.INDEX

    @staticmethod
    def quit():
        QtWidgets.QApplication.quit()
        return "QUIT PROGRAM"


class Hellpad(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Touch handling
        self.setAttribute(QtCore.Qt.WA_AcceptTouchEvents)
        self.touch_start_pos = None
        self.min_swipe_distance = 50

        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Font setup
        text_font = QtGui.QFontDatabase.addApplicationFont(os.path.join(current_dir, "automate.ttf"))
        if text_font != -1:
            font_family = QtGui.QFontDatabase.applicationFontFamilies(text_font)[0]
        else:
            font_family = "Arial"

        self.code = Code()

        self.press_sound = QtMultimedia.QSoundEffect()
        self.press_sound.setSource(QtCore.QUrl.fromLocalFile(os.path.join(current_dir, "audio/press.wav")))

        self.success_sound = QtMultimedia.QSoundEffect()
        self.success_sound.setSource(QtCore.QUrl.fromLocalFile(os.path.join(current_dir, "audio/success.wav")))

        self.fail_sound = QtMultimedia.QSoundEffect()
        self.fail_sound.setSource(QtCore.QUrl.fromLocalFile(os.path.join(current_dir, "audio/fail.wav")))

        self.container = QtWidgets.QFrame(self)
        self.container.setFixedSize(480, 320)
        self.container.setObjectName("Hellpad")

        
        self.arrow_image = QtGui.QPixmap(os.path.join(current_dir, "arrow.png"))
        self.arrow_image_highlighted = QtGui.QPixmap(os.path.join(current_dir, "arrow-highlighted.png"))
        self.arrow_size = QtCore.QSize(50, 50)  # Define size for arrows

        # Create container for arrows instead of text label
        self.code_display = QtWidgets.QWidget(self.container)
        self.code_display.setFixedHeight(60)
        self.code_display.move((480-200)//2, (320-60)//2)  # Initial position
        self.code_display_layout = QtWidgets.QHBoxLayout(self.code_display)
        self.code_display_layout.setContentsMargins(0, 0, 0, 0)
        self.code_display_layout.setSpacing(0)
        self.code_display_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.code_name = QtWidgets.QLabel(self.container)
        self.code_name.setAlignment(QtCore.Qt.AlignCenter)
        self.code_name.setFixedSize(480, 60)
        self.code_name.move(0, (320)//2 + 10)  # Center in container
        self.code_name.setObjectName("CodeName")
        self.code_name.setFont(QtGui.QFont(font_family, 48))
        self.code_name_text_queue = ""

        self.reset_button = QtWidgets.QPushButton("❌", self.container)
        self.reset_button.setFixedSize(85, 70)
        self.reset_button.move(
            self.container.width() - self.reset_button.width() - 10,
            self.container.height() - self.reset_button.height() - 30
        )
        self.reset_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.reset_button.setObjectName("ResetButton")
        self.reset_button.clicked.connect(self.resetCode)
    

        bg_path = os.path.join(current_dir, "hellpad-background.png").replace("\\", "/")
        self.setObjectName("Hellpad")
        self.setStyleSheet(f"""
            #Hellpad {{
                background-image: url("{bg_path}");
                padding: 85 54 14 54;
            }}
            #CodeDisplay {{
                color: #FFFFFF;
                font-size: 48px;
                font-weight: bold;
            }}
            #CodeName {{
                color: #FFFFFF;
                font-size: 20px;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: rgba(142, 143, 136, 0.3);
                border: 2px solid rgba(255, 255, 255, 0.5);
                font-size: 36px;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }}
            QPushButton:pressed {{
                background-color: rgba(240, 240, 250, 0.8);
            }}
        """)
        self.setFocusProxy(None)

    def mousePressEvent(self, event):
        if CodeIndex.is_valid(self.code.code):
            self.resetCode()
        else:
            self.touch_start_pos = event.globalPosition().toPoint()
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if self.touch_start_pos is not None:
            self.handleSwipe(self.touch_start_pos, event.globalPosition().toPoint())
            self.touch_start_pos = None
        return super().mouseReleaseEvent(event)
    
    def handleSwipe(self, start_pos, end_pos):
        dx = end_pos.x() - start_pos.x()
        dy = end_pos.y() - start_pos.y()
        
        # Check if the movement is significant enough to be considered a swipe
        if abs(dx) < self.min_swipe_distance and abs(dy) < self.min_swipe_distance:
            return
        
        # Determine the primary direction of the swipe
        if abs(dx) > abs(dy):
            # Horizontal swipe
            if dx > 0:
                # Right swipe
                self.code.input("R")
                # self.press_sound.stop()
                # self.press_sound.play()
            else:
                # Left swipe
                self.code.input("L")
                # self.press_sound.stop()
                # self.press_sound.play()
        else:
            # Vertical swipe
            if dy > 0:
                # Down swipe
                self.code.input("D")
                # self.press_sound.stop()
                # self.press_sound.play()
            else:
                # Up swipe
                self.code.input("U")
                # self.press_sound.stop()
                # self.press_sound.play()
        
        result = CodeIndex.handle(self.code)
        self.setCodeDisplay(self.code.code, result)
    
    def printText(self, text = ""):
        self.code_name_text_queue += text
        self.printNextTextQueueChar()

    def printNextTextQueueChar(self):
        self.code_name.setText(self.code_name.text() + self.code_name_text_queue[0])
        self.code_name_text_queue = self.code_name_text_queue[1:]
        if len(self.code_name_text_queue) > 0:
            QtCore.QTimer.singleShot(20, self.printNextTextQueueChar)

    def resetCode(self):
        self.code.reset()
        self.setCodeDisplay(self.code.code)

    def setCodeDisplay(self, code, name = None):
        # Clear existing arrows
        while self.code_display_layout.count():
            item = self.code_display_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        highlight = False
        if name is not None:
            highlight = True
            self.printText(name)
        else:
            self.code_name.setText("")

        arrow_size = self.arrow_size
        num_arrows = len(code)
        arrow_width = self.arrow_size.width()
        spacing = self.code_display_layout.spacing()
        total_width = num_arrows * arrow_width + (num_arrows - 1) * spacing if num_arrows > 0 else 200
        
        if total_width > 400:
            arrow_size = QtCore.QSize(400//num_arrows, 400//num_arrows)
            total_width = 400

        for direction in code:
            arrow_label = QtWidgets.QLabel()
            arrow_label.setFixedSize(arrow_size)
            
            # Create a copy of the base arrow image
            if highlight:
                pixmap = self.arrow_image_highlighted.scaled(arrow_size, 
                                                             QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, 
                                                             QtCore.Qt.TransformationMode.SmoothTransformation)
            else:
                pixmap = self.arrow_image.scaled(arrow_size, 
                                                 QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, 
                                                 QtCore.Qt.TransformationMode.SmoothTransformation)
                
            # Apply rotation based on direction
            transform = QtGui.QTransform()
            if direction == "R":
                transform.rotate(90)
            elif direction == "D":
                transform.rotate(180)
            elif direction == "L":
                transform.rotate(270)
            
            rotated_pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
            arrow_label.setPixmap(rotated_pixmap)
            self.code_display_layout.addWidget(arrow_label)
        
        # Update container width and position to center it
        self.code_display.setFixedWidth(max(200, total_width))
        self.code_display.move((480-self.code_display.width())//2, (320-60)//2)
        

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