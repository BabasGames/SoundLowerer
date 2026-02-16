#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ── Extract version ──────────────────────────────────────────────
VERSION=$(python3 -c "exec(open('soundlowerer_plus/version.py').read()); print(VERSION)")
ARCH="amd64"
PKG_NAME="soundlowerer-plus"
DEB_NAME="${PKG_NAME}_${VERSION}_${ARCH}.deb"

echo "=== Building SoundLowerer Plus v${VERSION} .deb package ==="
echo ""

# ── Check prerequisites ─────────────────────────────────────────
MISSING=""
for cmd in pyinstaller dpkg-deb python3; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        MISSING="$MISSING $cmd"
    fi
done
if [ -n "$MISSING" ]; then
    echo "Error: missing commands:$MISSING"
    echo "Install pyinstaller with: pip install pyinstaller"
    exit 1
fi

# ── Clean previous build ────────────────────────────────────────
rm -rf build/ "dist/soundlowerer_plus" deb_build/

# ── PyInstaller build ───────────────────────────────────────────
echo ">>> Running PyInstaller (one-dir mode)..."
pyinstaller soundlowerer_plus_linux.spec --clean --noconfirm

BINARY_DIR="dist/soundlowerer_plus"
if [ ! -d "$BINARY_DIR" ]; then
    echo "Error: PyInstaller output directory not found at $BINARY_DIR"
    exit 1
fi
echo "    PyInstaller OK: $BINARY_DIR"

# ── Create deb staging directory (in /tmp for proper Unix permissions) ──
echo ">>> Building .deb structure..."
STAGING=$(mktemp -d "/tmp/soundlowerer-deb-XXXXXX")
trap "rm -rf '$STAGING'" EXIT

mkdir -p "$STAGING/DEBIAN"
mkdir -p "$STAGING/opt/soundlowerer-plus"
mkdir -p "$STAGING/usr/bin"
mkdir -p "$STAGING/usr/share/applications"
mkdir -p "$STAGING/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$STAGING/usr/share/doc/soundlowerer-plus"
mkdir -p "$STAGING/etc/udev/rules.d"
mkdir -p "$STAGING/etc/sudoers.d"

# ── Copy application files ──────────────────────────────────────
cp -r "$BINARY_DIR"/. "$STAGING/opt/soundlowerer-plus/"
chmod 755 "$STAGING/opt/soundlowerer-plus/soundlowerer_plus"

# ── Install wrapper script in /usr/bin (runs via sudo for /dev/input access) ──
cp packaging/soundlowerer-plus-wrapper.sh "$STAGING/usr/bin/soundlowerer-plus"
chmod 755 "$STAGING/usr/bin/soundlowerer-plus"

# ── Generate 256x256 PNG icon ───────────────────────────────────
if [ -f "icon_source.png" ]; then
    python3 -c "
from PIL import Image
img = Image.open('icon_source.png')
img = img.resize((256, 256), Image.LANCZOS)
img.save('/tmp/soundlowerer_icon_256.png')
" 2>/dev/null && {
        cp /tmp/soundlowerer_icon_256.png "$STAGING/usr/share/icons/hicolor/256x256/apps/soundlowerer-plus.png"
        rm -f /tmp/soundlowerer_icon_256.png
        echo "    Icon generated from icon_source.png"
    } || {
        echo "    Warning: Pillow not installed, skipping icon generation (pip install Pillow)"
    }
else
    echo "    Warning: icon_source.png not found, skipping icon"
fi

# ── Copy desktop file ──────────────────────────────────────────
cp packaging/soundlowerer-plus.desktop "$STAGING/usr/share/applications/"

# ── Copy license ────────────────────────────────────────────────
if [ -f "LICENSE" ]; then
    cp LICENSE "$STAGING/usr/share/doc/soundlowerer-plus/copyright"
fi

# ── Copy udev rule (makes /dev/uinput accessible to input group) ──
cp packaging/udev/99-soundlowerer-input.rules "$STAGING/etc/udev/rules.d/"

# ── Copy sudoers rule (NOPASSWD for the binary) ──────────────────
cp packaging/sudoers/soundlowerer-plus "$STAGING/etc/sudoers.d/soundlowerer-plus"
chmod 440 "$STAGING/etc/sudoers.d/soundlowerer-plus"

# ── Calculate installed size (in KB) ────────────────────────────
INSTALLED_SIZE=$(du -sk "$STAGING" | cut -f1)

# ── Generate DEBIAN/control ─────────────────────────────────────
sed -e "s/@@VERSION@@/${VERSION}/" \
    -e "s/@@INSTALLED_SIZE@@/${INSTALLED_SIZE}/" \
    -e "s/@@ARCH@@/${ARCH}/" \
    packaging/DEBIAN/control.template > "$STAGING/DEBIAN/control"

# ── Copy maintainer scripts ────────────────────────────────────
cp packaging/DEBIAN/postinst "$STAGING/DEBIAN/postinst"
chmod 755 "$STAGING/DEBIAN/postinst"
cp packaging/DEBIAN/prerm "$STAGING/DEBIAN/prerm"
chmod 755 "$STAGING/DEBIAN/prerm"

# ── Set correct permissions for DEBIAN dir ──────────────────────
chmod 755 "$STAGING/DEBIAN"

# ── Build the .deb ──────────────────────────────────────────────
echo ">>> Building .deb package..."
mkdir -p dist
dpkg-deb --root-owner-group --build "$STAGING" "dist/${DEB_NAME}"

# ── Done ────────────────────────────────────────────────────────
echo ""
echo "=== Done! ==="
echo "Package: dist/${DEB_NAME}"
SIZE=$(du -sh "dist/${DEB_NAME}" | cut -f1)
echo "Size: ${SIZE}"
echo ""
echo "Install with: sudo dpkg -i dist/${DEB_NAME}"
echo "Remove with:  sudo dpkg -r soundlowerer-plus"
