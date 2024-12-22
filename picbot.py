from exif import Image

def convert2DD(c):
    return round(c[0] + (c[1]/60) + (c[2]/3600), 6)

if __name__ == '__main__':
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
