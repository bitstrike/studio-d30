#!/usr/bin/env python3
import asyncio
from bleak import BleakClient, BleakScanner
from PIL import Image, ImageDraw, ImageFont
import struct
import sys

ADDRESS = sys.argv[1] if len(sys.argv) > 1 else None
WRITE_CHAR = "0000ff02-0000-1000-8000-00805f9b34fb"

# D30 label dimensions (before rotation)
LABEL_WIDTH = 96
LABEL_HEIGHT = 320

def create_label_image(text, font_size=24):
    """Render text into a 1-bit image for the D30."""
    img = Image.new("1", (LABEL_HEIGHT, LABEL_WIDTH), 1)  # white background
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (LABEL_HEIGHT - tw) // 2
    y = (LABEL_WIDTH - th) // 2
    draw.text((x, y), text, font=font, fill=0)  # black text

    # Rotate 90° clockwise for printing
    img = img.rotate(-90, expand=True)
    return img

def image_to_raster(img):
    """Convert 1-bit image to raw raster bytes (1 = white, 0 = black in ESC/POS)."""
    width, height = img.size
    pixels = img.load()
    data = bytearray()

    for y in range(height):
        row = bytearray()
        for x in range(0, width, 8):
            byte = 0
            for bit in range(8):
                if x + bit < width:
                    # In ESC/POS raster: 1 = black dot
                    if pixels[x + bit, y] == 0:
                        byte |= (1 << (7 - bit))
            row.append(byte)
        data.extend(row)

    return bytes(data)

def build_print_command(img):
    """Build the full ESC/POS-like command sequence for the D30."""
    width, height = img.size
    width_bytes = width // 8

    commands = bytearray()
    # Preamble
    commands.extend(b"\x1f\x11\x24\x00")
    # Initialize
    commands.extend(b"\x1b\x40")
    # Raster bit image: GS v 0
    commands.extend(b"\x1d\x76\x30\x00")
    # Width in bytes (little-endian 16-bit)
    commands.extend(struct.pack("<H", width_bytes))
    # Height in dots (little-endian 16-bit)
    commands.extend(struct.pack("<H", height))
    # Raster data
    commands.extend(image_to_raster(img))

    return bytes(commands)

async def main():
    if not ADDRESS:
        print("Usage: label.py <BLE_ADDRESS> [text]")
        print("  e.g. label.py 78:C0:1B:AA:BB:CC \"Hello D30!\"")
        sys.exit(1)

    text = sys.argv[2] if len(sys.argv) > 2 else "Hello D30!"

    print(f"Creating label: '{text}'")
    img = create_label_image(text)
    payload = build_print_command(img)
    print(f"Payload size: {len(payload)} bytes")

    print("Scanning for printer...")
    device = await BleakScanner.find_device_by_address(ADDRESS, timeout=15)
    if not device:
        print("Printer not found. Wake it up and try again.")
        return

    print(f"Connecting to {device.name}...")
    async with BleakClient(device) as client:
        print("Connected. Sending print data...")

        # BLE has an MTU limit, send in chunks
        chunk_size = 20  # safe BLE chunk size
        for i in range(0, len(payload), chunk_size):
            chunk = payload[i:i + chunk_size]
            await client.write_gatt_char(WRITE_CHAR, chunk)
            await asyncio.sleep(0.01)

        print("Done! Label should be printing.")

asyncio.run(main())
