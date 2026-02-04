import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
from config import get_logger

def main():
    logger = get_logger()
    logger.info("SoundLowerer Plus démarré")

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()

    exit_code = app.exec_()
    logger.info("SoundLowerer Plus fermé")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
