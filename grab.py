from time import sleep
import requests


if __name__ == '__main__':

    # track_number = 499
    track_number = 493
    track_filename = f'{track_number}.gpx'

    for year in range(2024, 2018, -1):
        for month in range(12, 0, -1):
            for day in range(31, 0, -1):
                ffile = f'https://angara.net/files/track/{year}/{month:02d}/{day:02d}/{track_filename}'
                print(f'Search: {ffile}')
                sleep(1)
                response = requests.get(ffile)
                while response.status_code == 200:
                    with open(f'angara-w/{track_number:05d}.gpx', 'wb') as wf:
                        wf.write(response.content)
                    with open(f'angara-l/{track_number:05d}.href', 'w') as wl:
                        wl.write(f"{ffile}\n")
                    print(f"{track_number}.gpx found.")
                    sleep(1)
                    print(f'OK: {ffile}')
                    track_number -= 1
                    if track_number == 0:
                        exit(0)
                    track_filename = f'{track_number}.gpx'
                    ffile = f'https://angara.net/files/track/{year}/{month:02d}/{day:02d}/{track_filename}'
                    response = requests.get(ffile)