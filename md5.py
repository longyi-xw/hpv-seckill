import ctypes


def unsigned_rs(n, bits):
    """
    模拟 Javascript 无符号右移
    :param n:
    :param bits:
    :return:
    """
    x, bits = ctypes.c_uint32(n).value, bits % 32
    return ctypes.c_uint32(x >> bits).value


def hexMd5(val: str):
    def r_16(r, n):
        t = (65535 & r) + (65535 & n)
        return (r >> 16) + (n >> 16) + (t >> 16) << 16 | 65535 & t

    def n_32(n, t, e, u, o, c):
        f = r_16(r_16(t, n), r_16(u, c))
        return r_16(f << o | unsigned_rs(f, 32 - o), e)

    def _t(r, t, e, u, o, c, f):
        return n_32(t & e | ~t & u, r, t, o, c, f)

    def _e(r, t, e, u, o, c, f):
        return n_32(t & u | e & ~u, r, t, o, c, f)

    def _u(r, t, e, u, o, c, f):
        return n_32(t ^ e ^ u, r, t, o, c, f)

    def _o(r, t, e, u, o, c, f):
        return n_32(e ^ (t | ~u), r, t, o, c, f)

    def _c(n):
        c = 1732584193
        f = -271733879
        a = -1732584194
        i = 271733878
        h = 0
        while h < len(n):
            l = c
            v = f
            g = a
            d = i
            c = _t(c, f, a, i, n[h], 7, -680876936)
            i = _t(i, c, f, a, n[h + 1], 12, -389564586)
            a = _t(a, i, c, f, n[h + 2], 17, 606105819)
            f = _t(f, a, i, c, n[h + 3], 22, -1044525330)
            c = _t(c, f, a, i, n[h + 4], 7, -176418897)
            i = _t(i, c, f, a, n[h + 5], 12, 1200080426)
            a = _t(a, i, c, f, n[h + 6], 17, -1473231341)
            f = _t(f, a, i, c, n[h + 7], 22, -45705983)
            c = _t(c, f, a, i, n[h + 8], 7, 1770035416)
            i = _t(i, c, f, a, n[h + 9], 12, -1958414417)
            a = _t(a, i, c, f, n[h + 10], 17, -42063)
            f = _t(f, a, i, c, n[h + 11], 22, -1990404162)
            c = _t(c, f, a, i, n[h + 12], 7, 1804603682)
            i = _t(i, c, f, a, n[h + 13], 12, -40341101)
            a = _t(a, i, c, f, n[h + 14], 17, -1502002290)
            f = _t(f, a, i, c, n[h + 15], 22, 1236535329)
            c = _e(c, f, a, i, n[h + 1], 5, -165796510)
            i = _e(i, c, f, a, n[h + 6], 9, -1069501632)
            a = _e(a, i, c, f, n[h + 11], 14, 643717713)
            f = _e(f, a, i, c, n[h], 20, -373897302)
            c = _e(c, f, a, i, n[h + 5], 5, -701558691)
            i = _e(i, c, f, a, n[h + 10], 9, 38016083)
            a = _e(a, i, c, f, n[h + 15], 14, -660478335)
            f = _e(f, a, i, c, n[h + 4], 20, -405537848)
            c = _e(c, f, a, i, n[h + 9], 5, 568446438)
            i = _e(i, c, f, a, n[h + 14], 9, -1019803690)
            a = _e(a, i, c, f, n[h + 3], 14, -187363961)
            f = _e(f, a, i, c, n[h + 8], 20, 1163531501)
            c = _e(c, f, a, i, n[h + 13], 5, -1444681467)
            i = _e(i, c, f, a, n[h + 2], 9, -51403784)
            a = _e(a, i, c, f, n[h + 7], 14, 1735328473)
            f = _e(f, a, i, c, n[h + 12], 20, -1926607734)
            c = _u(c, f, a, i, n[h + 5], 4, -378558)
            i = _u(i, c, f, a, n[h + 8], 11, -2022574463)
            a = _u(a, i, c, f, n[h + 11], 16, 1839030562)
            f = _u(f, a, i, c, n[h + 14], 23, -35309556)
            c = _u(c, f, a, i, n[h + 1], 4, -1530992060)
            i = _u(i, c, f, a, n[h + 4], 11, 1272893353)
            a = _u(a, i, c, f, n[h + 7], 16, -155497632)
            f = _u(f, a, i, c, n[h + 10], 23, -1094730640)
            c = _u(c, f, a, i, n[h + 13], 4, 681279174)
            i = _u(i, c, f, a, n[h], 11, -358537222)
            a = _u(a, i, c, f, n[h + 3], 16, -722521979)
            f = _u(f, a, i, c, n[h + 6], 23, 76029189)
            c = _u(c, f, a, i, n[h + 9], 4, -640364487)
            i = _u(i, c, f, a, n[h + 12], 11, -421815835)
            a = _u(a, i, c, f, n[h + 15], 16, 530742520)
            f = _u(f, a, i, c, n[h + 2], 23, -995338651)
            c = _o(c, f, a, i, n[h], 6, -198630844)
            i = _o(i, c, f, a, n[h + 7], 10, 1126891415)
            a = _o(a, i, c, f, n[h + 14], 15, -1416354905)
            f = _o(f, a, i, c, n[h + 5], 21, -57434055)
            c = _o(c, f, a, i, n[h + 12], 6, 1700485571)
            i = _o(i, c, f, a, n[h + 3], 10, -1894986606)
            a = _o(a, i, c, f, n[h + 10], 15, -1051523)
            f = _o(f, a, i, c, n[h + 1], 21, -2054922799)
            c = _o(c, f, a, i, n[h + 8], 6, 1873313359)
            i = _o(i, c, f, a, n[h + 15], 10, -30611744)
            a = _o(a, i, c, f, n[h + 6], 15, -1560198380)
            f = _o(f, a, i, c, n[h + 13], 21, 1309151649)
            c = _o(c, f, a, i, n[h + 4], 6, -145523070)
            i = _o(i, c, f, a, n[h + 11], 10, -1120210379)
            a = _o(a, i, c, f, n[h + 2], 15, 718787259)
            f = _o(f, a, i, c, n[h + 9], 21, -343485551)
            c = r_16(c, l)
            f = r_16(f, v)
            a = r_16(a, g)
            i = r_16(i, d)
            h += 16
        return [c, f, a, i]

    def f_offset(r):
        n = ""
        for t in range(4 * len(r)):
            n += "0123456789abcdef"[r[t >> 2] >> t % 4 * 8 + 4 & 15] + "0123456789abcdef"[r[t >> 2] >> t % 4 * 8 & 15]
        return n

    def a_offset(r):
        n = 1 + (len(r) + 8 >> 6)
        t = [0] * (16 * n)
        for e in range(16 * n): t[e] = 0
        e = 0
        while e < len(r):
            t[e >> 2] |= (255 & ord(r[e])) << e % 4 * 8
            e += 1

        t[e >> 2] |= 128 << e % 4 * 8
        t[16 * n - 2] = 8 * len(r)
        return t

    return f_offset(_c(a_offset(val)))

# ecc_hs = hexMd5(hexMd5("7991264490731686362432495") + "ux$ad70*b")
