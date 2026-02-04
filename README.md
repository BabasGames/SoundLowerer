# SoundLowerer

A Windows application to automatically lower the volume of specific applications using keyboard shortcuts.

## Features

- **Custom hotkeys** - Assign any keyboard shortcut to control volume
- **Per-app control** - Target specific applications (Spotify, Discord, games, etc.)
- **Two modes**:
  - **Hold** - Keep the key pressed to reduce volume
  - **Toggle** - Press once to reduce, press again to restore
- **Smooth transitions** - Configurable fade duration and curve (linear/exponential)
- **Whitelist mode** - Lower ALL apps EXCEPT selected ones
- **Multiple services** - Create different profiles for different use cases
- **Same hotkey support** - Use one shortcut to control multiple apps
- **Import/Export** - Share your configurations as `.slp` files
- **System tray** - Runs quietly in the background
- **Auto-restore** - Services resume automatically on startup
- **Bilingual** - French and English interface
- **Dark/Light theme**

## Installation

### From Release
1. Download the latest `soundlowerer_plus.exe` from [Releases](../../releases)
2. Run the executable
3. **Run as Administrator** for hotkeys to work in games

### From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/SoundLowerer.git
cd SoundLowerer

# Install dependencies
pip install -r requirements.txt

# Run
python soundlowerer_plus/main.py
```

### Build Executable
```bash
pip install pyinstaller
pyinstaller soundlowerer_plus.spec --clean
```

## Usage

1. **Create a service**:
   - Enter a name
   - Select target applications (or add manually)
   - Click "Record..." and press your desired hotkey
   - Adjust reduction %, mode, and fade settings

2. **Add the service** by clicking "New service"

3. **Start the service** by double-clicking it or using the ▶ button

4. **Use your hotkey** to control the volume!

## Requirements

- Windows 10/11
- Python 3.8+ (if running from source)

### Dependencies
- PyQt5
- pycaw
- comtypes
- keyboard
- pywin32

## Screenshots

![Main Interface](screenshots/main.png)

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
