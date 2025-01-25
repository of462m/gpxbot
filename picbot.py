from exif import Image
from Levenshtein import distance as L_distance
from Levenshtein import jaro as L_jaro
from Levenshtein import jaro_winkler as L_jaro_winkler
from jaro import jaro_winkler_metric

def convert2DD(c):
    return round(c[0] + (c[1]/60) + (c[2]/3600), 6)





if __name__ == '__main__':
    cmp = ("пиком", "пик")
    print(L_distance(cmp[0], cmp[1], weights=(1,1,1)))
    print(L_jaro(cmp[0], cmp[1]))
    print(L_jaro_winkler(cmp[0], cmp[1]))
    print(jaro_winkler_metric(cmp[0], cmp[1]))
    exit(0)
    fname = "tmp/2nd.jpg"
    with open(fname, 'rb') as image_file:
        my_image = Image(image_file)
        if my_image.has_exif:
            print(f"{my_image.gps_latitude}\t{my_image.gps_longitude}")
            lat = convert2DD(my_image.gps_latitude)
            lon = convert2DD(my_image.gps_longitude)
            print(f"{lat}{my_image.gps_latitude_ref}/{lon}{my_image.gps_longitude_ref}")
        else:
            print("А нету")
