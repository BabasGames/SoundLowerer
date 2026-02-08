"""
Script pour créer l'icône .ico de l'application
Nécessite: pip install Pillow cairosvg
"""
import os

try:
    from PIL import Image
    import cairosvg
    import io

    # Chemin du SVG source et de l'ICO de destination
    svg_path = "soundlowerer_plus/icons/tray.svg"
    ico_path = "soundlowerer_plus/icons/app.ico"

    # Tailles pour l'icône Windows
    sizes = [16, 24, 32, 48, 64, 128, 256]

    images = []
    for size in sizes:
        # Convertir SVG en PNG en mémoire
        png_data = cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)
        img = Image.open(io.BytesIO(png_data))
        # Convertir en RGBA si nécessaire
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        images.append(img)

    # Sauvegarder en .ico (la première image est utilisée, les autres sont incluses)
    images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])

    print(f"Icône créée: {ico_path}")

except ImportError as e:
    print(f"Erreur: {e}")
    print("\nInstallez les dépendances avec:")
    print("pip install Pillow cairosvg")
except Exception as e:
    print(f"Erreur: {e}")
