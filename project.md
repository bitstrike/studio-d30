# Phomemo D30 Label Printer

Web-based label designer and printer for the Phomemo D30 thermal label printer over BLE.

## Architecture

Single-file HTML/CSS/JS application using the Web Bluetooth API. No build step, no dependencies, no backend. Served from localhost or any HTTPS host (Web Bluetooth requirement).

### File structure

```
studio-d30/
  index.html        # App (HTML + embedded CSS + JS)
  label.py          # CLI print script (Python/Bleak) - takes BLE address as argument
  project.md        # This file
  wireframe.md      # UI wireframe
  todo.md           # Implementation checklist
  README.md         # User-facing documentation
  images/           # Screenshots for README
```

## Features

### Label composition
- Icon upload (optional) - file picker or drag-and-drop, displayed left-aligned on the top row
- Top text input (optional, displayed right of the icon or full width if no icon)
- Bottom text input (optional, full width, second row)
- Font face selection (browser-available fonts, or upload a .ttf file)
- Font size selection
- Label size dropdown (see sizes below)

All content fields (icon, top text, bottom text) are optional. Any combination is valid. The layout adapts dynamically - elements center and expand to fill available space based on what is present.

### Preview
- Live canvas preview at actual label proportions (96x320 dots)
- Two-row layout matching print output
- Responsive: preview scales down on narrow viewports while controls remain fully visible

### Printing
- Connect button (BLE pairing/reconnect)
- Print button (rasterize and send)
- Rasterize canvas to ESC/POS format (GS v 0 command)
- Send over BLE in chunks
- Troubleshooting dialog on connection failure (step-by-step remedies)

### BLE notes
- The D30 does not advertise its service UUID, so the app uses `acceptAllDevices` and lists all nearby BLE devices for the user to pick
- Only one GATT connection is allowed at a time - the OS must not have an active connection to the printer
- On Linux, stale BlueZ pairings can block Web Bluetooth connections (remove via `bluetoothctl remove`)

### Status bar
- Connection state (disconnected/connecting/connected)
- Print progress or errors
- Help text for current action

### Templates
- Save current label configuration (text, font, size, icon) as a named template
- Load saved templates from a list
- Delete saved templates
- Persists across browser restarts via localStorage
- Icons are downscaled to 96x96 before storing to stay within localStorage limits
- Custom fonts are stored as data URLs for full restore

## Label sizes

Selectable from a dropdown. Common D30-compatible tape sizes (width x length in mm):

| Size (mm) | Notes |
|-----------|-------|
| 12 x 22 | Small square-ish |
| 12 x 30 | Medium rectangular |
| 12 x 40 | Standard rectangular |
| 14 x 22 | Wider, short |
| 14 x 30 | Wider, medium |
| 14 x 40 | Wider, long |
| 14 x 50 | Wider, extra long |
| 15 x 30 | Widest, medium |

The printhead is fixed at 96 dots wide (12 bytes) regardless of tape width. The tape width selection (12mm, 14mm, 15mm) affects the preview layout only - the printable area is always 96 dots. Label length (feed direction) is calculated from the length dimension at 203 DPI.

## Printer details

| Parameter | Value |
|-----------|-------|
| BLE service UUID | `0000ff00-0000-1000-8000-00805f9b34fb` |
| BLE write characteristic | `0000ff02-0000-1000-8000-00805f9b34fb` |
| Printhead width | 96 dots (12 bytes) - fixed, independent of tape width |
| Raster format | ESC/POS GS v 0 |

## Browser support

Requires Web Bluetooth API: Chrome, Edge, Opera. Not supported in Firefox or Safari.

## CLI Script (label.py)

A standalone Python script for printing from the command line using Bleak. Takes the printer's BLE address as the first argument:

```
python3 label.py <BLE_ADDRESS> "Label text"
```

## Reference

- [Wireframe](wireframe.md)
- [TODO](todo.md)
