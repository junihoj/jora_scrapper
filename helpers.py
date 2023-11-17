import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()
au_cities = []
ca_cities = []
us_cities = []
uk_cities = []
nz_cities = []
with open(f"{BASE_DIR}/au_cities.txt", encoding="utf8") as fp:
    for line in fp:
        au_cities.extend(line.strip().split(', '))

with open(f"{BASE_DIR}/ca_cities.txt", encoding="utf8") as fp:
    for line in fp:
        ca_cities.extend(line.strip().split(', '))

with open(f"{BASE_DIR}/nz_cities.txt", encoding="utf8") as fp:
    for line in fp:
        nz_cities.extend(line.strip().split(', '))

with open(f"{BASE_DIR}/uk_cities.txt", encoding="utf8") as fp:
    for line in fp:
        uk_cities.extend(line.strip().split(', '))

with open(f"{BASE_DIR}/us_cities.txt", encoding="utf8") as fp:
    for line in fp:
        us_cities.extend(line.strip().split(', '))