import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui import MainWindow
from config import get_logger

def main():
    logger = get_logger()
    logger.info("SoundLowerer Plus démarré")

    # Support High DPI pour écrans 4K
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Variable d'environnement pour le scaling
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)

    # Police par défaut adaptée
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)

    w = MainWindow()
    w.show()

    exit_code = app.exec_()
    logger.info("SoundLowerer Plus fermé")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
