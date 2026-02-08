"""
Script pour créer l'icône .ico de l'application
Nécessite: pip install Pillow
"""
import os

try:
    from PIL import Image

    # Source PNG et destination ICO
    png_path = "icon_source.png"
    ico_path = "soundlowerer_plus/icons/app.ico"

    # Tailles pour l'icône Windows
    sizes = [16, 24, 32, 48, 64, 128, 256]

    src = Image.open(png_path)
    if src.mode != 'RGBA':
        src = src.convert('RGBA')

    images = []
    for size in sizes:
        img = src.resize((size, size), Image.LANCZOS)
        images.append(img)

    images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])

    print(f"Icône créée: {ico_path}")

except ImportError as e:
    print(f"Erreur: {e}")
    print("\nInstallez les dépendances avec:")
    print("pip install Pillow")
except Exception as e:
    print(f"Erreur: {e}")
