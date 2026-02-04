import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtGui import QFont
from ui import MainWindow
from config import get_logger

SERVER_NAME = "SoundLowererPlus_SingleInstance"


class SingleInstanceApp(QApplication):
    """Application avec gestion d'instance unique via QLocalServer"""

    def __init__(self, argv):
        super().__init__(argv)
        self._server = None
        self._window = None
        self._is_primary = False

    def is_running(self) -> bool:
        """Vérifie si une instance est déjà en cours et envoie un signal si oui"""
        socket = QLocalSocket()
        socket.connectToServer(SERVER_NAME)

        if socket.waitForConnected(500):
            # Une instance existe, envoyer le signal "show"
            socket.write(b"show")
            socket.waitForBytesWritten(1000)
            socket.disconnectFromServer()
            return True

        return False

    def start_server(self):
        """Démarre le serveur pour écouter les autres instances"""
        self._server = QLocalServer()

        # Supprimer l'ancien serveur s'il existe (crash précédent)
        QLocalServer.removeServer(SERVER_NAME)

        if not self._server.listen(SERVER_NAME):
            print(f"Impossible de démarrer le serveur: {self._server.errorString()}")
            return False

        self._server.newConnection.connect(self._on_new_connection)
        self._is_primary = True
        return True

    def set_window(self, window):
        """Définit la fenêtre principale"""
        self._window = window

    def _on_new_connection(self):
        """Appelé quand une autre instance essaie de se connecter"""
        socket = self._server.nextPendingConnection()
        if socket:
            socket.waitForReadyRead(1000)
            data = socket.readAll().data().decode()

            if data == "show" and self._window:
                # Restaurer et afficher la fenêtre
                self._window.showNormal()
                self._window.activateWindow()
                self._window.raise_()

            socket.disconnectFromServer()


def main():
    logger = get_logger()

    # Support High DPI pour écrans 4K (doit être avant QApplication)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Variable d'environnement pour le scaling
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = SingleInstanceApp(sys.argv)

    # Vérifier si une instance existe déjà
    if app.is_running():
        logger.info("Une instance est déjà en cours d'exécution - signal envoyé")
        sys.exit(0)

    # Démarrer le serveur pour cette instance
    if not app.start_server():
        logger.error("Impossible de démarrer le serveur d'instance unique")

    logger.info("SoundLowerer Plus démarré")

    # Police par défaut adaptée
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)

    w = MainWindow()
    app.set_window(w)
    w.show()

    exit_code = app.exec_()

    logger.info("SoundLowerer Plus fermé")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
