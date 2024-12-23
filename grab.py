from time import sleep
import requests


if __name__ == '__main__':

    track_number = 490
    track_filename = f'{track_number}.gpx'

    # for year in range(2024,2018,-1):
    for month in range(12,5,-1):
        for day in range(31,0,-1):
            ffile = f'https://angara.net/files/track/2024/{month:02d}/{day:02d}/{track_filename}'
            print(f'Search: {ffile}')
            sleep(1)
            response = requests.get(ffile)
            while response.status_code == 200:
                open(f'angara/{track_filename}', 'wb').write(response.content)
                sleep(1)
                print(f'OK: {ffile}')
                track_number -= 1
                if track_number == 458:
                    exit(0)
                track_filename = f'{track_number}.gpx'
                ffile = f'https://angara.net/files/track/2024/{month:02d}/{day:02d}/{track_filename}'
                response = requests.get(ffile)