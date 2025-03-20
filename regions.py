import os
from gpxindex.index import load_gpx, get_trk_season

if __name__ == '__main__':
    with open("enisey/sea.txt", "w") as ss:
        for fname in os.listdir("angara-w"):
            gpx = load_gpx(f"angara-w/{fname}")
            ss.write(f"{fname}: {get_trk_season(gpx)}\n")



