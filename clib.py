import ctypes

clib = ctypes.CDLL('/usr/lib/libgpxbaikal.so')


def clib_get_ptokens(gpxdatafile: str, pdir: str) -> list:
    clib.get_ptokens.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    arg_pdir = pdir.encode('utf-8')
    arg_gpxdatafile = gpxdatafile.encode('utf-8')
    arg_ptokens = (ctypes.c_char * 256)()
    clib.get_ptokens(arg_pdir, arg_gpxdatafile, arg_ptokens)
    return arg_ptokens.value.decode('utf-8').split()


def clib_get_rtokens() -> list:
    pass
