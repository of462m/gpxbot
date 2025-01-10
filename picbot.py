from exif import Image
from Levenshtein import distance as l_distance

def convert2DD(c):
    return round(c[0] + (c[1]/60) + (c[2]/3600), 6)

def decasum(k):
    def doublesum(ff):
        def inner(*args, **kwargs):
            return k * ff(*args, **kwargs)
        return inner
    return doublesum

@decasum(10)
def summa(a, b):
    return a + b



if __name__ == '__main__':
    print(l_distance('трехглавая', 'трехглавоя', weights=(1,5,3)))
    # print(l_distance('трехглавая', 'трехглавя', weights=(100,1,10)))
    D, N, NEA = list(), list(), list()
    A = ([2,3], [2,6], [7,6], [7,3], [5,3], [5,4], [3,4], [3,3])
    for i in range(0,len(A)):
        NEA.append(A[-i - 1])
        # print(i+1, i % (len(A)-1))
        i01, i02 = i, (i + 1) % len(A)
        print(i02, i01)
        D.append([A[i02][0]-A[i01][0], A[i02][1]-A[i01][1]])
        N.append([-A[i02][1]+A[i01][1], A[i02][0]-A[i01][0]])
    print(NEA)
    print(D)
    print(N)
    exit(0)

    print(summa(3, 4))
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
