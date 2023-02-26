import random as rnd


def gen_ip_v4():
    ip = str(str(rnd.randint(172, 192)) + "." + str(rnd.randint(0, 255)) + "." + str(rnd.randint(0, 255)) + "." + str(
        rnd.randint(1, 255)))
    return ip


def gen_ip_v6():
    __m = 16 ** 4
    __ip = "fd39:fffd:" + ":".join(("%x" % rnd.randint(0, __m) for i in range(6)))
    return __ip

