import os

def get_ab(a: tuple, b: tuple, c: tuple, d: tuple):
    delta = (b[0]-a[0])*(c[1]-d[1]) - (b[1]-a[1])*(c[0]-d[0])
    delta_A = (c[0]-a[0])*(c[1]-d[1]) - (c[1]-a[1])*(c[0]-d[0])
    delta_B = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    return delta_A/delta, delta_B/delta



if __name__ == '__main__':
    a,b,c,d = (1,1), (5,1), (2,-2), (2,2)
    print(get_ab(a,b,c,d))

