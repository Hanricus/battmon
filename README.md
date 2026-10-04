# battmon

A small floating battery monitor for Windows laptops, with charge limit (cutoff) control on supported Dell machines.

Made by [Abdul Shakir Hakim](https://www.linkedin.com/in/abdulshakirhakim/).

## Features

- Floating always-on-top widget with battery percentage, live state (charging, cutoff/hold, on battery) and a history graph
- Battery details: voltage, charge rate, capacity, health and cycle count
- Charge limit control (50%, 80%, 90%) on Dell laptops through the Dell BIOS WMI interface
- Works on any Windows laptop as a monitor. Charge control is Dell only for now
- Startup system check that detects the battery, laptop brand, admin rights, BIOS interface and BIOS admin password. Click "System check" in the widget to see the report
- English and Malay (click EN/MY in the header, your choice is remembered)
- Compact mode, system tray icon, and an hourly update check against GitHub Releases

## Requirements

- Windows 10 or 11
- Python 3.9+
- Optional: `pip install pystray pillow` for the tray icon
- For charge limit control: a Dell laptop that exposes `root\dcim\sysman\biosattributes`. The app asks for administrator rights (UAC) only on Dell machines. Changes apply immediately, no restart needed

## Run

```
pythonw battmon.pyw
```

Or double-click `battmon.pyw`.

## Other laptop brands

Every brand uses its own BIOS or driver interface for charge limits, so battmon only controls Dell for now. On other brands it runs as a monitor and points you to the vendor tool (for example Lenovo Vantage, MyASUS or the battery setting in HP BIOS). Pull requests and issues for other brands are welcome.

## Updates

battmon checks the latest GitHub Release once an hour. When a newer tag exists it shows a banner. Click it and confirm, and battmon replaces its own `battmon.pyw` (the old file is kept as `battmon.pyw.bak`) and restarts.

## Custom logo

Run `python make_logo.py` next to your own `Media.jfif`, then paste the result into `LOGO_B64` in `battmon.pyw`.

## Disclaimer

On Dell laptops this tool writes battery charge settings to the BIOS through the Dell WMI interface. Only the charge configuration attributes are changed, but use it at your own risk. Company laptops may have IT policies or a BIOS admin password that block or override these settings.

## License

MIT
