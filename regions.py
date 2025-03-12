import os
from index import load_gpx, get_gpx_season

if __name__ == '__main__':
    with open("enisey/sea.txt", "w") as ss:
        for fname in os.listdir("angara-w"):
            gpx = load_gpx(f"angara-w/{fname}")
            ss.write(f"{fname}: {get_gpx_season(gpx)}\n")



