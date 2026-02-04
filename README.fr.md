# SoundLowerer

🇬🇧 [Read in English](README.md)

Une application Windows pour baisser automatiquement le volume de certaines applications avec des raccourcis clavier.

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
- **Barre des tâches** - Fonctionne discrètement avec indicateur coloré
- **Auto-restauration** - Les services reprennent automatiquement au démarrage
- **Bilingue** - Interface française et anglaise
- **Thème sombre/clair**
- **Raccourcis clavier** - Suppr, Entrée, Espace pour gérer les services
- **Recherche de services** - Filtrez les services par nom
- **Glisser-déposer** - Réorganisez les services par glisser-déposer

### Fonctionnalités avancées (activer dans Paramètres)
- **Profils** - Sauvegardez/chargez des ensembles de services
- **Démarrer avec Windows** - Lancement automatique au démarrage
- **Sauvegarde auto** - Sauvegarde automatique de votre configuration
- **Statistiques** - Suivez la fréquence d'utilisation de chaque service
- **Vérification des mises à jour** - Vérifiez les nouvelles versions sur GitHub
- **Volume par défaut au démarrage** - Remet les applications au volume spécifié au lancement
- **Planification horaire** - Démarre/arrête automatiquement les services selon l'heure et le jour
- **Détection de jeux** - Démarre automatiquement les services quand un jeu est détecté

## Installation

### Depuis les Releases
1. Téléchargez le dernier `soundlowerer_plus.exe` depuis [Releases](../../releases)
2. Lancez l'exécutable
3. **Lancez en Administrateur** pour que les raccourcis fonctionnent dans les jeux

> **Note** : Windows SmartScreen peut afficher un avertissement au premier lancement car l'application n'est pas signée avec un certificat payant. C'est normal pour les logiciels indépendants. Cliquez sur **"Informations complémentaires"** puis **"Exécuter quand même"** pour continuer. L'application est open source et sans danger.

### Depuis les sources
```bash
# Cloner le dépôt
git clone https://github.com/BabasGames/SoundLowerer.git
cd SoundLowerer

# Installer les dépendances
pip install -r requirements.txt

# Lancer
python soundlowerer_plus/main.py
```

### Compiler l'exécutable
```bash
pip install pyinstaller
pyinstaller soundlowerer_plus.spec --clean
```

## Utilisation

1. **Créer un service** :
   - Entrez un nom
   - Sélectionnez les applications cibles (ou ajoutez-en manuellement)
   - Cliquez sur "Enregistrer..." et appuyez sur votre raccourci
   - Ajustez le % de réduction, le mode et les paramètres de fondu

2. **Ajoutez le service** en cliquant sur "Nouveau service"

3. **Démarrez le service** en double-cliquant dessus ou avec le bouton ▶

4. **Utilisez votre raccourci** pour contrôler le volume !

## Configuration requise

- Windows 10/11
- Python 3.8+ (si lancé depuis les sources)

### Dépendances
- PyQt5
- pycaw
- comtypes
- keyboard
- pywin32

## Capture d'écran

<img width="1089" height="993" alt="SoundLowerer Plus 04_02_2026 18_12_01" src="https://github.com/user-attachments/assets/c5162dae-39ff-40ef-bf46-d44ebda41ac1" />

## Licence

Licence MIT - Voir [LICENSE](LICENSE) pour les détails.

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou soumettre des pull requests.
