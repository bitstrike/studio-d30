# TODO

## HTML/CSS Layout
- [x] Create single-page HTML structure (left panel controls, right panel preview, bottom status bar)
- [x] Style controls panel (icon upload, text inputs, font picker, font size picker, label size dropdown)
- [x] Style label preview canvas (proportions update based on selected label size)
- [x] Style status bar
- [x] Connect and Print buttons

## Canvas Preview
- [x] Render live label preview on canvas as inputs change
- [x] Adaptive layout: arrange present elements dynamically (icon, top text, bottom text are all optional)
- [x] Icon only: centered on label
- [x] Single text row: vertically centered, full width (or beside icon if present)
- [x] Two text rows: split vertically (icon beside top row if present)
- [x] Support font face and size changes in preview
- [x] Update canvas proportions when label size dropdown changes
- [x] Scale preview for display while maintaining actual pixel ratio for print

## Icon Support
- [x] File picker for icon upload (PNG/SVG)
- [x] Drag-and-drop zone for icon upload
- [x] Render uploaded icon on canvas
- [x] Clear/remove icon option

## Font Support
- [x] List browser-available fonts in dropdown
- [x] File picker to upload a .ttf font file
- [x] Register uploaded font via FontFace API
- [x] Apply selected font to canvas text rendering

## Label Size
- [x] Dropdown with common D30 sizes: 12x22, 12x30, 12x40, 14x22, 14x30, 14x40, 14x50, 15x30 (mm)
- [x] Calculate dot dimensions from mm selection (203 DPI)
- [x] Resize canvas and preview when size changes

## BLE Communication
- [x] Connect button: Web Bluetooth scan and pair (acceptAllDevices, D30 does not advertise service UUID)
- [x] Track connection state and display in status bar
- [x] Handle disconnect/reconnect
- [x] Troubleshooting dialog on connection failure with step-by-step remedies

## Raster and Print
- [x] Print button (disabled until connected)
- [x] Convert canvas to 1-bit raster data
- [x] Build ESC/POS command sequence (preamble, GS v 0, raster payload)
- [x] Chunk and send over BLE characteristic
- [x] Show print progress in status bar
- [x] Fix: always use 96-dot (12-byte) printhead width regardless of tape size selection

## Polish
- [x] Error handling (BLE unavailable, connection lost, print failure)
- [x] Troubleshooting dialog for connection issues (Linux bluetoothctl steps)
- [x] Responsive layout: label preview scales down on narrow viewports, controls panel stays usable
- [x] Remove hardcoded BLE MAC address (use CLI arg in label.py, placeholder in troubleshooting)
- [ ] Help text in status bar for each action
- [ ] Test on Chrome with actual D30 hardware

## Templates
- [x] Save template button with name prompt dialog
- [x] Load template button with list of saved templates
- [x] Delete saved templates
- [x] Store in localStorage (persists across browser restarts)
- [x] Downscale icons to 96x96 before saving (keeps under localStorage size limit)
- [x] Store custom font as data URL for restore
