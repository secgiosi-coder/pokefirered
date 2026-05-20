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
from pathlib import Path
import struct

SRC_W, SRC_H = 24, 20
DST_W, DST_H = 40, 35

src = Path("data/layouts/PalletTown/map.bin").read_bytes()
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
WATER = 0x3281

# Base
fill(0, 0, DST_W, DST_H, GRASS)

# Acqua Lago di Garda lato destro e canale basso
fill(36, 0, 40, 35, WATER)
fill(0, 31, 40, 35, WATER)
fill(0, 24, 4, 31, WATER)

# Sentieri principali
fill(18, 0, 22, 31, PATH)      # strada nord-sud centrale
fill(4, 12, 36, 17, PATH)      # strada orizzontale alta
fill(4, 25, 36, 30, PATH)      # strada orizzontale bassa
fill(0, 14, 18, 17, PATH)      # uscita ovest Villaggio dei Fiori
fill(22, 6, 36, 10, PATH)      # accesso casa alta destra
fill(28, 10, 36, 25, PATH)     # strada destra verticale
fill(16, 17, 24, 25, PATH)     # piazza centrale

# Piazza centrale più grande
fill(13, 15, 27, 24, PATH)

# Edifici principali copiati da Pallet Town
copy_rect(4, 0, 7, 5, 5, 5)      # 1 Casa Bacci
copy_rect(13, 0, 7, 5, 28, 2)    # 2 Placeholder futura casa rivale
copy_rect(4, 0, 7, 5, 6, 22)     # 5 Casa esplorabile
copy_rect(13, 0, 7, 5, 28, 22)   # 6 Casa esplorabile
copy_rect(4, 0, 7, 5, 17, 25)    # 7 Casa esplorabile

# Centro e Mart usando case vanilla come placeholder grafico
copy_rect(4, 0, 7, 5, 13, 10)    # 3 Pokémon Center placeholder
copy_rect(13, 0, 7, 5, 22, 10)   # 4 Poké Mart placeholder

# Palestra Cagli edificio grande
copy_rect(12, 5, 9, 5, 4, 20)    # 8 Palestra di Cagli

# Aiuole e zone verdi
fill(1, 3, 12, 5, FLOWER)
fill(23, 3, 28, 5, FLOWER2)
fill(30, 12, 35, 14, FLOWER)
fill(5, 17, 13, 20, FLOWER2)
fill(14, 24, 17, 29, FLOWER)
fill(25, 24, 28, 29, FLOWER2)

# Piccolo canale/laghetto decorativo centrale basso
fill(12, 24, 18, 25, WATER)
fill(23, 24, 29, 25, WATER)

# Output
out = bytearray()
for tile in dst:
    out += struct.pack("<H", tile)

Path("data/layouts/LuganaEntroterra/map.bin").write_bytes(out)
print("Lugana Entroterra generated - Build 0.1 city layout.")
