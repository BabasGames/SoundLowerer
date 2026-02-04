#!/usr/bin/env python3
"""
Script de build et release automatique pour SoundLowerer
Usage: python release.py [patch|minor|major|X.Y.Z]
"""

import os
import sys
import subprocess
import json
import re

VERSION_FILE = "soundlowerer_plus/version.py"
SPEC_FILE = "soundlowerer_plus.spec"
EXE_NAME = "soundlowerer_plus.exe"
REPO = "BabasGames/SoundLowerer"


def get_current_version():
    """Lit la version actuelle depuis version.py"""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            content = f.read()
            match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    return "1.0.0"


def parse_version(version_str):
    """Parse une version X.Y.Z en tuple"""
    parts = version_str.split('.')
    return [int(p) for p in parts[:3]] + [0] * (3 - len(parts))


def increment_version(current, bump_type):
    """Incrémente la version selon le type"""
    major, minor, patch = parse_version(current)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        # Version explicite fournie
        return bump_type


def save_version(version):
    """Sauvegarde la nouvelle version dans version.py"""
    content = f'VERSION = "{version}"\n'
    os.makedirs(os.path.dirname(VERSION_FILE), exist_ok=True)
    with open(VERSION_FILE, 'w') as f:
        f.write(content)
    print(f"Version mise à jour: {version}")


def run_command(cmd, check=True):
    """Exécute une commande shell"""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        print(f"Erreur: commande échouée avec code {result.returncode}")
        sys.exit(1)
    return result


def build():
    """Build l'exe avec PyInstaller"""
    print("\n=== Building exe ===")
    run_command("pyinstaller soundlowerer_plus.spec --clean --noconfirm")

    exe_path = os.path.join("dist", EXE_NAME)
    if os.path.exists(exe_path):
        print(f"Build réussi: {exe_path}")
        return exe_path
    else:
        print("Erreur: exe non trouvé après build")
        sys.exit(1)


def git_commit_and_tag(version):
    """Commit les changements et crée un tag"""
    print("\n=== Git commit & tag ===")

    run_command(f"git add {VERSION_FILE}")
    run_command(f'git commit -m "Bump version to {version}"', check=False)
    run_command(f"git tag -a v{version} -m \"Release v{version}\"")
    run_command("git push")
    run_command("git push --tags")


def create_github_release(version, exe_path):
    """Crée une release GitHub avec gh CLI"""
    print("\n=== Creating GitHub release ===")

    # Vérifier si gh est installé
    result = run_command("gh --version", check=False)
    if result.returncode != 0:
        print("GitHub CLI (gh) non installé. Installe-le avec: winget install GitHub.cli")
        print(f"Tu peux créer la release manuellement sur https://github.com/{REPO}/releases")
        return

    # Créer la release
    notes = f"""## SoundLowerer v{version}

### Downloads
- **soundlowerer_plus.exe** - Windows executable (run as Administrator for games)

### Notes
> Windows SmartScreen may show a warning. Click "More info" > "Run anyway".
"""

    cmd = f'gh release create v{version} "{exe_path}" --title "SoundLowerer v{version}" --notes "{notes}"'
    run_command(cmd)

    print(f"\nRelease créée: https://github.com/{REPO}/releases/tag/v{version}")


def main():
    # Déterminer le type de bump
    if len(sys.argv) < 2:
        bump_type = "patch"
        print("Usage: python release.py [patch|minor|major|X.Y.Z]")
        print("Défaut: patch")
    else:
        bump_type = sys.argv[1]

    # Obtenir et incrémenter la version
    current = get_current_version()
    print(f"Version actuelle: {current}")

    new_version = increment_version(current, bump_type)
    print(f"Nouvelle version: {new_version}")

    # Confirmation
    response = input(f"\nContinuer avec v{new_version}? [y/N] ")
    if response.lower() != 'y':
        print("Annulé")
        sys.exit(0)

    # Sauvegarder la version
    save_version(new_version)

    # Build
    exe_path = build()

    # Git
    git_commit_and_tag(new_version)

    # GitHub release
    create_github_release(new_version, exe_path)

    print(f"\n=== Release v{new_version} terminée! ===")


if __name__ == "__main__":
    main()
