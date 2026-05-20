from pathlib import Path
import struct

DST_W, DST_H = 40, 35

SOURCES = {
    "PalletTown": (24, 20, Path("tools_custom/pallet_source_map.bin")),
    "ViridianCity": (40, 36, Path("data/layouts/ViridianCity/map.bin")),
    "PewterCity": (50, 40, Path("data/layouts/PewterCity/map.bin")),
}

src_cache = {}

def read_source(name):
    if name not in src_cache:
        w, h, path = SOURCES[name]
        data = path.read_bytes()
        src_cache[name] = (w, h, data)
    return src_cache[name]

def get_src(name, x, y):
    w, h, data = read_source(name)
    return struct.unpack_from("<H", data, 2 * (y * w + x))[0]

def set_dst(x, y, tile):
    if 0 <= x < DST_W and 0 <= y < DST_H:
        dst[y * DST_W + x] = tile

def fill(x1, y1, x2, y2, tile):
    for y in range(y1, y2):
        for x in range(x1, x2):
            set_dst(x, y, tile)

def copy_rect(source, sx, sy, w, h, dx, dy):
    for y in range(h):
        for x in range(w):
            set_dst(dx + x, dy + y, get_src(source, sx + x, sy + y))

GRASS = 0x3296
PATH = 0x328E

dst = [GRASS] * (DST_W * DST_H)

# Strade semplici
fill(18, 0, 22, 35, PATH)
fill(4, 12, 36, 17, PATH)
fill(4, 25, 36, 30, PATH)
fill(13, 15, 27, 25, PATH)
fill(0, 14, 18, 17, PATH)
fill(18, 30, 22, 35, PATH)

# Case da Pallet originale, coordinate verificate
copy_rect("PalletTown", 5, 3, 5, 5, 5, 5)       # Casa Bacci
copy_rect("PalletTown", 14, 3, 5, 5, 28, 5)     # Casa placeholder futura rivale

copy_rect("PalletTown", 5, 3, 5, 5, 6, 22)      # Casa esplorabile 1
copy_rect("PalletTown", 14, 3, 5, 5, 28, 22)    # Casa esplorabile 2
copy_rect("PalletTown", 5, 3, 5, 5, 17, 26)     # Casa esplorabile 3

# Edificio grande da Pallet originale
copy_rect("PalletTown", 13, 9, 7, 5, 4, 18)     # Palestra placeholder

# Center/Mart placeholder case diverse
copy_rect("PalletTown", 14, 3, 5, 5, 13, 9)     # Centro placeholder
copy_rect("PalletTown", 5, 3, 5, 5, 23, 9)      # Mart placeholder

# Output sulla mappa effettivamente usata
out = bytearray()
for tile in dst:
    out += struct.pack("<H", tile)

Path("data/layouts/PalletTown/map.bin").write_bytes(out)
print("Lugana Entroterra generated from verified source maps.")

