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
        "SASWD": "MG-43 MACHINE GUN",
        "SADWS": "APW-1 ANTI-MATERIEL RIFLE",
        "SASWWA": "M-105 STALWART",
        "SSAWD": "EAT-17 EXPENDABLE ANTI-TANK",
        "SADDA": "GR-8 RECOILLESS RIFLE",
        "SAWSW": "FLAM-40 FLAMETHROWER",
        "SASWWD": "AC-8 AUTOCANNON",
        "SAWSS": "MG-206 HEAVY MACHINE GUN",
        "SWWAD": "RL-77 AIRBURST ROCKET LAUNCHER",
        "SAWSD": "MLS-4X COMMANDO",
        "SDSWAD": "RS-422 RAILGUN",
        "SSWSS": "FAF-14 SPEAR",
        "SSWSD": "StA-X3 W.A.S.P. LAUNCHER",
        "DSAWW": "ORBITAL GATLING BARRAGE",
        "DDD": "ORBITAL AIRBURST STRIKE",
        "DDSADS": "ORBITAL 120MM HE BARRAGE",
        "DSWWASS": "ORBITAL 380MM HE BARRAGE",
        "DSDSDS": "ORBITAL WALKING BARRAGE",
        "DSWDS": "ORBITAL LASER",
        "DDSADW": "ORBITAL NAPALM BARRAGE",
        "DWSSD": "ORBITAL RAILCANNON STRIKE",
        "WDD": "EAGLE STRAFING RUN",
        "WDSD": "EAGLE AIRSTRIKE",
        "WDSSD": "EAGLE CLUSTER BOMB",
        "WDSW": "EAGLE NAPALM AIRSTRIKE",
        "SWWSW": "LIFT-850 JUMP PACK",
        "WDWS": "EAGLE SMOKE STRIKE",
        "WDWA": "EAGLE 110MM ROCKET PODS",
        "WDSSS": "EAGLE 500KG BOMB",
        "ASDSDSW": "M-102 FAST RECON VEHICLE",
        "DDW": "ORBITAL PRECISION STRIKE",
        "DDSD": "ORBITAL GAS STRIKE",
        "DDAS": "ORBITAL EMS STRIKE",
        "DDSW": "ORBITAL SMOKE STRIKE",
        "SWADDA": "E/MG-101 HMG EMPLACEMENT",
        "SSADAD": "FX-12 SHIELD GENERATOR RELAY",
        "SWDWAD": "A/ARC-3 TESLA TOWER",
        "SAWD": "MD-6 ANTI-PERSONNEL MINEFIELD",
        "SASWWS": "B-1 SUPPLY PACK",
        "SAWAS": "GL-12 GRENADE LAUNCHER",
        "SASWA": "LAS-98 LASER CANNON",
        "SAAS": "MD-14 INCENDIARY MINES",
        "SWAWDD": "AX/LAS-5 \"GUARD DOG\" ROVER",
        "SASSWA": "SH-20 BALLISTIC SHIELD BACKPACK",
        "SDSWAA": "ARC-3 ARC THROWER",
        "SAWW": "MD-17 ANTI-TANK MINES",
        "SSWAD": "LAS-99 QUASAR CANNON",
        "SWADAD": "SH-32 SHIELD GENERATOR PACK",
        "SAAD": "MD-8 GAS MINES",
        "SWDDW": "A/MG-43 MACHINE GUN SENTRY",
        "SWDA": "A/G-16 GATLING SENTRY",
        "SWDDS": "A/M-12 MORTAR SENTRY",
        "SWAWDS": "AX/AR-23 \"GUARD DOG\"",
        "SWDWAW": "A/AC-8 AUTOCANNON SENTRY",
        "SWDDA": "A/MLS-4X ROCKET SENTRY",
        "SWDSD": "A/M-23 EMS MORTAR SENTRY",
        "ASDWASS": "EXO-45 PATRIOT EXOSUIT",
        "ASDWASW": "EXO-49 EMANCIPATOR EXOSUIT",
        "SAWSA": "TX-41 STERILIZER",
        "SWAWDW": "AX/TX-13 \"GUARD DOG\" DOG BREATH",
        "SWADWW": "SH-51 DIRECTIONAL SHIELD",
        "SWADDD": "E/AT-12 ANTI-TANK EMPLACEMENT",
        "SWDSWW": "A/FLAM-40 FLAME SENTRY",
        "SDWWW": "B-100 PORTABLE HELLBOMB",
        "WSDAW": "REINFORCE",
        "WSDW": "SOS BEACON",
        "SSWD": "RESUPPLY",
        "WWAWD": "EAGLE REARM",
        "SSSWW": "SSSD DELIVERY",
        "SSADSS": "PROSPECTING DRILL",
        "SWSW": "SUPER EARTH FLAG",
        "SWASWDSW": "HELLBOMB",
        "ADWWW": "UPLOAD DATA",
        "WWADSS": "SEISMIC PROBE",
        "DDAA": "ORBITAL ILLUMINATION FLARE",
        "DWWS": "SEAF ARTILLERY",
        "WADSWW": "DARK FLUID VESSEL",
        "WSWSWS": "TECTONIC DRILL",
        "AWSDSS": "HIVE BREAKER DRILL",
        "WWSSADAD": quit
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
                self.code.input("D")
                # self.press_sound.stop()
                # self.press_sound.play()
            else:
                # Left swipe
                self.code.input("A")
                # self.press_sound.stop()
                # self.press_sound.play()
        else:
            # Vertical swipe
            if dy > 0:
                # Down swipe
                self.code.input("S")
                # self.press_sound.stop()
                # self.press_sound.play()
            else:
                # Up swipe
                self.code.input("W")
                # self.press_sound.stop()
                # self.press_sound.play()
        
        result = CodeIndex.handle(self.code)
        self.setCodeDisplay(self.code.code, result)
    
    def printText(self, text = ""):
        self.code_name_text_queue += text
        self.printNextTextQueueChar()

    def printNextTextQueueChar(self):
        if self.code_name_text_queue == "":
            return
        if " " in self.code_name_text_queue:
            self.code_name.setText(self.code_name.text() + self.code_name_text_queue[0:self.code_name_text_queue.index(" ") + 1])
            self.code_name_text_queue = self.code_name_text_queue[self.code_name_text_queue.index(" ")+1:]
        else:
            self.code_name.setText(self.code_name.text() + self.code_name_text_queue)
            self.code_name_text_queue = ""
        if len(self.code_name_text_queue) > 0:
            QtCore.QTimer.singleShot(100, self.printNextTextQueueChar)

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
            self.code_name_text_queue = ""
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
            if direction == "D":
                transform.rotate(90)
            elif direction == "S":
                transform.rotate(180)
            elif direction == "A":
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