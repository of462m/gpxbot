import ctypes
import os


class wpt(ctypes.Structure):
    _fields_ = [('lat', ctypes.c_double),
                ('lon', ctypes.c_double),
                ]


if __name__ == '__main__':
    test = ctypes.CDLL('/usr/lib/libgpxbaikal.so')
    test.fillmeup.restype = ctypes.c_voidp
    mystr = (ctypes.c_char * 256)()
    test.fillmeup(mystr)
    tokens = mystr.value.decode('utf-8').split()
    print(tokens)
    exit(0)

    #	test.deg2rad.restype = ctypes.c_void_p
    #	test.deg2rad.argtypes = [ctypes.POINTER(wpt)]

    test.geo2_distance_m.restype = ctypes.c_double
    #	test.geo2_distance_m.argtypes = [ctypes.POINTER(wpt)]

    w_pt = wpt(52.28832, 104.24759)

    test.deg2rad(ctypes.byref(w_pt))
    print(w_pt.lat, w_pt.lon)

    trk = (wpt * 2)()
    trk[0] = wpt(52.28832, 104.24759)
    trk[1] = wpt(52.29832, 104.25759)
    print(test.geo2_distance_m(ctypes.byref(trk)))

    print(os.getcwd())
