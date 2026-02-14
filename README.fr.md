# SoundLowerer Plus

🇬🇧 [Read in English](README.md)

Une application multi-plateforme (Windows & Linux) pour baisser automatiquement le volume de certaines applications avec des raccourcis clavier.

## Fonctionnalités

### Fonctionnalités de base
- **Raccourcis personnalisés** - Assignez n'importe quel raccourci clavier
- **Contrôle par application** - Ciblez des applications spécifiques (Spotify, Discord, jeux, etc.)
- **Deux modes** :
  - **Hold** - Maintenez la touche pour réduire le volume
  - **Toggle** - Appuyez une fois pour réduire, encore pour restaurer
- **Transitions douces** - Durée et courbe de fondu configurables (linéaire/exponentielle)
- **Mode whitelist** - Baissez TOUT sauf les applications sélectionnées
- **Services multiples** - Créez différents profils selon vos besoins
- **Même raccourci** - Utilisez un raccourci pour contrôler plusieurs apps
- **Import/Export** - Partagez vos configurations en fichiers `.slp`
- **Barre des tâches** - Fonctionne discrètement avec icône active/inactive
- **Auto-restauration** - Les services reprennent automatiquement au démarrage
- **Bilingue** - Interface française et anglaise
- **Thème sombre/clair**
- **Raccourcis clavier** - Suppr, Entrée, Espace, Ctrl+Entrée pour gérer les services
- **Recherche de services** - Filtrez les services par nom
- **Glisser-déposer** - Réorganisez les services par glisser-déposer
- **Slider dynamique** - La couleur change selon le niveau de réduction (vert/cyan/orange)
- **Liste enrichie** - Affiche le % de réduction, le mode et le raccourci d'un coup d'oeil
- **Boutons d'action fixes** - Toujours visibles en bas, sans scroller
- **Listes d'apps redimensionnables** - Glissez pour agrandir les zones de sélection
- **Détection de conflits en temps réel** - Avertit immédiatement si un raccourci est déjà utilisé
- **Validation des entrées** - Empêche les noms dupliqués, les horaires invalides
- **Tout arrêter depuis le tray** - Coupe tous les services actifs depuis la barre des tâches
- **Pulse visuel** - L'indicateur de statut clignote quand un raccourci est déclenché
- **Polling intelligent** - Met en pause le scan en arrière-plan quand l'app est minimisée

### Fonctionnalités avancées (activer dans Paramètres)
- **Profils** - Sauvegardez/chargez des ensembles de services
- **Démarrer au login** - Lancement automatique au démarrage
- **Sauvegarde auto** - Sauvegarde automatique de votre configuration
- **Statistiques** - Suivez la fréquence d'utilisation de chaque service
- **Vérification des mises à jour** - Vérifiez les nouvelles versions sur GitHub
- **Volume par défaut au démarrage** - Remet les applications au volume spécifié au lancement
- **Planification horaire** - Démarre/arrête automatiquement les services selon l'heure et le jour
- **Détection de jeux** - Démarre automatiquement les services quand un jeu est détecté
- **Réinitialisation** - Restaure tous les paramètres par défaut

## Installation

### Depuis les Releases (Windows)
1. Téléchargez le dernier `soundlowerer_plus.exe` depuis [Releases](../../releases)
2. Lancez l'exécutable
3. **Lancez en Administrateur** pour que les raccourcis fonctionnent dans les jeux

> **Note** : Windows SmartScreen peut afficher un avertissement au premier lancement car l'application n'est pas signée avec un certificat payant. C'est normal pour les logiciels indépendants. Cliquez sur **"Informations complémentaires"** puis **"Exécuter quand même"** pour continuer. L'application est open source et sans danger.

### Depuis les sources (Windows & Linux)
```bash
# Cloner le dépôt
git clone https://github.com/BabasGames/SoundLowerer.git
cd SoundLowerer

# Installer les dépendances
pip install -r soundlowerer_plus/requirements.txt

# Lancer
python soundlowerer_plus/main.py
```

> **Note Linux** : La bibliothèque `keyboard` nécessite des privilèges élevés pour les raccourcis globaux. Lancez avec `sudo` ou ajoutez votre utilisateur au groupe `input` :
> ```bash
> sudo usermod -aG input $USER
> # Déconnectez-vous puis reconnectez-vous, puis :
> python soundlowerer_plus/main.py
> ```

### Compiler l'exécutable
```bash
pip install pyinstaller
# Windows
pyinstaller soundlowerer_plus.spec --clean
# Linux
pyinstaller soundlowerer_plus_linux.spec --clean
```

## Utilisation

1. **Créer un service** :
   - Entrez un nom
   - Cliquez sur "Enregistrer..." et appuyez sur votre raccourci
   - Sélectionnez les applications cibles (ou ajoutez-en manuellement)
   - Ajustez le % de réduction, le mode et les paramètres de fondu

2. **Ajoutez le service** en cliquant sur "Nouveau service" (toujours visible en bas)

3. **Démarrez le service** en double-cliquant dessus dans la liste

4. **Utilisez votre raccourci** pour contrôler le volume !

## Configuration requise

- Windows 10/11 ou Linux (PulseAudio/PipeWire)
- Python 3.8+ (si lancé depuis les sources)

### Dépendances
- PyQt5
- keyboard
- pycaw (Windows)
- pulsectl (Linux)
- psutil

## Capture d'écran

<img width="1495" height="1055" alt="SoundLowerer Plus 08_02_2026 22_51_37" src="https://github.com/user-attachments/assets/5e5ea3d8-5c7e-4b06-be4c-a7226a1b69ce" />

## Licence

Licence MIT - Voir [LICENSE](LICENSE) pour les détails.

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou soumettre des pull requests.
