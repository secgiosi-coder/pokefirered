from pathlib import Path
import struct

SRC_W, SRC_H = 24, 20
DST_W, DST_H = 40, 35

src = Path("data/layouts/PalletTown/map.bin").read_bytes()
dst = [0x3296] * (DST_W * DST_H)  # grass

def get_src(x, y):
    return struct.unpack_from("<H", src, 2 * (y * SRC_W + x))[0]

def set_dst(x, y, tile):
    if 0 <= x < DST_W and 0 <= y < DST_H:
        dst[y * DST_W + x] = tile

def fill(x1, y1, x2, y2, tile):
    for y in range(y1, y2):
        for x in range(x1, x2):
            set_dst(x, y, tile)

def copy_rect(sx, sy, w, h, dx, dy):
    for y in range(h):
        for x in range(w):
            set_dst(dx + x, dy + y, get_src(sx + x, sy + y))

GRASS = 0x3296
PATH = 0x328E
FLOWER = 0x3009
FLOWER2 = 0x3011

# Base
fill(0, 0, DST_W, DST_H, GRASS)

# Sentieri principali
fill(17, 0, 23, 35, PATH)      # nord-sud
fill(8, 13, 32, 21, PATH)      # piazza centrale
fill(0, 14, 12, 18, PATH)      # accesso ovest Villaggio dei Fiori
fill(17, 27, 23, 35, PATH)     # uscita sud Percorso dei Fiori

# Edifici copiati da Pallet Town vanilla
copy_rect(4, 0, 7, 5, 5, 5)     # Casa Bacci
copy_rect(13, 0, 7, 5, 28, 5)   # Casa Cobelli
copy_rect(12, 5, 9, 5, 25, 16)  # Palestra Cagli / edificio grande

# Case extra
copy_rect(4, 0, 7, 5, 5, 22)
copy_rect(13, 0, 7, 5, 16, 22)
copy_rect(4, 0, 7, 5, 28, 25)

# Laghetto / decorazione acqua
copy_rect(7, 13, 4, 4, 4, 28)

# Aiuole / fiori
fill(2, 10, 8, 13, FLOWER)
fill(31, 10, 37, 13, FLOWER2)
fill(10, 25, 14, 29, FLOWER)
fill(24, 25, 28, 29, FLOWER2)

# Output
out = bytearray()
for tile in dst:
    out += struct.pack("<H", tile)

Path("data/layouts/LuganaEntroterra/map.bin").write_bytes(out)
print("Lugana Entroterra generated with buildings.")
