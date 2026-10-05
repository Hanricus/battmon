# battmon

A small floating battery monitor for Windows laptops, with charge limit (cutoff) control on supported Dell machines.

Made by Me[Abdul Shakir Hakim](https://www.linkedin.com/in/abdulshakirhakim/).

## Features

- Floating always-on-top widget with battery percentage, live state (charging, cutoff/hold, on battery) and a history graph
- Battery details: voltage, charge rate, capacity, health and cycle count
- Charge limit control (50%, 80%, 90%) on Dell laptops through the Dell BIOS WMI interface
- Works on any Windows laptop as a monitor. Charge control is Dell only for now
- Battery report: laptop and battery info, health verdict, charge cutoff/bypass support for your brand, where to find your brand's own tool, and observed cutoff behaviour from battmon's own log. Save it as HTML or text
- Startup checks: battery present, laptop brand, admin rights, BIOS interface, BIOS admin password, and tray support
- The close button hides battmon to the system tray instead of quitting. If the tray packages are missing, battmon offers to install them
- English and Malay (click EN/MY in the header, your choice is remembered)
- Compact mode, and an hourly update check against GitHub Releases

## Download

Clone the repo (needs Git):

```
git clone https://github.com/Hanricus/battmon.git
cd battmon
```

Or just download the script with PowerShell:

```
Invoke-WebRequest -Uri https://raw.githubusercontent.com/Hanricus/battmon/main/battmon.pyw -OutFile battmon.pyw
```

## Requirements

- Windows 10 or 11
- Python 3.9+
- Tray icon packages `pystray` and `pillow` (battmon offers to install them on first run)
- For charge limit control: a Dell laptop that exposes `root\dcim\sysman\biosattributes`. The app asks for administrator rights (UAC) only on Dell machines. Changes apply immediately, no restart needed

## Run

```
pythonw battmon.pyw
```

Or double-click `battmon.pyw`.

## Other laptop brands

Every brand uses its own BIOS or app for charge limits, so battmon only controls Dell for now. On other brands it runs as a monitor. The battery report tells you what is usually available for your brand (for example HP Battery Health Manager in the BIOS, Lenovo Vantage Conservation Mode, MyASUS Battery Care) and whether the vendor tool is installed. It depends on the exact model, so treat it as a pointer, not a guarantee. Issues and pull requests for other brands are welcome.

True bypass charging (battery fully out of the power path) is rare and battmon cannot detect it. Cutoff behaviour can be spotted from the log: if the laptop holds below 100% while plugged in, the report says so.

## Updates

battmon checks the latest GitHub Release once an hour. When a newer tag exists it shows a banner. Click it and confirm, and battmon replaces its own `battmon.pyw` (the old file is kept as `battmon.pyw.bak`) and restarts.

## Custom logo

Run `python make_logo.py` next to your own `Media.jfif`, then paste the result into `LOGO_B64` in `battmon.pyw`.

## Disclaimer

On Dell laptops this tool writes battery charge settings to the BIOS through the Dell WMI interface. Only the charge configuration attributes are changed, but use it at your own risk. Company laptops may have IT policies or a BIOS admin password that block or override these settings.

## License

MIT
