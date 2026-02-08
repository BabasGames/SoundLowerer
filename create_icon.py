"""
Script pour créer les icônes .ico de l'application
Nécessite: pip install Pillow
"""
import os

try:
    from PIL import Image

    sizes = [16, 24, 32, 48, 64, 128, 256]

    for png_path, ico_path in [
        ("icon_source.png", "soundlowerer_plus/icons/app.ico"),
        ("icon_source_active.png", "soundlowerer_plus/icons/app_active.ico"),
    ]:
        if not os.path.exists(png_path):
            print(f"Ignoré (fichier absent): {png_path}")
            continue

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
