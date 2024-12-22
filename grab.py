from time import sleep
import requests

track_number = 458
track_filename = f'{track_number}.gpx'

for year in range(2024,2018,-1):
    for month in range(12,0,-1):
        for day in range(31,0,-1):
            ffile = f'https://angara.net/files/track/{year}/{month:02d}/{day:02d}/{track_filename}'
            print(f'Search: {ffile}')
            response = requests.get(ffile)
            while response.status_code == 200:
                print(ffile)
                # open(f'angara/{track_filename}', 'wb').write(response.content)
                sleep(1)
                print(f'OK: {ffile}')
                track_number = track_number - 1
                if track_number < 2:
                    exit(0)
                track_filename = f'{track_number}.gpx'
                # ffile = f'https://angara.net/files/track/{year}/{month:02d}/{day:02d}/{track_filename}'
                response = requests.get(ffile)