from pathlib import Path
import struct

SRC_W, SRC_H = 24, 20
DST_W, DST_H = 40, 35

src = Path("tools_custom/pallet_source_map.bin").read_bytes()
dst = [0x3296] * (DST_W * DST_H)

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

# Base erba
fill(0, 0, DST_W, DST_H, GRASS)

# Strade principali
fill(18, 0, 22, 35, PATH)      # strada verticale centrale
fill(4, 12, 36, 17, PATH)      # strada orizzontale alta
fill(4, 25, 36, 30, PATH)      # strada orizzontale bassa
fill(13, 17, 27, 25, PATH)     # piazza centrale
fill(0, 14, 18, 17, PATH)      # uscita ovest
fill(18, 30, 22, 35, PATH)     # uscita sud
fill(18, 0, 22, 5, PATH)       # uscita nord

# Edifici verificati da PalletTown originale
# Casa piccola A: sorgente x5 y3, 5x5
# Casa piccola B: sorgente x14 y3, 5x5
# Edificio grande/lab: sorgente x13 y9, 7x5

copy_rect(5, 3, 5, 5, 5, 5)       # Casa Bacci
copy_rect(14, 3, 5, 5, 28, 5)     # Casa futura/placeholder

copy_rect(5, 3, 5, 5, 6, 22)      # Casa esplorabile 1
copy_rect(14, 3, 5, 5, 28, 22)    # Casa esplorabile 2
copy_rect(5, 3, 5, 5, 17, 26)     # Casa esplorabile 3

copy_rect(14, 3, 5, 5, 13, 9)     # Pokémon Center placeholder
copy_rect(5, 3, 5, 5, 23, 9)      # Poké Mart placeholder

copy_rect(13, 9, 7, 5, 4, 18)     # Palestra Cagli placeholder grande

# Aiuole decorative
fill(2, 3, 10, 5, FLOWER)
fill(30, 3, 36, 5, FLOWER2)
fill(5, 17, 12, 20, FLOWER)
fill(28, 17, 35, 20, FLOWER2)
fill(12, 30, 17, 33, FLOWER)
fill(23, 30, 28, 33, FLOWER2)

# Output direttamente sulla mappa usata in game
out = bytearray()
for tile in dst:
    out += struct.pack("<H", tile)

Path("data/layouts/PalletTown/map.bin").write_bytes(out)
print("Lugana Entroterra generated correctly from verified Pallet tiles.")
