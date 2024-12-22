import io
import requests
from exif import Image

def convert2DD(c):
    return round(c[0] + (c[1]/60) + (c[2]/3600), 6)

if __name__ == '__main__':
    with io.BytesIO() as buf:
        # response = requests.get('https://angara.net/files/track/2024/09/28/484.gpx')
        response = requests.get('https://nc.icc.ru/2nd.jpg')
        if response.status_code == 200:
            print(response.headers)
            buf.write(response.content)
            buf.seek(0)
            my_image = Image(buf)
            if my_image.has_exif:
                print(f"{my_image.gps_latitude}\t{my_image.gps_longitude}")
                lat = convert2DD(my_image.gps_latitude)
                lon = convert2DD(my_image.gps_longitude)
                print(f"{lat}{my_image.gps_latitude_ref}/{lon}{my_image.gps_longitude_ref}")

            else:
                print("А нету")
