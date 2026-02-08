# SoundLowerer Plus

🇫🇷 [Lire en français](README.fr.md)

A Windows application to automatically lower the volume of specific applications using keyboard shortcuts.

## Features

### Basic Features
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
- **System tray** - Runs quietly in the background with active/inactive icon
- **Auto-restore** - Services resume automatically on startup
- **Bilingual** - French and English interface
- **Dark/Light theme**
- **Keyboard shortcuts** - Delete, Enter, Space, Ctrl+Enter to manage services
- **Service search** - Filter services by name
- **Drag & drop** - Reorder services by dragging
- **Dynamic slider** - Color changes based on reduction level (green/cyan/orange)
- **Enriched service list** - Shows reduction %, mode, and hotkey at a glance
- **Sticky action buttons** - Always visible at the bottom, no scrolling needed
- **Resizable app lists** - Drag to resize target app selection areas
- **Real-time hotkey conflict detection** - Warns immediately when a shortcut is already in use
- **Input validation** - Prevents duplicate names, invalid schedules
- **Stop all from tray** - Quickly stop every running service from the system tray
- **Visual pulse** - Status indicator flashes when a service hotkey is triggered
- **Smart polling** - Pauses background scanning when minimized to save resources

### Advanced Features (enable in Settings)
- **Profiles** - Save/load sets of services for different use cases
- **Start with Windows** - Launch automatically at startup
- **Auto backup** - Automatically backup your configuration
- **Usage statistics** - Track how often each service is used
- **Update checker** - Check for new versions on GitHub
- **Default volume on startup** - Reset specific apps to a defined volume when launching
- **Hourly scheduling** - Automatically start/stop services based on time and day
- **Game detection** - Auto-start services when a game is detected
- **Reset to defaults** - Restore all settings to factory values

## Installation

### From Release
1. Download the latest `soundlowerer_plus.exe` from [Releases](../../releases)
2. Run the executable
3. **Run as Administrator** for hotkeys to work in games

> **Note**: Windows SmartScreen may display a warning on first launch because the app is not signed with a paid certificate. This is normal for independent software. Click **"More info"** then **"Run anyway"** to proceed. The application is open source and safe to use.

### From Source
```bash
# Clone the repository
git clone https://github.com/BabasGames/SoundLowerer.git
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
   - Click "Record..." and press your desired hotkey
   - Select target applications (or add manually)
   - Adjust reduction %, mode, and fade settings

2. **Add the service** by clicking "New service" (always visible at the bottom)

3. **Start the service** by double-clicking it in the list

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

## Screenshot

<img width="1498" height="1094" alt="{64F8044F-5413-4EBE-9863-D9E2E4172BA4}" src="https://github.com/user-attachments/assets/7e0c4f0c-f577-47bc-aac2-3b3c4435e257" />

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

