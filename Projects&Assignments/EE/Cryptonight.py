#!/usr/bin/env python
__author__ = "Patrik Lundin"
__copyright__ = "Copyright 2018, nothisispatrik.com"
__license__ = "LGPL v3. Algorithms/constants may be (C) 2014-2018 The Monero project or (C) 2012-2014 The Cryptonote Developers. All code is original"
__email__ = "patrik@nothisispatrik.com"
__status__ = "Prototype"
__doc__ = """

   This is a Python implementation of the cryptonight slow hash. It includes a
   short main() with an example call. It is based on (and was checked against)
   the original Monero Project code (https://github.com/monero-project/monero)
   with and without the 2018 April hard fork variant. It's written for 
   Python 2.7, and probably won't work under 3, though it's not using anything
   particularly version specific.

   It's very slow, around 0.02 hashes per second (a little under two hashes
   per minute) on my gen 2 i5. As such, it's meant more as a consise summary
   of the algorithm than usefully runnable code. It's not particularly
   optimized, and where possible prior optimization has been removed. 

   There are no outside dependencies (except "time" which is only used 
   in the example) with everything reimplemented in pure python, including 
   AES, Keccak, Blake, Groestl, JH, and Skein. 
   """


# Single AES round, no round key (can be xor:ed in after)

# Here implemented using TBoxes, which is relativily fast, but
# vulnerable to cache-timing attacks. Not safe for other purposes.
def round(b):
    def col(c1, c2, c3, c4):
        t = S1[c1] ^ S2[c2] ^ S3[c3] ^ S4[c4]
        t1 = t >> 0 & 255
        t2 = t >> 8 & 255
        t3 = t >> 16 & 255
        t4 = t >> 24 & 255
        return (
            t1, t2, t3, t4)

    b = col(b[0], b[5], b[10], b[15]) + col(b[4], b[9], b[14], b[3]) + col(b[8], b[13], b[2], b[7]) + col(b[12], b[1],
                                                                                                          b[6], b[11])
    return b

    # AES key expansion.

    # Specific to CN:s ten rounds. Presumes that round keys follow
    # rc(n+1) = rc(n)<<1, which isn't true generally.


def kexp(k):
    xk = [
             0] * 160
    xk[:32] = k[:32]
    cs = 32
    rc = 1
    while cs < 160:
        t = xk[cs - 4:cs]
        if cs % 32 == 0:
            t = [
                SBox[t[1]] ^ rc, SBox[t[2]], SBox[t[3]], SBox[t[0]]]
            rc *= 2
        else:
            if cs % 32 == 16:
                t = [
                    SBox[t[0]], SBox[t[1]], SBox[t[2]], SBox[t[3]]]
        xk[cs:(cs + 4)] = [
            xk[cs - 32 + 0] ^ t[0],
            xk[cs - 32 + 1] ^ t[1],
            xk[cs - 32 + 2] ^ t[2],
            xk[cs - 32 + 3] ^ t[3]]
        cs += 4

    return xk

    # expand result from initial Keccac into a 2Mb scratchad by
    # repeatedly 10 round AES:ing a chunk of data.


def asplode(kec):
    xkey = kexp(kec[:32])
    st = kec[64:192]
    xk = [xkey[i:i + 16] for i in range(0, len(xkey), 16)]
    pad = []
    while len(pad) < 2097152:
        for j in range(0, len(st), 16):
            t = st[j:j + 16]
            for i in range(10):
                t = round(t)
                t = [a ^ b for a, b in zip(t, xk[i])]
            pad.extend(t)
        st = pad[-128:]
    return pad

    # combine final scratchpad into a single block again by xoring and
    # then 10 round AESing the blocks over each other one at a time


def implode(pad, kec):
    xkey = kexp(kec[32:64])
    xk = [xkey[i:i + 16] for i in range(0, len(xkey), 16)]
    st = kec[64:192]
    for p in range(0, len(pad), 128):
        for i in xrange(128):
            st[i] ^= pad[p + i]
        for i in xrange(0, 128, 16):
            for r in xrange(10):
                st[i:i + 16] = round(st[i:i + 16])
                for j in xrange(16):
                    st[i + j] ^= xk[r][j]

    kec[64:192] = st
    return kec

    # Do the memhard loop. Starting two blocks, read another from scratch pad
    # do an AES round on it, xor it by some things, write it back. Then use
    # a value from that to read another block, do two 64 bit mul:s and two
    # 64 bit adds, some more xors, and write that back. Start over and do it
    # again 1<<19 times.


def memhrd(pad, kec, variant=0, tw=[0] * 8):
    # convert a series of bytes into two 64 bit words and multiply them
    # return as 8 bytes
    def mul(a, b):
        t1 = a[0] << 0 | a[1] << 8 | a[2] << 16 | a[3] << 24 | a[4] << 32 | a[5] << 40 | a[6] << 48 | a[7] << 56
        t2 = b[0] << 0 | b[1] << 8 | b[2] << 16 | b[3] << 24 | b[4] << 32 | b[5] << 40 | b[6] << 48 | b[7] << 56
        r = t1 * t2
        r1 = r >> 64
        r2 = r & 0xffffffffffffffffL
        return [r1 & 255, (r1 >> 8) & 255, (r1 >> 16) & 255, (r1 >> 24) & 255, (r1 >> 32) & 255, (r1 >> 40) & 255,
                (r1 >> 48) & 255, (r1 >> 56) & 255, r2 & 0xff, (r2 >> 8) & 255, (r2 >> 16) & 255, (r2 >> 24) & 255,
                (r2 >> 32) & 255, (r2 >> 40) & 255, (r2 >> 48) & 255, (r2 >> 56) & 255]

        # Convert two blocks into four 64 bit numbers and pairwise add them,
        # no overflow. Swap order and convert back into bytes

    def sumhlf(a, b):
        ta1 = a[0] << 0 | a[1] << 8 | a[2] << 16 | a[3] << 24 | a[4] << 32 | a[5] << 40 | a[6] << 48 | a[7] << 56
        ta2 = a[8] << 0 | a[9] << 8 | a[10] << 16 | a[11] << 24 | a[12] << 32 | a[13] << 40 | a[14] << 48 | a[15] << 56
        tb1 = b[0] << 0 | b[1] << 8 | b[2] << 16 | b[3] << 24 | b[4] << 32 | b[5] << 40 | b[6] << 48 | b[7] << 56
        tb2 = b[8] << 0 | b[9] << 8 | b[10] << 16 | b[11] << 24 | b[12] << 32 | b[13] << 40 | b[14] << 48 | b[15] << 56
        r1, r2 = (ta1 + tb1 & 18446744073709551615L, ta2 + tb2 & 18446744073709551615L)
        return [r1 & 255, (r1 >> 8) & 255, (r1 >> 16) & 255, (r1 >> 24) & 255, (r1 >> 32) & 255, (r1 >> 40) & 255,
                (r1 >> 48) & 255, (r1 >> 56) & 255, r2 & 0xff, (r2 >> 8) & 255, (r2 >> 16) & 255, (r2 >> 24) & 255,
                (r2 >> 32) & 255, (r2 >> 40) & 255, (r2 >> 48) & 255, (r2 >> 56) & 255]

        # xor two blocks

    def blxor(a, b):
        return [t1 ^ t2 for t1, t2 in zip(a, b)]

        # pull 17 bits from a block for use as an address in the scratchpad.
        # Zeroes out the 4 LSB rather than dividing, making it useful as an
        # index in the pad directly. >>4 instead of &.. would give a block
        # index, which could then later be <<4 to give an actual location.

    def toaddr(a):
        return (a[2] << 16 | a[1] << 8 | a[0]) & 2097136

        # make the first two indexes

    A = blxor(kec[0:16], kec[32:48])
    B = blxor(kec[16:32], kec[48:64])

    for i in xrange(1 << 19):
        t = toaddr(A)
        C = pad[t:t + 16]
        C = round(C)
        C = blxor(C, A)
        pad[t:(t + 16)] = blxor(B, C)

        # After the Apr 2018 hardfork, this will be/was
        # added to the loop. This is equivalent to VARIANT1_1
        # in the original C.
        if variant:
            a = pad[t + 11]
            a = (~a & 1) << 4 | ((~a & 1) << 4 & a) << 1 | (a & 32) >> 1
            pad[t + 11] ^= a

        B = C
        t = toaddr(C)
        C = pad[t:t + 16]

        P = mul(B, C)
        A = sumhlf(A, P)
        pad[t:(t + 16)] = A
        # this is the second variant add in, equivalent of VARIENT1_2 in
        # C.
        if variant:
            for i in range(8):
                pad[t + i + 8] ^= tw[i]
        A = blxor(A, C)

    return pad

    # Calculate 1600 bit keccak hash from a 200b input.
    # This isn't equivalent to the final SHA3 version.
    # I don't remember how exactly, but don't expect it to be.


def keccak(inp):
    def rol(b, n):
        return ((b << n) & 0xffffffffffffffff) | (b >> (64 - n))

    s = [sum(a[i] << (i << 3) for i in range(8)) for a in [inp[i:i + 8] for i in xrange(0, 200, 8)]]

    xo = [0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
          0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
          0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
          0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
          0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
          0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
          0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
          0x8000000000008080, 0x0000000080000001, 0x8000000080008008]

    ro = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 2, 14,
          27, 41, 56, 8, 25, 43, 62, 18, 39, 61, 20, 44]

    pn = [10, 7, 11, 17, 18, 3, 5, 16, 8, 21, 24, 4,
          15, 23, 19, 13, 12, 2, 20, 14, 22, 9, 6, 1]

    for r in xrange(24):
        b0 = s[0] ^ s[5] ^ s[10] ^ s[15] ^ s[20]
        b1 = s[1] ^ s[6] ^ s[11] ^ s[16] ^ s[21]
        b2 = s[2] ^ s[7] ^ s[12] ^ s[17] ^ s[22]
        b3 = s[3] ^ s[8] ^ s[13] ^ s[18] ^ s[23]
        b4 = s[4] ^ s[9] ^ s[14] ^ s[19] ^ s[24]

        t = b4 ^ rol(b1, 1)
        s[0] ^= t;
        s[5] ^= t;
        s[10] ^= t;
        s[15] ^= t;
        s[20] ^= t
        t = b0 ^ rol(b2, 1)
        s[1] ^= t;
        s[6] ^= t;
        s[11] ^= t;
        s[16] ^= t;
        s[21] ^= t
        t = b1 ^ rol(b3, 1)
        s[2] ^= t;
        s[7] ^= t;
        s[12] ^= t;
        s[17] ^= t;
        s[22] ^= t
        t = b2 ^ rol(b4, 1)
        s[3] ^= t;
        s[8] ^= t;
        s[13] ^= t;
        s[18] ^= t;
        s[23] ^= t
        t = b3 ^ rol(b0, 1)
        s[4] ^= t;
        s[9] ^= t;
        s[14] ^= t;
        s[19] ^= t;
        s[24] ^= t

        t = s[1]
        for i in xrange(24):
            j = pn[i]
            t2 = s[j]
            s[j] = rol(t, ro[i])
            t = t2

        for j in xrange(0, 24, 5):
            b0 = s[j];
            b1 = s[j + 1];
            b2 = s[j + 2];
            b3 = s[j + 3];
            b4 = s[j + 4];
            s[j] ^= (b1 ^ 0xffffffffffffffff) & b2;
            s[j + 1] ^= (b2 ^ 0xffffffffffffffff) & b3;
            s[j + 2] ^= (b3 ^ 0xffffffffffffffff) & b4;
            s[j + 3] ^= (b4 ^ 0xffffffffffffffff) & b0;
            s[j + 4] ^= (b0 ^ 0xffffffffffffffff) & b1;

        s[0] ^= xo[r]

    b = reduce(lambda a, b: a + b, [[((a >> (c << 3)) & 255) for c in range(8)] for a in s])
    return b

    # Blake hash. Assumes 200b input, produces 32b output


def blake(data):
    K = [0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344, 0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89, 0x452821E6,
         0x38D01377, 0xBE5466CF, 0x34E90C6C, 0xC0AC29B7, 0xC97C50DD, 0x3F84D5B5, 0xB5470917]
    h = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
    S = blakeS  # Constant from bottom of file
    data = data + [0x80] + [0x00] * 46 + [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x40]
    for (o, t) in [(0, 512), (64, 1024), (128, 1536), (192, 1600)]:
        m = [((data[o + i + 0] << 24)) |
             ((data[o + i + 1] << 16)) |
             ((data[o + i + 2] << 8)) |
             ((data[o + i + 3] << 0)) for i in range(0, 64, 4)]
        v = [0] * 16
        v[0: 8] = [h[i] for i in range(8)]
        v[8:16] = [K[i] for i in range(8)]
        v[8:12] = [v[8 + i] for i in range(4)]
        v[12] = v[12] ^ t
        v[13] = v[13] ^ t

        ror = lambda x, n: (x >> n) | ((x << (32 - n)) & 0xFFFFFFFF)
        for round in range(14):
            i = 0
            for (a, b, c, d) in [
                (0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14),
                (3, 7, 11, 15), (0, 5, 10, 15), (1, 6, 11, 12),
                (2, 7, 8, 13), (3, 4, 9, 14)]:
                p, q = S[round][i], S[round][i + 1]
                i += 2

                v[a] = ((v[a] + v[b]) + (m[p] ^ K[q])) & 0xFFFFFFFF
                v[d] = ror(v[d] ^ v[a], 16)
                v[c] = (v[c] + v[d]) & 0xFFFFFFFF
                v[b] = ror(v[b] ^ v[c], 12)

                v[a] = ((v[a] + v[b]) + (m[q] ^ K[p])) & 0xFFFFFFFF
                v[d] = ror(v[d] ^ v[a], 8)
                v[c] = (v[c] + v[d]) & 0xFFFFFFFF
                v[b] = ror(v[b] ^ v[c], 7)

        h = [h[i] ^ v[i] ^ v[i + 8] for i in range(8)]
    rv = reduce(lambda a, b: a + b,
                [[(h[i] >> 24) & 255, (h[i] >> 16) & 255, (h[i] >> 8) & 255, (h[i] >> 0) & 255] for i in range(8)])
    return rv

    # Groestl hash. Assumes 200b input, produces 32b output


def groestl(inp):
    def col(x, y, i, c0, c1, c2, c3, c4, c5, c6, c7):
        T = groestlT  # Constant from bottom of file
        y[i] = T[0 * 256 + ((x[c0] >> 0) & 255)] ^ T[1 * 256 + ((x[c1] >> 8) & 255)] ^ T[
            2 * 256 + ((x[c2] >> 16) & 255)] ^ T[3 * 256 + ((x[c3] >> 24) & 255)] ^ T[4 * 256 + ((x[c4] >> 0) & 255)] ^ \
               T[5 * 256 + ((x[c5] >> 8) & 255)] ^ T[6 * 256 + ((x[c6] >> 16) & 255)] ^ T[
                   7 * 256 + ((x[c7] >> 24) & 255)]

    def P(x, y, r):
        x[0] ^= 0x00000000 ^ r
        x[2] ^= 0x00000010 ^ r
        x[4] ^= 0x00000020 ^ r
        x[6] ^= 0x00000030 ^ r
        x[8] ^= 0x00000040 ^ r
        x[10] ^= 0x00000050 ^ r
        x[12] ^= 0x00000060 ^ r
        x[14] ^= 0x00000070 ^ r
        col(x, y, 0, 0, 2, 4, 6, 9, 11, 13, 15)
        col(x, y, 1, 9, 11, 13, 15, 0, 2, 4, 6)
        col(x, y, 2, 2, 4, 6, 8, 11, 13, 15, 1)
        col(x, y, 3, 11, 13, 15, 1, 2, 4, 6, 8)
        col(x, y, 4, 4, 6, 8, 10, 13, 15, 1, 3)
        col(x, y, 5, 13, 15, 1, 3, 4, 6, 8, 10)
        col(x, y, 6, 6, 8, 10, 12, 15, 1, 3, 5)
        col(x, y, 7, 15, 1, 3, 5, 6, 8, 10, 12)
        col(x, y, 8, 8, 10, 12, 14, 1, 3, 5, 7)
        col(x, y, 9, 1, 3, 5, 7, 8, 10, 12, 14)
        col(x, y, 10, 10, 12, 14, 0, 3, 5, 7, 9)
        col(x, y, 11, 3, 5, 7, 9, 10, 12, 14, 0)
        col(x, y, 12, 12, 14, 0, 2, 5, 7, 9, 11)
        col(x, y, 13, 5, 7, 9, 11, 12, 14, 0, 2)
        col(x, y, 14, 14, 0, 2, 4, 7, 9, 11, 13)
        col(x, y, 15, 7, 9, 11, 13, 14, 0, 2, 4)

    def Q(x, y, r):
        x[0] = x[0] ^ 0xffffffff
        x[1] ^= 0xffffffff ^ r
        x[2] = x[2] ^ 0xffffffff
        x[3] ^= 0xefffffff ^ r
        x[4] = x[4] ^ 0xffffffff
        x[5] ^= 0xdfffffff ^ r
        x[6] = x[6] ^ 0xffffffff
        x[7] ^= 0xcfffffff ^ r
        x[8] = x[8] ^ 0xffffffff
        x[9] ^= 0xbfffffff ^ r
        x[10] = x[10] ^ 0xffffffff
        x[11] ^= 0xafffffff ^ r
        x[12] = x[12] ^ 0xffffffff
        x[13] ^= 0x9fffffff ^ r
        x[14] = x[14] ^ 0xffffffff
        x[15] ^= 0x8fffffff ^ r
        col(x, y, 0, 2, 6, 10, 14, 1, 5, 9, 13)
        col(x, y, 1, 1, 5, 9, 13, 2, 6, 10, 14)
        col(x, y, 2, 4, 8, 12, 0, 3, 7, 11, 15)
        col(x, y, 3, 3, 7, 11, 15, 4, 8, 12, 0)
        col(x, y, 4, 6, 10, 14, 2, 5, 9, 13, 1)
        col(x, y, 5, 5, 9, 13, 1, 6, 10, 14, 2)
        col(x, y, 6, 8, 12, 0, 4, 7, 11, 15, 3)
        col(x, y, 7, 7, 11, 15, 3, 8, 12, 0, 4)
        col(x, y, 8, 10, 14, 2, 6, 9, 13, 1, 5)
        col(x, y, 9, 9, 13, 1, 5, 10, 14, 2, 6)
        col(x, y, 10, 12, 0, 4, 8, 11, 15, 3, 7)
        col(x, y, 11, 11, 15, 3, 7, 12, 0, 4, 8)
        col(x, y, 12, 14, 2, 6, 10, 13, 1, 5, 9)
        col(x, y, 13, 13, 1, 5, 9, 14, 2, 6, 10)
        col(x, y, 14, 0, 4, 8, 12, 15, 3, 7, 11)
        col(x, y, 15, 15, 3, 7, 11, 0, 4, 8, 12)

    def F(h, m):
        Ptmp = [0L] * 16;
        Qtmp = [0L] * 16;
        y = [0L] * 16;
        z = [0L] * 16;

        for i in range(16):
            z[i] = m[i]
            Ptmp[i] = h[i] ^ m[i]

        Q(z, y, 0x00000000)
        Q(y, z, 0x01000000)
        Q(z, y, 0x02000000)
        Q(y, z, 0x03000000)
        Q(z, y, 0x04000000)
        Q(y, z, 0x05000000)
        Q(z, y, 0x06000000)
        Q(y, z, 0x07000000)
        Q(z, y, 0x08000000)
        Q(y, Qtmp, 0x09000000)

        P(Ptmp, y, 0x00000000)
        P(y, z, 0x00000001)
        P(z, y, 0x00000002)
        P(y, z, 0x00000003)
        P(z, y, 0x00000004)
        P(y, z, 0x00000005)
        P(z, y, 0x00000006)
        P(y, z, 0x00000007)
        P(z, y, 0x00000008)
        P(y, Ptmp, 0x00000009)

        for i in range(16):
            h[i] ^= Ptmp[i] ^ Qtmp[i]

    buf = [0L] * 16
    tmp = [0L] * 16
    y = [0L] * 16
    z = [0L] * 16
    d = [0L] * 16

    d[15] = 0x00010000L
    data = [
               (inp[i + 3] << 24) | (inp[i + 2] << 16) | (inp[i + 1] << 8) | (inp[i + 0] << 0)
               for i in range(0, len(inp), 4)] + [0x80] + [0L] * 12 + [4 << 24]

    F(d, data[0:16])
    F(d, data[16:32])
    F(d, data[32:48])
    F(d, data[48:64])

    tmp = d[:16]
    P(tmp, y, 0x00000000L)
    P(y, z, 0x00000001L)
    P(z, y, 0x00000002L)
    P(y, z, 0x00000003L)
    P(z, y, 0x00000004L)
    P(y, z, 0x00000005L)
    P(z, y, 0x00000006L)
    P(y, z, 0x00000007L)
    P(z, y, 0x00000008L)
    P(y, tmp, 0x00000009L)

    rv = [d[j] ^ tmp[j] for j in range(8, 16)]
    rv = reduce(lambda a, b: a + b, [[a & 255, (a >> 8) & 255, (a >> 16) & 255, (a >> 24) & 255] for a in rv])
    return rv

    # JH hash, Assumes 200b input, produces 32b output


def jh(data):
    hashval = [32]
    A = [0] * 256
    rc = [0] * 64
    rcx = [0] * 256
    tmp = [0] * 256
    S = [[9, 0, 4, 11, 13, 12, 3, 15, 1, 10, 2, 6, 7, 5, 8, 14], [3, 12, 6, 13, 5, 7, 1, 9, 15, 2, 0, 4, 11, 10, 14, 8]]
    rc0 = [0x6, 0xa, 0x0, 0x9, 0xe, 0x6, 0x6, 0x7, 0xf, 0x3, 0xb, 0xc, 0xc, 0x9, 0x0, 0x8, 0xb, 0x2, 0xf, 0xb, 0x1, 0x3,
           0x6, 0x6, 0xe, 0xa, 0x9, 0x5, 0x7, 0xd, 0x3, 0xe, 0x3, 0xa, 0xd, 0xe, 0xc, 0x1, 0x7, 0x5, 0x1, 0x2, 0x7, 0x7,
           0x5, 0x0, 0x9, 0x9, 0xd, 0xa, 0x2, 0xf, 0x5, 0x9, 0x0, 0xb, 0x0, 0x6, 0x6, 0x7, 0x3, 0x2, 0x2, 0xa]
    d = [254, 0, 64, 128, 255, 254]

    H = [1] + [0] * 127

    for b in d:
        if b <= 128:
            for i in range(64):
                H[i] ^= data[b + i]
        elif b == 255:
            H[:8] = [H[i] ^ data[192 + i] for i in range(8)]
            H[8] ^= 128
        rc = rc0[:]

        for i in range(256):
            t0 = (H[i >> 3] >> (7 - (i & 7))) & 1
            t1 = (H[(i + 256) >> 3] >> (7 - (i & 7))) & 1
            t2 = (H[(i + 512) >> 3] >> (7 - (i & 7))) & 1
            t3 = (H[(i + 768) >> 3] >> (7 - (i & 7))) & 1
            tmp[i] = (t0 << 3) | (t1 << 2) | (t2 << 1) | (t3 << 0)
        for i in range(128):
            A[i << 1] = tmp[i]
            A[(i << 1) + 1] = tmp[i + 128]

        for r in range(42):
            for i in range(256):
                rcx[i] = (rc[i >> 2] >> (3 - (i & 3))) & 1
            for i in range(256):
                tmp[i] = S[rcx[i]][A[i]]
            for i in range(0, 256, 2):
                t0 = tmp[i + 1] ^ (((tmp[i] << 1) ^ (tmp[i] >> 3) ^ ((tmp[i] >> 2) & 2)) & 0xf)
                t1 = tmp[i + 0] ^ (((t0 << 1) ^ (t0 >> 3) ^ ((t0 >> 2) & 2)) & 0xf)
                t2 = (i >> 1) & 1
                tmp[i + t2 ^ 1] = t0
                tmp[i + t2] = t1
            for i in range(128):
                A[i] = tmp[i << 1]
                A[(i + 128) ^ 1] = tmp[(i << 1) + 1]
            for i in range(64):
                tmp[i] = S[0][rc[i]]
            for i in range(0, 64, 2):
                tmp[i + 1] ^= ((tmp[i] << 1) ^ (tmp[i] >> 3) ^ ((tmp[i] >> 2) & 2)) & 0xf
                tmp[i] ^= ((tmp[i + 1] << 1) ^ (tmp[i + 1] >> 3) ^ ((tmp[i + 1] >> 2) & 2)) & 0xf
            for i in range(0, 64, 4):
                t = tmp[i + 2]
                tmp[i + 2] = tmp[i + 3]
                tmp[i + 3] = t
            for i in range(32):
                rc[i] = tmp[i << 1]
                rc[(i + 32) ^ 1] = tmp[(i << 1) + 1]

        for i in range(128):
            tmp[i] = A[i << 1]
            tmp[i + 128] = A[(i << 1) + 1]
        for i in range(128):
            H[i] = 0
        for i in range(256):
            t0 = (tmp[i] >> 3) & 1
            t1 = (tmp[i] >> 2) & 1
            t2 = (tmp[i] >> 1) & 1
            t3 = (tmp[i] >> 0) & 1
            H[i >> 3] |= t0 << (7 - (i & 7))
            H[(i + 256) >> 3] |= t1 << (7 - (i & 7))
            H[(i + 512) >> 3] |= t2 << (7 - (i & 7))
            H[(i + 768) >> 3] |= t3 << (7 - (i & 7))

        if b <= 128:
            for i in range(64):
                H[i + 64] ^= data[b + i]
        elif (b == 255):
            for i in range(8):
                H[64 + i] ^= data[192 + i]
            H[8 + 64] ^= 128
            H[63] ^= 64
            H[62] ^= 6
    H[127] ^= 64
    H[126] ^= 6
    return H[96:]

    # Skein hash. Assumes 200b input, produces 32b output


def skein(data):
    def M(x):  # Mask down to 64 bin
        return x & 0xffffffffffffffffL

    def R64(x, p, n):  # Rotate left, 64 bit
        x[p] = M((x[p] << n) | (x[p] >> (64 - n)))

    def Add(x, a, b):  # 64 bit add, no overflow
        x[a] = M(x[a] + x[b])

    def R512(X, p0, p1, p2, p3, p4, p5, p6, p7, q):
        Rk = [[46, 36, 19, 37], [33, 27, 14, 42], [17, 49, 36, 39], [44, 9, 54, 56], [39, 30, 34, 24], [13, 50, 10, 17],
              [25, 29, 39, 43], [8, 35, 56, 22]]

        Add(X, p0, p1)
        R64(X, p1, Rk[q][0])
        X[p1] ^= X[p0]

        Add(X, p2, p3)
        R64(X, p3, Rk[q][1])
        X[p3] ^= X[p2]

        Add(X, p4, p5)
        R64(X, p5, Rk[q][2])
        X[p5] ^= X[p4]

        Add(X, p6, p7)
        R64(X, p7, Rk[q][3])
        X[p7] ^= X[p6]

        # Skein types and lengths. Since it's just five blocks, always
        # same length and such, they're constant. Here as TYPE | LEN,
        # as it is stored in Skeins T(2)

    LC = [0x7000000000000040L, 0x3000000000000080L, 0x30000000000000c0L,
          0xb0000000000000c8L, 0xff00000000000008L]
    # Init vector. Specific to 512-256 hash
    L = [0, 0, 0, 0xCCD044A12FDB3E13L, 0xE83590301A79A9EBL,
         0x55AEA0614F816E6FL, 0x2A2767A4AE9B94DBL, 0xEC06025E74DD7683L,
         0xE7A436CDC4746251L, 0xC36FBAF9393AD185L, 0x3EEDBA1833EDFC13L, 0]
    # Keeper of data. Extra length so that after the 200b we send,
    # there's enough zeros for another full block, and, for the
    # OUT+FINAL block, one with all zeros.
    b = [0] * 35
    # Offset to current data. Hops around
    w = 0
    # Temp state data
    X = [0] * 8;
    # fill b up with 8b words
    for i in range(25):
        b[i] = (
                (data[(i * 8) + 0] << 0) |
                (data[(i * 8) + 1] << 8) |
                (data[(i * 8) + 2] << 16) |
                (data[(i * 8) + 3] << 24) |
                (data[(i * 8) + 4] << 32) |
                (data[(i * 8) + 5] << 40) |
                (data[(i * 8) + 6] << 48) |
                (data[(i * 8) + 7] << 56))
        # Each block..
    for i in range(5):
        # T2 = T1^T0, like we stored
        L[2] = LC[i]
        # T0 = length. Extract with &0xff
        L[0] = L[2] & 255;
        # T2 = type+flags. Exract by removing T0
        L[1] = L[2] ^ L[0];
        # Parity + magic constant.
        L[11] = L[3] ^ L[4] ^ L[5] ^ L[6] ^ L[7] ^ L[8] ^ L[9] ^ L[10] ^ 0x1BD11BDAA9FC1A22L;
        # Next chunk
        w = ((i & 3) << 3) + 25 * (i >> 2);
        # Init X
        for R in range(8):
            X[R] = M(b[w + R] + L[R + 3])
        X[5] = M(X[5] + L[0])
        X[6] = M(X[6] + L[1])

        # Rounds
        for R in range(0, 18, 2):
            R512(X, 0, 1, 2, 3, 4, 5, 6, 7, 0)
            R512(X, 2, 1, 4, 7, 6, 5, 0, 3, 1)
            R512(X, 4, 1, 6, 3, 0, 5, 2, 7, 2)
            R512(X, 6, 1, 0, 7, 2, 5, 4, 3, 3)
            for j in range(8):
                X[j] = M(X[j] + L[3 + ((R + j + 1) % 9)])
            X[5] = M(X[5] + L[(R + 1) % 3])
            X[6] = M(X[6] + L[(R + 2) % 3])
            X[7] = M(X[7] + R + 1)
            R512(X, 0, 1, 2, 3, 4, 5, 6, 7, 4)
            R512(X, 2, 1, 4, 7, 6, 5, 0, 3, 5)
            R512(X, 4, 1, 6, 3, 0, 5, 2, 7, 6)
            R512(X, 6, 1, 0, 7, 2, 5, 4, 3, 7)
            for j in range(8):
                X[j] = M(X[j] + L[3 + ((R + j + 2) % 9)])
            X[5] = M(X[5] + L[(R + 2) % 3])
            X[6] = M(X[6] + L[(R + 3) % 3])
            X[7] = M(X[7] + R + 2)

            # Back into state w/ round results
        for R in range(8):
            L[3 + R] = X[R] ^ b[w + R]

            # Done, convert to bytes and shove into h
    h = []
    for i in range(4):
        h.extend([
            (L[i + 3] >> 0) & 255,
            (L[i + 3] >> 8) & 255,
            (L[i + 3] >> 16) & 255,
            (L[i + 3] >> 24) & 255,
            (L[i + 3] >> 32) & 255,
            (L[i + 3] >> 40) & 255,
            (L[i + 3] >> 48) & 255,
            (L[i + 3] >> 56) & 255])

    return h

    # All of the preceeding hash functions are de-generalized to presume
    # input length and to only produce specific output length. The will not
    # function correctly under other circumstances.

    # The main cryptonight hash function. Takes 76 bytes input (without
    # verifying that) and outputs the final 32 byte hash. Both input
    # and output are arrays of 8 bit integers. If "quiet" is set False,
    # it'll print what it's doing through off and on the steps. If
    # "variant" is set to 1, it'll work as it's supposed to after the
    # Apr 2018 hard fork, otherwise as it's supposed to before.


def cn_slow_hash(inp, quiet=0, variant=0):
    tw = [0] * 8
    if (not quiet):
        print
        "Keccac.."
        # Padding
    inp = inp + [0x01] + [0x00] * 58 + [0x80] + [0x00] * 64
    kec = keccak(inp)

    # Equivalent to VARIANT*INIT* in C. Stores the last 8 bytes after
    # keccak xor the current Nonce, which will later be xored in thoughout
    # the memhard loop (in the equivalent of VARIANT1_2).
    if variant:
        tw = [a ^ b for (a, b) in zip(kec[192:], inp[35:35 + 8])]

    if (not quiet):
        print
        "Expanding scratchpad.."
    pad = asplode(kec)
    if (not quiet):
        print
        "Memhard.."
    memhrd(pad, kec, variant, tw)
    if (not quiet):
        print
        "Imploding.."
    imp = implode(pad, kec)
    if (not quiet):
        print
        "Keccac again.."
    kec = keccak(imp)

    h = kec[0] & 3
    if h == 0:
        if (not quiet):
            print
            "Blake.."
        r = blake(kec)
    elif h == 1:
        if (not quiet):
            print
            "Groestl.."
        r = groestl(kec)
    elif h == 2:
        if (not quiet):
            print
            "Jh.."
        r = jh(kec)
    else:
        if (not quiet):
            print
            "Skein.."
        r = skein(kec)

    return r


import time  # only used in main


# Main. This runs a single case and checks it against one of two
# precalculated results depending on "variant". This isn't particularly
# sufficient for testing it, but it's at least a single runnable example

def main():
    inp = [
        0x05, 0x05, 0x84, 0xe2, 0xfa, 0xcc, 0x05, 0xfe,
        0x5c, 0x31, 0x96, 0xe9, 0x95, 0xae, 0x88, 0x31,
        0x0b, 0xa8, 0x6e, 0xae, 0x4a, 0xb6, 0x25, 0xab,
        0xd2, 0x6e, 0x19, 0x2f, 0x26, 0xf3, 0x2c, 0x7d,

        0xcb, 0x6d, 0xb1, 0xd1, 0x08, 0xd7, 0x68, 0x5d,
        0x00, 0x08, 0x57, 0xd6, 0x62, 0xea, 0x60, 0x02,
        0xe5, 0x19, 0xa2, 0x76, 0xb9, 0xd6, 0x9a, 0xb9,
        0xf0, 0xdf, 0x14, 0xc9, 0xf5, 0x86, 0xe1, 0x1a,

        0xe4, 0x57, 0xb1, 0xb5, 0x74, 0x05, 0xaf, 0xbf,
        0x9c, 0xc0, 0xcb, 0x06]

    st = time.time()
    variant = 1  # change to run other version

    r = cn_slow_hash(inp, False, variant)

    et = time.time()

    print
    ' '.join("%.2x" % (a) for a in r)
    print
    "Total %ds (%f H/s)" % (et - st, 1. / (et - st))
    correct_result_old = [0x2a, 0x26, 0x47, 0x75, 0x7c, 0xf6, 0x20, 0xa9, 0x9a, 0xf4, 0xf8, 0x3f, 0xe5, 0x9f, 0x98,
                          0x5d, 0x3e, 0x3b, 0x8d, 0x63, 0xa7, 0x5e, 0x01, 0x20, 0x75, 0x6f, 0x8b, 0xff, 0xa4, 0x8e,
                          0x00, 0x00]
    correct_result_new = [0xfc, 0x24, 0x23, 0x8f, 0x96, 0x0c, 0x14, 0x72, 0x73, 0x86, 0x29, 0x5b, 0xd0, 0xfc, 0xec,
                          0xba, 0xce, 0x8f, 0x2a, 0xef, 0x74, 0xad, 0x71, 0x08, 0x77, 0x1c, 0x7c, 0x83, 0x2b, 0x0a,
                          0x9f, 0x00]

    if variant:
        print
        "Pass" if correct_result_new == r else "Fail"
    else:
        print
        "Pass" if correct_result_old == r else "Fail"


# Constants ahoy!

# Tboxes, Sbox (generated from TBox), Blake and Groestl constant lists
# Other constants are sprinkled thought their respective functions, these
# are here to somewhat improve readabillity.

# There's nothing below them besides the if __name__.. to call main
S1 = [0xa56363c6, 0x847c7cf8, 0x997777ee, 0x8d7b7bf6, 0x0df2f2ff, 0xbd6b6bd6, 0xb16f6fde, 0x54c5c591, 0x50303060,
      0x03010102, 0xa96767ce, 0x7d2b2b56, 0x19fefee7, 0x62d7d7b5, 0xe6abab4d, 0x9a7676ec, 0x45caca8f, 0x9d82821f,
      0x40c9c989, 0x877d7dfa, 0x15fafaef, 0xeb5959b2, 0xc947478e, 0x0bf0f0fb, 0xecadad41, 0x67d4d4b3, 0xfda2a25f,
      0xeaafaf45, 0xbf9c9c23, 0xf7a4a453, 0x967272e4, 0x5bc0c09b, 0xc2b7b775, 0x1cfdfde1, 0xae93933d, 0x6a26264c,
      0x5a36366c, 0x413f3f7e, 0x02f7f7f5, 0x4fcccc83, 0x5c343468, 0xf4a5a551, 0x34e5e5d1, 0x08f1f1f9, 0x937171e2,
      0x73d8d8ab, 0x53313162, 0x3f15152a, 0x0c040408, 0x52c7c795, 0x65232346, 0x5ec3c39d, 0x28181830, 0xa1969637,
      0x0f05050a, 0xb59a9a2f, 0x0907070e, 0x36121224, 0x9b80801b, 0x3de2e2df, 0x26ebebcd, 0x6927274e, 0xcdb2b27f,
      0x9f7575ea, 0x1b090912, 0x9e83831d, 0x742c2c58, 0x2e1a1a34, 0x2d1b1b36, 0xb26e6edc, 0xee5a5ab4, 0xfba0a05b,
      0xf65252a4, 0x4d3b3b76, 0x61d6d6b7, 0xceb3b37d, 0x7b292952, 0x3ee3e3dd, 0x712f2f5e, 0x97848413, 0xf55353a6,
      0x68d1d1b9, 0x00000000, 0x2cededc1, 0x60202040, 0x1ffcfce3, 0xc8b1b179, 0xed5b5bb6, 0xbe6a6ad4, 0x46cbcb8d,
      0xd9bebe67, 0x4b393972, 0xde4a4a94, 0xd44c4c98, 0xe85858b0, 0x4acfcf85, 0x6bd0d0bb, 0x2aefefc5, 0xe5aaaa4f,
      0x16fbfbed, 0xc5434386, 0xd74d4d9a, 0x55333366, 0x94858511, 0xcf45458a, 0x10f9f9e9, 0x06020204, 0x817f7ffe,
      0xf05050a0, 0x443c3c78, 0xba9f9f25, 0xe3a8a84b, 0xf35151a2, 0xfea3a35d, 0xc0404080, 0x8a8f8f05, 0xad92923f,
      0xbc9d9d21, 0x48383870, 0x04f5f5f1, 0xdfbcbc63, 0xc1b6b677, 0x75dadaaf, 0x63212142, 0x30101020, 0x1affffe5,
      0x0ef3f3fd, 0x6dd2d2bf, 0x4ccdcd81, 0x140c0c18, 0x35131326, 0x2fececc3, 0xe15f5fbe, 0xa2979735, 0xcc444488,
      0x3917172e, 0x57c4c493, 0xf2a7a755, 0x827e7efc, 0x473d3d7a, 0xac6464c8, 0xe75d5dba, 0x2b191932, 0x957373e6,
      0xa06060c0, 0x98818119, 0xd14f4f9e, 0x7fdcdca3, 0x66222244, 0x7e2a2a54, 0xab90903b, 0x8388880b, 0xca46468c,
      0x29eeeec7, 0xd3b8b86b, 0x3c141428, 0x79dedea7, 0xe25e5ebc, 0x1d0b0b16, 0x76dbdbad, 0x3be0e0db, 0x56323264,
      0x4e3a3a74, 0x1e0a0a14, 0xdb494992, 0x0a06060c, 0x6c242448, 0xe45c5cb8, 0x5dc2c29f, 0x6ed3d3bd, 0xefacac43,
      0xa66262c4, 0xa8919139, 0xa4959531, 0x37e4e4d3, 0x8b7979f2, 0x32e7e7d5, 0x43c8c88b, 0x5937376e, 0xb76d6dda,
      0x8c8d8d01, 0x64d5d5b1, 0xd24e4e9c, 0xe0a9a949, 0xb46c6cd8, 0xfa5656ac, 0x07f4f4f3, 0x25eaeacf, 0xaf6565ca,
      0x8e7a7af4, 0xe9aeae47, 0x18080810, 0xd5baba6f, 0x887878f0, 0x6f25254a, 0x722e2e5c, 0x241c1c38, 0xf1a6a657,
      0xc7b4b473, 0x51c6c697, 0x23e8e8cb, 0x7cdddda1, 0x9c7474e8, 0x211f1f3e, 0xdd4b4b96, 0xdcbdbd61, 0x868b8b0d,
      0x858a8a0f, 0x907070e0, 0x423e3e7c, 0xc4b5b571, 0xaa6666cc, 0xd8484890, 0x05030306, 0x01f6f6f7, 0x120e0e1c,
      0xa36161c2, 0x5f35356a, 0xf95757ae, 0xd0b9b969, 0x91868617, 0x58c1c199, 0x271d1d3a, 0xb99e9e27, 0x38e1e1d9,
      0x13f8f8eb, 0xb398982b, 0x33111122, 0xbb6969d2, 0x70d9d9a9, 0x898e8e07, 0xa7949433, 0xb69b9b2d, 0x221e1e3c,
      0x92878715, 0x20e9e9c9, 0x49cece87, 0xff5555aa, 0x78282850, 0x7adfdfa5, 0x8f8c8c03, 0xf8a1a159, 0x80898909,
      0x170d0d1a, 0xdabfbf65, 0x31e6e6d7, 0xc6424284, 0xb86868d0, 0xc3414182, 0xb0999929, 0x772d2d5a, 0x110f0f1e,
      0xcbb0b07b, 0xfc5454a8, 0xd6bbbb6d, 0x3a16162c]
S2 = [0x6363c6a5, 0x7c7cf884, 0x7777ee99, 0x7b7bf68d, 0xf2f2ff0d, 0x6b6bd6bd, 0x6f6fdeb1, 0xc5c59154, 0x30306050,
      0x01010203, 0x6767cea9, 0x2b2b567d, 0xfefee719, 0xd7d7b562, 0xabab4de6, 0x7676ec9a, 0xcaca8f45, 0x82821f9d,
      0xc9c98940, 0x7d7dfa87, 0xfafaef15, 0x5959b2eb, 0x47478ec9, 0xf0f0fb0b, 0xadad41ec, 0xd4d4b367, 0xa2a25ffd,
      0xafaf45ea, 0x9c9c23bf, 0xa4a453f7, 0x7272e496, 0xc0c09b5b, 0xb7b775c2, 0xfdfde11c, 0x93933dae, 0x26264c6a,
      0x36366c5a, 0x3f3f7e41, 0xf7f7f502, 0xcccc834f, 0x3434685c, 0xa5a551f4, 0xe5e5d134, 0xf1f1f908, 0x7171e293,
      0xd8d8ab73, 0x31316253, 0x15152a3f, 0x0404080c, 0xc7c79552, 0x23234665, 0xc3c39d5e, 0x18183028, 0x969637a1,
      0x05050a0f, 0x9a9a2fb5, 0x07070e09, 0x12122436, 0x80801b9b, 0xe2e2df3d, 0xebebcd26, 0x27274e69, 0xb2b27fcd,
      0x7575ea9f, 0x0909121b, 0x83831d9e, 0x2c2c5874, 0x1a1a342e, 0x1b1b362d, 0x6e6edcb2, 0x5a5ab4ee, 0xa0a05bfb,
      0x5252a4f6, 0x3b3b764d, 0xd6d6b761, 0xb3b37dce, 0x2929527b, 0xe3e3dd3e, 0x2f2f5e71, 0x84841397, 0x5353a6f5,
      0xd1d1b968, 0x00000000, 0xededc12c, 0x20204060, 0xfcfce31f, 0xb1b179c8, 0x5b5bb6ed, 0x6a6ad4be, 0xcbcb8d46,
      0xbebe67d9, 0x3939724b, 0x4a4a94de, 0x4c4c98d4, 0x5858b0e8, 0xcfcf854a, 0xd0d0bb6b, 0xefefc52a, 0xaaaa4fe5,
      0xfbfbed16, 0x434386c5, 0x4d4d9ad7, 0x33336655, 0x85851194, 0x45458acf, 0xf9f9e910, 0x02020406, 0x7f7ffe81,
      0x5050a0f0, 0x3c3c7844, 0x9f9f25ba, 0xa8a84be3, 0x5151a2f3, 0xa3a35dfe, 0x404080c0, 0x8f8f058a, 0x92923fad,
      0x9d9d21bc, 0x38387048, 0xf5f5f104, 0xbcbc63df, 0xb6b677c1, 0xdadaaf75, 0x21214263, 0x10102030, 0xffffe51a,
      0xf3f3fd0e, 0xd2d2bf6d, 0xcdcd814c, 0x0c0c1814, 0x13132635, 0xececc32f, 0x5f5fbee1, 0x979735a2, 0x444488cc,
      0x17172e39, 0xc4c49357, 0xa7a755f2, 0x7e7efc82, 0x3d3d7a47, 0x6464c8ac, 0x5d5dbae7, 0x1919322b, 0x7373e695,
      0x6060c0a0, 0x81811998, 0x4f4f9ed1, 0xdcdca37f, 0x22224466, 0x2a2a547e, 0x90903bab, 0x88880b83, 0x46468cca,
      0xeeeec729, 0xb8b86bd3, 0x1414283c, 0xdedea779, 0x5e5ebce2, 0x0b0b161d, 0xdbdbad76, 0xe0e0db3b, 0x32326456,
      0x3a3a744e, 0x0a0a141e, 0x494992db, 0x06060c0a, 0x2424486c, 0x5c5cb8e4, 0xc2c29f5d, 0xd3d3bd6e, 0xacac43ef,
      0x6262c4a6, 0x919139a8, 0x959531a4, 0xe4e4d337, 0x7979f28b, 0xe7e7d532, 0xc8c88b43, 0x37376e59, 0x6d6ddab7,
      0x8d8d018c, 0xd5d5b164, 0x4e4e9cd2, 0xa9a949e0, 0x6c6cd8b4, 0x5656acfa, 0xf4f4f307, 0xeaeacf25, 0x6565caaf,
      0x7a7af48e, 0xaeae47e9, 0x08081018, 0xbaba6fd5, 0x7878f088, 0x25254a6f, 0x2e2e5c72, 0x1c1c3824, 0xa6a657f1,
      0xb4b473c7, 0xc6c69751, 0xe8e8cb23, 0xdddda17c, 0x7474e89c, 0x1f1f3e21, 0x4b4b96dd, 0xbdbd61dc, 0x8b8b0d86,
      0x8a8a0f85, 0x7070e090, 0x3e3e7c42, 0xb5b571c4, 0x6666ccaa, 0x484890d8, 0x03030605, 0xf6f6f701, 0x0e0e1c12,
      0x6161c2a3, 0x35356a5f, 0x5757aef9, 0xb9b969d0, 0x86861791, 0xc1c19958, 0x1d1d3a27, 0x9e9e27b9, 0xe1e1d938,
      0xf8f8eb13, 0x98982bb3, 0x11112233, 0x6969d2bb, 0xd9d9a970, 0x8e8e0789, 0x949433a7, 0x9b9b2db6, 0x1e1e3c22,
      0x87871592, 0xe9e9c920, 0xcece8749, 0x5555aaff, 0x28285078, 0xdfdfa57a, 0x8c8c038f, 0xa1a159f8, 0x89890980,
      0x0d0d1a17, 0xbfbf65da, 0xe6e6d731, 0x424284c6, 0x6868d0b8, 0x414182c3, 0x999929b0, 0x2d2d5a77, 0x0f0f1e11,
      0xb0b07bcb, 0x5454a8fc, 0xbbbb6dd6, 0x16162c3a]
S3 = [0x63c6a563, 0x7cf8847c, 0x77ee9977, 0x7bf68d7b, 0xf2ff0df2, 0x6bd6bd6b, 0x6fdeb16f, 0xc59154c5, 0x30605030,
      0x01020301, 0x67cea967, 0x2b567d2b, 0xfee719fe, 0xd7b562d7, 0xab4de6ab, 0x76ec9a76, 0xca8f45ca, 0x821f9d82,
      0xc98940c9, 0x7dfa877d, 0xfaef15fa, 0x59b2eb59, 0x478ec947, 0xf0fb0bf0, 0xad41ecad, 0xd4b367d4, 0xa25ffda2,
      0xaf45eaaf, 0x9c23bf9c, 0xa453f7a4, 0x72e49672, 0xc09b5bc0, 0xb775c2b7, 0xfde11cfd, 0x933dae93, 0x264c6a26,
      0x366c5a36, 0x3f7e413f, 0xf7f502f7, 0xcc834fcc, 0x34685c34, 0xa551f4a5, 0xe5d134e5, 0xf1f908f1, 0x71e29371,
      0xd8ab73d8, 0x31625331, 0x152a3f15, 0x04080c04, 0xc79552c7, 0x23466523, 0xc39d5ec3, 0x18302818, 0x9637a196,
      0x050a0f05, 0x9a2fb59a, 0x070e0907, 0x12243612, 0x801b9b80, 0xe2df3de2, 0xebcd26eb, 0x274e6927, 0xb27fcdb2,
      0x75ea9f75, 0x09121b09, 0x831d9e83, 0x2c58742c, 0x1a342e1a, 0x1b362d1b, 0x6edcb26e, 0x5ab4ee5a, 0xa05bfba0,
      0x52a4f652, 0x3b764d3b, 0xd6b761d6, 0xb37dceb3, 0x29527b29, 0xe3dd3ee3, 0x2f5e712f, 0x84139784, 0x53a6f553,
      0xd1b968d1, 0x00000000, 0xedc12ced, 0x20406020, 0xfce31ffc, 0xb179c8b1, 0x5bb6ed5b, 0x6ad4be6a, 0xcb8d46cb,
      0xbe67d9be, 0x39724b39, 0x4a94de4a, 0x4c98d44c, 0x58b0e858, 0xcf854acf, 0xd0bb6bd0, 0xefc52aef, 0xaa4fe5aa,
      0xfbed16fb, 0x4386c543, 0x4d9ad74d, 0x33665533, 0x85119485, 0x458acf45, 0xf9e910f9, 0x02040602, 0x7ffe817f,
      0x50a0f050, 0x3c78443c, 0x9f25ba9f, 0xa84be3a8, 0x51a2f351, 0xa35dfea3, 0x4080c040, 0x8f058a8f, 0x923fad92,
      0x9d21bc9d, 0x38704838, 0xf5f104f5, 0xbc63dfbc, 0xb677c1b6, 0xdaaf75da, 0x21426321, 0x10203010, 0xffe51aff,
      0xf3fd0ef3, 0xd2bf6dd2, 0xcd814ccd, 0x0c18140c, 0x13263513, 0xecc32fec, 0x5fbee15f, 0x9735a297, 0x4488cc44,
      0x172e3917, 0xc49357c4, 0xa755f2a7, 0x7efc827e, 0x3d7a473d, 0x64c8ac64, 0x5dbae75d, 0x19322b19, 0x73e69573,
      0x60c0a060, 0x81199881, 0x4f9ed14f, 0xdca37fdc, 0x22446622, 0x2a547e2a, 0x903bab90, 0x880b8388, 0x468cca46,
      0xeec729ee, 0xb86bd3b8, 0x14283c14, 0xdea779de, 0x5ebce25e, 0x0b161d0b, 0xdbad76db, 0xe0db3be0, 0x32645632,
      0x3a744e3a, 0x0a141e0a, 0x4992db49, 0x060c0a06, 0x24486c24, 0x5cb8e45c, 0xc29f5dc2, 0xd3bd6ed3, 0xac43efac,
      0x62c4a662, 0x9139a891, 0x9531a495, 0xe4d337e4, 0x79f28b79, 0xe7d532e7, 0xc88b43c8, 0x376e5937, 0x6ddab76d,
      0x8d018c8d, 0xd5b164d5, 0x4e9cd24e, 0xa949e0a9, 0x6cd8b46c, 0x56acfa56, 0xf4f307f4, 0xeacf25ea, 0x65caaf65,
      0x7af48e7a, 0xae47e9ae, 0x08101808, 0xba6fd5ba, 0x78f08878, 0x254a6f25, 0x2e5c722e, 0x1c38241c, 0xa657f1a6,
      0xb473c7b4, 0xc69751c6, 0xe8cb23e8, 0xdda17cdd, 0x74e89c74, 0x1f3e211f, 0x4b96dd4b, 0xbd61dcbd, 0x8b0d868b,
      0x8a0f858a, 0x70e09070, 0x3e7c423e, 0xb571c4b5, 0x66ccaa66, 0x4890d848, 0x03060503, 0xf6f701f6, 0x0e1c120e,
      0x61c2a361, 0x356a5f35, 0x57aef957, 0xb969d0b9, 0x86179186, 0xc19958c1, 0x1d3a271d, 0x9e27b99e, 0xe1d938e1,
      0xf8eb13f8, 0x982bb398, 0x11223311, 0x69d2bb69, 0xd9a970d9, 0x8e07898e, 0x9433a794, 0x9b2db69b, 0x1e3c221e,
      0x87159287, 0xe9c920e9, 0xce8749ce, 0x55aaff55, 0x28507828, 0xdfa57adf, 0x8c038f8c, 0xa159f8a1, 0x89098089,
      0x0d1a170d, 0xbf65dabf, 0xe6d731e6, 0x4284c642, 0x68d0b868, 0x4182c341, 0x9929b099, 0x2d5a772d, 0x0f1e110f,
      0xb07bcbb0, 0x54a8fc54, 0xbb6dd6bb, 0x162c3a16]
S4 = [0xc6a56363, 0xf8847c7c, 0xee997777, 0xf68d7b7b, 0xff0df2f2, 0xd6bd6b6b, 0xdeb16f6f, 0x9154c5c5, 0x60503030,
      0x02030101, 0xcea96767, 0x567d2b2b, 0xe719fefe, 0xb562d7d7, 0x4de6abab, 0xec9a7676, 0x8f45caca, 0x1f9d8282,
      0x8940c9c9, 0xfa877d7d, 0xef15fafa, 0xb2eb5959, 0x8ec94747, 0xfb0bf0f0, 0x41ecadad, 0xb367d4d4, 0x5ffda2a2,
      0x45eaafaf, 0x23bf9c9c, 0x53f7a4a4, 0xe4967272, 0x9b5bc0c0, 0x75c2b7b7, 0xe11cfdfd, 0x3dae9393, 0x4c6a2626,
      0x6c5a3636, 0x7e413f3f, 0xf502f7f7, 0x834fcccc, 0x685c3434, 0x51f4a5a5, 0xd134e5e5, 0xf908f1f1, 0xe2937171,
      0xab73d8d8, 0x62533131, 0x2a3f1515, 0x080c0404, 0x9552c7c7, 0x46652323, 0x9d5ec3c3, 0x30281818, 0x37a19696,
      0x0a0f0505, 0x2fb59a9a, 0x0e090707, 0x24361212, 0x1b9b8080, 0xdf3de2e2, 0xcd26ebeb, 0x4e692727, 0x7fcdb2b2,
      0xea9f7575, 0x121b0909, 0x1d9e8383, 0x58742c2c, 0x342e1a1a, 0x362d1b1b, 0xdcb26e6e, 0xb4ee5a5a, 0x5bfba0a0,
      0xa4f65252, 0x764d3b3b, 0xb761d6d6, 0x7dceb3b3, 0x527b2929, 0xdd3ee3e3, 0x5e712f2f, 0x13978484, 0xa6f55353,
      0xb968d1d1, 0x00000000, 0xc12ceded, 0x40602020, 0xe31ffcfc, 0x79c8b1b1, 0xb6ed5b5b, 0xd4be6a6a, 0x8d46cbcb,
      0x67d9bebe, 0x724b3939, 0x94de4a4a, 0x98d44c4c, 0xb0e85858, 0x854acfcf, 0xbb6bd0d0, 0xc52aefef, 0x4fe5aaaa,
      0xed16fbfb, 0x86c54343, 0x9ad74d4d, 0x66553333, 0x11948585, 0x8acf4545, 0xe910f9f9, 0x04060202, 0xfe817f7f,
      0xa0f05050, 0x78443c3c, 0x25ba9f9f, 0x4be3a8a8, 0xa2f35151, 0x5dfea3a3, 0x80c04040, 0x058a8f8f, 0x3fad9292,
      0x21bc9d9d, 0x70483838, 0xf104f5f5, 0x63dfbcbc, 0x77c1b6b6, 0xaf75dada, 0x42632121, 0x20301010, 0xe51affff,
      0xfd0ef3f3, 0xbf6dd2d2, 0x814ccdcd, 0x18140c0c, 0x26351313, 0xc32fecec, 0xbee15f5f, 0x35a29797, 0x88cc4444,
      0x2e391717, 0x9357c4c4, 0x55f2a7a7, 0xfc827e7e, 0x7a473d3d, 0xc8ac6464, 0xbae75d5d, 0x322b1919, 0xe6957373,
      0xc0a06060, 0x19988181, 0x9ed14f4f, 0xa37fdcdc, 0x44662222, 0x547e2a2a, 0x3bab9090, 0x0b838888, 0x8cca4646,
      0xc729eeee, 0x6bd3b8b8, 0x283c1414, 0xa779dede, 0xbce25e5e, 0x161d0b0b, 0xad76dbdb, 0xdb3be0e0, 0x64563232,
      0x744e3a3a, 0x141e0a0a, 0x92db4949, 0x0c0a0606, 0x486c2424, 0xb8e45c5c, 0x9f5dc2c2, 0xbd6ed3d3, 0x43efacac,
      0xc4a66262, 0x39a89191, 0x31a49595, 0xd337e4e4, 0xf28b7979, 0xd532e7e7, 0x8b43c8c8, 0x6e593737, 0xdab76d6d,
      0x018c8d8d, 0xb164d5d5, 0x9cd24e4e, 0x49e0a9a9, 0xd8b46c6c, 0xacfa5656, 0xf307f4f4, 0xcf25eaea, 0xcaaf6565,
      0xf48e7a7a, 0x47e9aeae, 0x10180808, 0x6fd5baba, 0xf0887878, 0x4a6f2525, 0x5c722e2e, 0x38241c1c, 0x57f1a6a6,
      0x73c7b4b4, 0x9751c6c6, 0xcb23e8e8, 0xa17cdddd, 0xe89c7474, 0x3e211f1f, 0x96dd4b4b, 0x61dcbdbd, 0x0d868b8b,
      0x0f858a8a, 0xe0907070, 0x7c423e3e, 0x71c4b5b5, 0xccaa6666, 0x90d84848, 0x06050303, 0xf701f6f6, 0x1c120e0e,
      0xc2a36161, 0x6a5f3535, 0xaef95757, 0x69d0b9b9, 0x17918686, 0x9958c1c1, 0x3a271d1d, 0x27b99e9e, 0xd938e1e1,
      0xeb13f8f8, 0x2bb39898, 0x22331111, 0xd2bb6969, 0xa970d9d9, 0x07898e8e, 0x33a79494, 0x2db69b9b, 0x3c221e1e,
      0x15928787, 0xc920e9e9, 0x8749cece, 0xaaff5555, 0x50782828, 0xa57adfdf, 0x038f8c8c, 0x59f8a1a1, 0x09808989,
      0x1a170d0d, 0x65dabfbf, 0xd731e6e6, 0x84c64242, 0xd0b86868, 0x82c34141, 0x29b09999, 0x5a772d2d, 0x1e110f0f,
      0x7bcbb0b0, 0xa8fc5454, 0x6dd6bbbb, 0x2c3a1616]
SBox = [a & 255 for a in S3]

groestlT = [
    0xa5f432c6L, 0x84976ff8L, 0x99b05eeeL, 0x8d8c7af6L, 0x0d17e8ffL, 0xbddc0ad6L, 0xb1c816deL, 0x54fc6d91L, 0x50f09060L,
    0x03050702L, 0xa9e02eceL, 0x7d87d156L, 0x192bcce7L, 0x62a613b5L, 0xe6317c4dL, 0x9ab559ecL, 0x45cf408fL, 0x9dbca31fL,
    0x40c04989L, 0x879268faL, 0x153fd0efL, 0xeb2694b2L, 0xc940ce8eL, 0x0b1de6fbL, 0xec2f6e41L, 0x67a91ab3L, 0xfd1c435fL,
    0xea256045L, 0xbfdaf923L, 0xf7025153L, 0x96a145e4L, 0x5bed769bL, 0xc25d2875L, 0x1c24c5e1L, 0xaee9d43dL, 0x6abef24cL,
    0x5aee826cL, 0x41c3bd7eL, 0x0206f3f5L, 0x4fd15283L, 0x5ce48c68L, 0xf4075651L, 0x345c8dd1L, 0x0818e1f9L, 0x93ae4ce2L,
    0x73953eabL, 0x53f59762L, 0x3f416b2aL, 0x0c141c08L, 0x52f66395L, 0x65afe946L, 0x5ee27f9dL, 0x28784830L, 0xa1f8cf37L,
    0x0f111b0aL, 0xb5c4eb2fL, 0x091b150eL, 0x365a7e24L, 0x9bb6ad1bL, 0x3d4798dfL, 0x266aa7cdL, 0x69bbf54eL, 0xcd4c337fL,
    0x9fba50eaL, 0x1b2d3f12L, 0x9eb9a41dL, 0x749cc458L, 0x2e724634L, 0x2d774136L, 0xb2cd11dcL, 0xee299db4L, 0xfb164d5bL,
    0xf601a5a4L, 0x4dd7a176L, 0x61a314b7L, 0xce49347dL, 0x7b8ddf52L, 0x3e429fddL, 0x7193cd5eL, 0x97a2b113L, 0xf504a2a6L,
    0x68b801b9L, 0x00000000L, 0x2c74b5c1L, 0x60a0e040L, 0x1f21c2e3L, 0xc8433a79L, 0xed2c9ab6L, 0xbed90dd4L, 0x46ca478dL,
    0xd9701767L, 0x4bddaf72L, 0xde79ed94L, 0xd467ff98L, 0xe82393b0L, 0x4ade5b85L, 0x6bbd06bbL, 0x2a7ebbc5L, 0xe5347b4fL,
    0x163ad7edL, 0xc554d286L, 0xd762f89aL, 0x55ff9966L, 0x94a7b611L, 0xcf4ac08aL, 0x1030d9e9L, 0x060a0e04L, 0x819866feL,
    0xf00baba0L, 0x44ccb478L, 0xbad5f025L, 0xe33e754bL, 0xf30eaca2L, 0xfe19445dL, 0xc05bdb80L, 0x8a858005L, 0xadecd33fL,
    0xbcdffe21L, 0x48d8a870L, 0x040cfdf1L, 0xdf7a1963L, 0xc1582f77L, 0x759f30afL, 0x63a5e742L, 0x30507020L, 0x1a2ecbe5L,
    0x0e12effdL, 0x6db708bfL, 0x4cd45581L, 0x143c2418L, 0x355f7926L, 0x2f71b2c3L, 0xe13886beL, 0xa2fdc835L, 0xcc4fc788L,
    0x394b652eL, 0x57f96a93L, 0xf20d5855L, 0x829d61fcL, 0x47c9b37aL, 0xacef27c8L, 0xe73288baL, 0x2b7d4f32L, 0x95a442e6L,
    0xa0fb3bc0L, 0x98b3aa19L, 0xd168f69eL, 0x7f8122a3L, 0x66aaee44L, 0x7e82d654L, 0xabe6dd3bL, 0x839e950bL, 0xca45c98cL,
    0x297bbcc7L, 0xd36e056bL, 0x3c446c28L, 0x798b2ca7L, 0xe23d81bcL, 0x1d273116L, 0x769a37adL, 0x3b4d96dbL, 0x56fa9e64L,
    0x4ed2a674L, 0x1e223614L, 0xdb76e492L, 0x0a1e120cL, 0x6cb4fc48L, 0xe4378fb8L, 0x5de7789fL, 0x6eb20fbdL, 0xef2a6943L,
    0xa6f135c4L, 0xa8e3da39L, 0xa4f7c631L, 0x37598ad3L, 0x8b8674f2L, 0x325683d5L, 0x43c54e8bL, 0x59eb856eL, 0xb7c218daL,
    0x8c8f8e01L, 0x64ac1db1L, 0xd26df19cL, 0xe03b7249L, 0xb4c71fd8L, 0xfa15b9acL, 0x0709faf3L, 0x256fa0cfL, 0xafea20caL,
    0x8e897df4L, 0xe9206747L, 0x18283810L, 0xd5640b6fL, 0x888373f0L, 0x6fb1fb4aL, 0x7296ca5cL, 0x246c5438L, 0xf1085f57L,
    0xc7522173L, 0x51f36497L, 0x2365aecbL, 0x7c8425a1L, 0x9cbf57e8L, 0x21635d3eL, 0xdd7cea96L, 0xdc7f1e61L, 0x86919c0dL,
    0x85949b0fL, 0x90ab4be0L, 0x42c6ba7cL, 0xc4572671L, 0xaae529ccL, 0xd873e390L, 0x050f0906L, 0x0103f4f7L, 0x12362a1cL,
    0xa3fe3cc2L, 0x5fe18b6aL, 0xf910beaeL, 0xd06b0269L, 0x91a8bf17L, 0x58e87199L, 0x2769533aL, 0xb9d0f727L, 0x384891d9L,
    0x1335deebL, 0xb3cee52bL, 0x33557722L, 0xbbd604d2L, 0x709039a9L, 0x89808707L, 0xa7f2c133L, 0xb6c1ec2dL, 0x22665a3cL,
    0x92adb815L, 0x2060a9c9L, 0x49db5c87L, 0xff1ab0aaL, 0x7888d850L, 0x7a8e2ba5L, 0x8f8a8903L, 0xf8134a59L, 0x809b9209L,
    0x1739231aL, 0xda751065L, 0x315384d7L, 0xc651d584L, 0xb8d303d0L, 0xc35edc82L, 0xb0cbe229L, 0x7799c35aL, 0x11332d1eL,
    0xcb463d7bL, 0xfc1fb7a8L, 0xd6610c6dL, 0x3a4e622cL,
    0xf432c6c6L, 0x976ff8f8L, 0xb05eeeeeL, 0x8c7af6f6L, 0x17e8ffffL, 0xdc0ad6d6L, 0xc816dedeL, 0xfc6d9191L, 0xf0906060L,
    0x05070202L, 0xe02ececeL, 0x87d15656L, 0x2bcce7e7L, 0xa613b5b5L, 0x317c4d4dL, 0xb559ececL, 0xcf408f8fL, 0xbca31f1fL,
    0xc0498989L, 0x9268fafaL, 0x3fd0efefL, 0x2694b2b2L, 0x40ce8e8eL, 0x1de6fbfbL, 0x2f6e4141L, 0xa91ab3b3L, 0x1c435f5fL,
    0x25604545L, 0xdaf92323L, 0x02515353L, 0xa145e4e4L, 0xed769b9bL, 0x5d287575L, 0x24c5e1e1L, 0xe9d43d3dL, 0xbef24c4cL,
    0xee826c6cL, 0xc3bd7e7eL, 0x06f3f5f5L, 0xd1528383L, 0xe48c6868L, 0x07565151L, 0x5c8dd1d1L, 0x18e1f9f9L, 0xae4ce2e2L,
    0x953eababL, 0xf5976262L, 0x416b2a2aL, 0x141c0808L, 0xf6639595L, 0xafe94646L, 0xe27f9d9dL, 0x78483030L, 0xf8cf3737L,
    0x111b0a0aL, 0xc4eb2f2fL, 0x1b150e0eL, 0x5a7e2424L, 0xb6ad1b1bL, 0x4798dfdfL, 0x6aa7cdcdL, 0xbbf54e4eL, 0x4c337f7fL,
    0xba50eaeaL, 0x2d3f1212L, 0xb9a41d1dL, 0x9cc45858L, 0x72463434L, 0x77413636L, 0xcd11dcdcL, 0x299db4b4L, 0x164d5b5bL,
    0x01a5a4a4L, 0xd7a17676L, 0xa314b7b7L, 0x49347d7dL, 0x8ddf5252L, 0x429fddddL, 0x93cd5e5eL, 0xa2b11313L, 0x04a2a6a6L,
    0xb801b9b9L, 0x00000000L, 0x74b5c1c1L, 0xa0e04040L, 0x21c2e3e3L, 0x433a7979L, 0x2c9ab6b6L, 0xd90dd4d4L, 0xca478d8dL,
    0x70176767L, 0xddaf7272L, 0x79ed9494L, 0x67ff9898L, 0x2393b0b0L, 0xde5b8585L, 0xbd06bbbbL, 0x7ebbc5c5L, 0x347b4f4fL,
    0x3ad7ededL, 0x54d28686L, 0x62f89a9aL, 0xff996666L, 0xa7b61111L, 0x4ac08a8aL, 0x30d9e9e9L, 0x0a0e0404L, 0x9866fefeL,
    0x0baba0a0L, 0xccb47878L, 0xd5f02525L, 0x3e754b4bL, 0x0eaca2a2L, 0x19445d5dL, 0x5bdb8080L, 0x85800505L, 0xecd33f3fL,
    0xdffe2121L, 0xd8a87070L, 0x0cfdf1f1L, 0x7a196363L, 0x582f7777L, 0x9f30afafL, 0xa5e74242L, 0x50702020L, 0x2ecbe5e5L,
    0x12effdfdL, 0xb708bfbfL, 0xd4558181L, 0x3c241818L, 0x5f792626L, 0x71b2c3c3L, 0x3886bebeL, 0xfdc83535L, 0x4fc78888L,
    0x4b652e2eL, 0xf96a9393L, 0x0d585555L, 0x9d61fcfcL, 0xc9b37a7aL, 0xef27c8c8L, 0x3288babaL, 0x7d4f3232L, 0xa442e6e6L,
    0xfb3bc0c0L, 0xb3aa1919L, 0x68f69e9eL, 0x8122a3a3L, 0xaaee4444L, 0x82d65454L, 0xe6dd3b3bL, 0x9e950b0bL, 0x45c98c8cL,
    0x7bbcc7c7L, 0x6e056b6bL, 0x446c2828L, 0x8b2ca7a7L, 0x3d81bcbcL, 0x27311616L, 0x9a37adadL, 0x4d96dbdbL, 0xfa9e6464L,
    0xd2a67474L, 0x22361414L, 0x76e49292L, 0x1e120c0cL, 0xb4fc4848L, 0x378fb8b8L, 0xe7789f9fL, 0xb20fbdbdL, 0x2a694343L,
    0xf135c4c4L, 0xe3da3939L, 0xf7c63131L, 0x598ad3d3L, 0x8674f2f2L, 0x5683d5d5L, 0xc54e8b8bL, 0xeb856e6eL, 0xc218dadaL,
    0x8f8e0101L, 0xac1db1b1L, 0x6df19c9cL, 0x3b724949L, 0xc71fd8d8L, 0x15b9acacL, 0x09faf3f3L, 0x6fa0cfcfL, 0xea20cacaL,
    0x897df4f4L, 0x20674747L, 0x28381010L, 0x640b6f6fL, 0x8373f0f0L, 0xb1fb4a4aL, 0x96ca5c5cL, 0x6c543838L, 0x085f5757L,
    0x52217373L, 0xf3649797L, 0x65aecbcbL, 0x8425a1a1L, 0xbf57e8e8L, 0x635d3e3eL, 0x7cea9696L, 0x7f1e6161L, 0x919c0d0dL,
    0x949b0f0fL, 0xab4be0e0L, 0xc6ba7c7cL, 0x57267171L, 0xe529ccccL, 0x73e39090L, 0x0f090606L, 0x03f4f7f7L, 0x362a1c1cL,
    0xfe3cc2c2L, 0xe18b6a6aL, 0x10beaeaeL, 0x6b026969L, 0xa8bf1717L, 0xe8719999L, 0x69533a3aL, 0xd0f72727L, 0x4891d9d9L,
    0x35deebebL, 0xcee52b2bL, 0x55772222L, 0xd604d2d2L, 0x9039a9a9L, 0x80870707L, 0xf2c13333L, 0xc1ec2d2dL, 0x665a3c3cL,
    0xadb81515L, 0x60a9c9c9L, 0xdb5c8787L, 0x1ab0aaaaL, 0x88d85050L, 0x8e2ba5a5L, 0x8a890303L, 0x134a5959L, 0x9b920909L,
    0x39231a1aL, 0x75106565L, 0x5384d7d7L, 0x51d58484L, 0xd303d0d0L, 0x5edc8282L, 0xcbe22929L, 0x99c35a5aL, 0x332d1e1eL,
    0x463d7b7bL, 0x1fb7a8a8L, 0x610c6d6dL, 0x4e622c2cL,
    0x32c6c6a5L, 0x6ff8f884L, 0x5eeeee99L, 0x7af6f68dL, 0xe8ffff0dL, 0x0ad6d6bdL, 0x16dedeb1L, 0x6d919154L, 0x90606050L,
    0x07020203L, 0x2ececea9L, 0xd156567dL, 0xcce7e719L, 0x13b5b562L, 0x7c4d4de6L, 0x59ecec9aL, 0x408f8f45L, 0xa31f1f9dL,
    0x49898940L, 0x68fafa87L, 0xd0efef15L, 0x94b2b2ebL, 0xce8e8ec9L, 0xe6fbfb0bL, 0x6e4141ecL, 0x1ab3b367L, 0x435f5ffdL,
    0x604545eaL, 0xf92323bfL, 0x515353f7L, 0x45e4e496L, 0x769b9b5bL, 0x287575c2L, 0xc5e1e11cL, 0xd43d3daeL, 0xf24c4c6aL,
    0x826c6c5aL, 0xbd7e7e41L, 0xf3f5f502L, 0x5283834fL, 0x8c68685cL, 0x565151f4L, 0x8dd1d134L, 0xe1f9f908L, 0x4ce2e293L,
    0x3eabab73L, 0x97626253L, 0x6b2a2a3fL, 0x1c08080cL, 0x63959552L, 0xe9464665L, 0x7f9d9d5eL, 0x48303028L, 0xcf3737a1L,
    0x1b0a0a0fL, 0xeb2f2fb5L, 0x150e0e09L, 0x7e242436L, 0xad1b1b9bL, 0x98dfdf3dL, 0xa7cdcd26L, 0xf54e4e69L, 0x337f7fcdL,
    0x50eaea9fL, 0x3f12121bL, 0xa41d1d9eL, 0xc4585874L, 0x4634342eL, 0x4136362dL, 0x11dcdcb2L, 0x9db4b4eeL, 0x4d5b5bfbL,
    0xa5a4a4f6L, 0xa176764dL, 0x14b7b761L, 0x347d7dceL, 0xdf52527bL, 0x9fdddd3eL, 0xcd5e5e71L, 0xb1131397L, 0xa2a6a6f5L,
    0x01b9b968L, 0x00000000L, 0xb5c1c12cL, 0xe0404060L, 0xc2e3e31fL, 0x3a7979c8L, 0x9ab6b6edL, 0x0dd4d4beL, 0x478d8d46L,
    0x176767d9L, 0xaf72724bL, 0xed9494deL, 0xff9898d4L, 0x93b0b0e8L, 0x5b85854aL, 0x06bbbb6bL, 0xbbc5c52aL, 0x7b4f4fe5L,
    0xd7eded16L, 0xd28686c5L, 0xf89a9ad7L, 0x99666655L, 0xb6111194L, 0xc08a8acfL, 0xd9e9e910L, 0x0e040406L, 0x66fefe81L,
    0xaba0a0f0L, 0xb4787844L, 0xf02525baL, 0x754b4be3L, 0xaca2a2f3L, 0x445d5dfeL, 0xdb8080c0L, 0x8005058aL, 0xd33f3fadL,
    0xfe2121bcL, 0xa8707048L, 0xfdf1f104L, 0x196363dfL, 0x2f7777c1L, 0x30afaf75L, 0xe7424263L, 0x70202030L, 0xcbe5e51aL,
    0xeffdfd0eL, 0x08bfbf6dL, 0x5581814cL, 0x24181814L, 0x79262635L, 0xb2c3c32fL, 0x86bebee1L, 0xc83535a2L, 0xc78888ccL,
    0x652e2e39L, 0x6a939357L, 0x585555f2L, 0x61fcfc82L, 0xb37a7a47L, 0x27c8c8acL, 0x88babae7L, 0x4f32322bL, 0x42e6e695L,
    0x3bc0c0a0L, 0xaa191998L, 0xf69e9ed1L, 0x22a3a37fL, 0xee444466L, 0xd654547eL, 0xdd3b3babL, 0x950b0b83L, 0xc98c8ccaL,
    0xbcc7c729L, 0x056b6bd3L, 0x6c28283cL, 0x2ca7a779L, 0x81bcbce2L, 0x3116161dL, 0x37adad76L, 0x96dbdb3bL, 0x9e646456L,
    0xa674744eL, 0x3614141eL, 0xe49292dbL, 0x120c0c0aL, 0xfc48486cL, 0x8fb8b8e4L, 0x789f9f5dL, 0x0fbdbd6eL, 0x694343efL,
    0x35c4c4a6L, 0xda3939a8L, 0xc63131a4L, 0x8ad3d337L, 0x74f2f28bL, 0x83d5d532L, 0x4e8b8b43L, 0x856e6e59L, 0x18dadab7L,
    0x8e01018cL, 0x1db1b164L, 0xf19c9cd2L, 0x724949e0L, 0x1fd8d8b4L, 0xb9acacfaL, 0xfaf3f307L, 0xa0cfcf25L, 0x20cacaafL,
    0x7df4f48eL, 0x674747e9L, 0x38101018L, 0x0b6f6fd5L, 0x73f0f088L, 0xfb4a4a6fL, 0xca5c5c72L, 0x54383824L, 0x5f5757f1L,
    0x217373c7L, 0x64979751L, 0xaecbcb23L, 0x25a1a17cL, 0x57e8e89cL, 0x5d3e3e21L, 0xea9696ddL, 0x1e6161dcL, 0x9c0d0d86L,
    0x9b0f0f85L, 0x4be0e090L, 0xba7c7c42L, 0x267171c4L, 0x29ccccaaL, 0xe39090d8L, 0x09060605L, 0xf4f7f701L, 0x2a1c1c12L,
    0x3cc2c2a3L, 0x8b6a6a5fL, 0xbeaeaef9L, 0x026969d0L, 0xbf171791L, 0x71999958L, 0x533a3a27L, 0xf72727b9L, 0x91d9d938L,
    0xdeebeb13L, 0xe52b2bb3L, 0x77222233L, 0x04d2d2bbL, 0x39a9a970L, 0x87070789L, 0xc13333a7L, 0xec2d2db6L, 0x5a3c3c22L,
    0xb8151592L, 0xa9c9c920L, 0x5c878749L, 0xb0aaaaffL, 0xd8505078L, 0x2ba5a57aL, 0x8903038fL, 0x4a5959f8L, 0x92090980L,
    0x231a1a17L, 0x106565daL, 0x84d7d731L, 0xd58484c6L, 0x03d0d0b8L, 0xdc8282c3L, 0xe22929b0L, 0xc35a5a77L, 0x2d1e1e11L,
    0x3d7b7bcbL, 0xb7a8a8fcL, 0x0c6d6dd6L, 0x622c2c3aL,
    0xc6c6a597L, 0xf8f884ebL, 0xeeee99c7L, 0xf6f68df7L, 0xffff0de5L, 0xd6d6bdb7L, 0xdedeb1a7L, 0x91915439L, 0x606050c0L,
    0x02020304L, 0xcecea987L, 0x56567dacL, 0xe7e719d5L, 0xb5b56271L, 0x4d4de69aL, 0xecec9ac3L, 0x8f8f4505L, 0x1f1f9d3eL,
    0x89894009L, 0xfafa87efL, 0xefef15c5L, 0xb2b2eb7fL, 0x8e8ec907L, 0xfbfb0bedL, 0x4141ec82L, 0xb3b3677dL, 0x5f5ffdbeL,
    0x4545ea8aL, 0x2323bf46L, 0x5353f7a6L, 0xe4e496d3L, 0x9b9b5b2dL, 0x7575c2eaL, 0xe1e11cd9L, 0x3d3dae7aL, 0x4c4c6a98L,
    0x6c6c5ad8L, 0x7e7e41fcL, 0xf5f502f1L, 0x83834f1dL, 0x68685cd0L, 0x5151f4a2L, 0xd1d134b9L, 0xf9f908e9L, 0xe2e293dfL,
    0xabab734dL, 0x626253c4L, 0x2a2a3f54L, 0x08080c10L, 0x95955231L, 0x4646658cL, 0x9d9d5e21L, 0x30302860L, 0x3737a16eL,
    0x0a0a0f14L, 0x2f2fb55eL, 0x0e0e091cL, 0x24243648L, 0x1b1b9b36L, 0xdfdf3da5L, 0xcdcd2681L, 0x4e4e699cL, 0x7f7fcdfeL,
    0xeaea9fcfL, 0x12121b24L, 0x1d1d9e3aL, 0x585874b0L, 0x34342e68L, 0x36362d6cL, 0xdcdcb2a3L, 0xb4b4ee73L, 0x5b5bfbb6L,
    0xa4a4f653L, 0x76764decL, 0xb7b76175L, 0x7d7dcefaL, 0x52527ba4L, 0xdddd3ea1L, 0x5e5e71bcL, 0x13139726L, 0xa6a6f557L,
    0xb9b96869L, 0x00000000L, 0xc1c12c99L, 0x40406080L, 0xe3e31fddL, 0x7979c8f2L, 0xb6b6ed77L, 0xd4d4beb3L, 0x8d8d4601L,
    0x6767d9ceL, 0x72724be4L, 0x9494de33L, 0x9898d42bL, 0xb0b0e87bL, 0x85854a11L, 0xbbbb6b6dL, 0xc5c52a91L, 0x4f4fe59eL,
    0xeded16c1L, 0x8686c517L, 0x9a9ad72fL, 0x666655ccL, 0x11119422L, 0x8a8acf0fL, 0xe9e910c9L, 0x04040608L, 0xfefe81e7L,
    0xa0a0f05bL, 0x787844f0L, 0x2525ba4aL, 0x4b4be396L, 0xa2a2f35fL, 0x5d5dfebaL, 0x8080c01bL, 0x05058a0aL, 0x3f3fad7eL,
    0x2121bc42L, 0x707048e0L, 0xf1f104f9L, 0x6363dfc6L, 0x7777c1eeL, 0xafaf7545L, 0x42426384L, 0x20203040L, 0xe5e51ad1L,
    0xfdfd0ee1L, 0xbfbf6d65L, 0x81814c19L, 0x18181430L, 0x2626354cL, 0xc3c32f9dL, 0xbebee167L, 0x3535a26aL, 0x8888cc0bL,
    0x2e2e395cL, 0x9393573dL, 0x5555f2aaL, 0xfcfc82e3L, 0x7a7a47f4L, 0xc8c8ac8bL, 0xbabae76fL, 0x32322b64L, 0xe6e695d7L,
    0xc0c0a09bL, 0x19199832L, 0x9e9ed127L, 0xa3a37f5dL, 0x44446688L, 0x54547ea8L, 0x3b3bab76L, 0x0b0b8316L, 0x8c8cca03L,
    0xc7c72995L, 0x6b6bd3d6L, 0x28283c50L, 0xa7a77955L, 0xbcbce263L, 0x16161d2cL, 0xadad7641L, 0xdbdb3badL, 0x646456c8L,
    0x74744ee8L, 0x14141e28L, 0x9292db3fL, 0x0c0c0a18L, 0x48486c90L, 0xb8b8e46bL, 0x9f9f5d25L, 0xbdbd6e61L, 0x4343ef86L,
    0xc4c4a693L, 0x3939a872L, 0x3131a462L, 0xd3d337bdL, 0xf2f28bffL, 0xd5d532b1L, 0x8b8b430dL, 0x6e6e59dcL, 0xdadab7afL,
    0x01018c02L, 0xb1b16479L, 0x9c9cd223L, 0x4949e092L, 0xd8d8b4abL, 0xacacfa43L, 0xf3f307fdL, 0xcfcf2585L, 0xcacaaf8fL,
    0xf4f48ef3L, 0x4747e98eL, 0x10101820L, 0x6f6fd5deL, 0xf0f088fbL, 0x4a4a6f94L, 0x5c5c72b8L, 0x38382470L, 0x5757f1aeL,
    0x7373c7e6L, 0x97975135L, 0xcbcb238dL, 0xa1a17c59L, 0xe8e89ccbL, 0x3e3e217cL, 0x9696dd37L, 0x6161dcc2L, 0x0d0d861aL,
    0x0f0f851eL, 0xe0e090dbL, 0x7c7c42f8L, 0x7171c4e2L, 0xccccaa83L, 0x9090d83bL, 0x0606050cL, 0xf7f701f5L, 0x1c1c1238L,
    0xc2c2a39fL, 0x6a6a5fd4L, 0xaeaef947L, 0x6969d0d2L, 0x1717912eL, 0x99995829L, 0x3a3a2774L, 0x2727b94eL, 0xd9d938a9L,
    0xebeb13cdL, 0x2b2bb356L, 0x22223344L, 0xd2d2bbbfL, 0xa9a97049L, 0x0707890eL, 0x3333a766L, 0x2d2db65aL, 0x3c3c2278L,
    0x1515922aL, 0xc9c92089L, 0x87874915L, 0xaaaaff4fL, 0x505078a0L, 0xa5a57a51L, 0x03038f06L, 0x5959f8b2L, 0x09098012L,
    0x1a1a1734L, 0x6565dacaL, 0xd7d731b5L, 0x8484c613L, 0xd0d0b8bbL, 0x8282c31fL, 0x2929b052L, 0x5a5a77b4L, 0x1e1e113cL,
    0x7b7bcbf6L, 0xa8a8fc4bL, 0x6d6dd6daL, 0x2c2c3a58L,
    0xc6a597f4L, 0xf884eb97L, 0xee99c7b0L, 0xf68df78cL, 0xff0de517L, 0xd6bdb7dcL, 0xdeb1a7c8L, 0x915439fcL, 0x6050c0f0L,
    0x02030405L, 0xcea987e0L, 0x567dac87L, 0xe719d52bL, 0xb56271a6L, 0x4de69a31L, 0xec9ac3b5L, 0x8f4505cfL, 0x1f9d3ebcL,
    0x894009c0L, 0xfa87ef92L, 0xef15c53fL, 0xb2eb7f26L, 0x8ec90740L, 0xfb0bed1dL, 0x41ec822fL, 0xb3677da9L, 0x5ffdbe1cL,
    0x45ea8a25L, 0x23bf46daL, 0x53f7a602L, 0xe496d3a1L, 0x9b5b2dedL, 0x75c2ea5dL, 0xe11cd924L, 0x3dae7ae9L, 0x4c6a98beL,
    0x6c5ad8eeL, 0x7e41fcc3L, 0xf502f106L, 0x834f1dd1L, 0x685cd0e4L, 0x51f4a207L, 0xd134b95cL, 0xf908e918L, 0xe293dfaeL,
    0xab734d95L, 0x6253c4f5L, 0x2a3f5441L, 0x080c1014L, 0x955231f6L, 0x46658cafL, 0x9d5e21e2L, 0x30286078L, 0x37a16ef8L,
    0x0a0f1411L, 0x2fb55ec4L, 0x0e091c1bL, 0x2436485aL, 0x1b9b36b6L, 0xdf3da547L, 0xcd26816aL, 0x4e699cbbL, 0x7fcdfe4cL,
    0xea9fcfbaL, 0x121b242dL, 0x1d9e3ab9L, 0x5874b09cL, 0x342e6872L, 0x362d6c77L, 0xdcb2a3cdL, 0xb4ee7329L, 0x5bfbb616L,
    0xa4f65301L, 0x764decd7L, 0xb76175a3L, 0x7dcefa49L, 0x527ba48dL, 0xdd3ea142L, 0x5e71bc93L, 0x139726a2L, 0xa6f55704L,
    0xb96869b8L, 0x00000000L, 0xc12c9974L, 0x406080a0L, 0xe31fdd21L, 0x79c8f243L, 0xb6ed772cL, 0xd4beb3d9L, 0x8d4601caL,
    0x67d9ce70L, 0x724be4ddL, 0x94de3379L, 0x98d42b67L, 0xb0e87b23L, 0x854a11deL, 0xbb6b6dbdL, 0xc52a917eL, 0x4fe59e34L,
    0xed16c13aL, 0x86c51754L, 0x9ad72f62L, 0x6655ccffL, 0x119422a7L, 0x8acf0f4aL, 0xe910c930L, 0x0406080aL, 0xfe81e798L,
    0xa0f05b0bL, 0x7844f0ccL, 0x25ba4ad5L, 0x4be3963eL, 0xa2f35f0eL, 0x5dfeba19L, 0x80c01b5bL, 0x058a0a85L, 0x3fad7eecL,
    0x21bc42dfL, 0x7048e0d8L, 0xf104f90cL, 0x63dfc67aL, 0x77c1ee58L, 0xaf75459fL, 0x426384a5L, 0x20304050L, 0xe51ad12eL,
    0xfd0ee112L, 0xbf6d65b7L, 0x814c19d4L, 0x1814303cL, 0x26354c5fL, 0xc32f9d71L, 0xbee16738L, 0x35a26afdL, 0x88cc0b4fL,
    0x2e395c4bL, 0x93573df9L, 0x55f2aa0dL, 0xfc82e39dL, 0x7a47f4c9L, 0xc8ac8befL, 0xbae76f32L, 0x322b647dL, 0xe695d7a4L,
    0xc0a09bfbL, 0x199832b3L, 0x9ed12768L, 0xa37f5d81L, 0x446688aaL, 0x547ea882L, 0x3bab76e6L, 0x0b83169eL, 0x8cca0345L,
    0xc729957bL, 0x6bd3d66eL, 0x283c5044L, 0xa779558bL, 0xbce2633dL, 0x161d2c27L, 0xad76419aL, 0xdb3bad4dL, 0x6456c8faL,
    0x744ee8d2L, 0x141e2822L, 0x92db3f76L, 0x0c0a181eL, 0x486c90b4L, 0xb8e46b37L, 0x9f5d25e7L, 0xbd6e61b2L, 0x43ef862aL,
    0xc4a693f1L, 0x39a872e3L, 0x31a462f7L, 0xd337bd59L, 0xf28bff86L, 0xd532b156L, 0x8b430dc5L, 0x6e59dcebL, 0xdab7afc2L,
    0x018c028fL, 0xb16479acL, 0x9cd2236dL, 0x49e0923bL, 0xd8b4abc7L, 0xacfa4315L, 0xf307fd09L, 0xcf25856fL, 0xcaaf8feaL,
    0xf48ef389L, 0x47e98e20L, 0x10182028L, 0x6fd5de64L, 0xf088fb83L, 0x4a6f94b1L, 0x5c72b896L, 0x3824706cL, 0x57f1ae08L,
    0x73c7e652L, 0x975135f3L, 0xcb238d65L, 0xa17c5984L, 0xe89ccbbfL, 0x3e217c63L, 0x96dd377cL, 0x61dcc27fL, 0x0d861a91L,
    0x0f851e94L, 0xe090dbabL, 0x7c42f8c6L, 0x71c4e257L, 0xccaa83e5L, 0x90d83b73L, 0x06050c0fL, 0xf701f503L, 0x1c123836L,
    0xc2a39ffeL, 0x6a5fd4e1L, 0xaef94710L, 0x69d0d26bL, 0x17912ea8L, 0x995829e8L, 0x3a277469L, 0x27b94ed0L, 0xd938a948L,
    0xeb13cd35L, 0x2bb356ceL, 0x22334455L, 0xd2bbbfd6L, 0xa9704990L, 0x07890e80L, 0x33a766f2L, 0x2db65ac1L, 0x3c227866L,
    0x15922aadL, 0xc9208960L, 0x874915dbL, 0xaaff4f1aL, 0x5078a088L, 0xa57a518eL, 0x038f068aL, 0x59f8b213L, 0x0980129bL,
    0x1a173439L, 0x65daca75L, 0xd731b553L, 0x84c61351L, 0xd0b8bbd3L, 0x82c31f5eL, 0x29b052cbL, 0x5a77b499L, 0x1e113c33L,
    0x7bcbf646L, 0xa8fc4b1fL, 0x6dd6da61L, 0x2c3a584eL,
    0xa597f4a5L, 0x84eb9784L, 0x99c7b099L, 0x8df78c8dL, 0x0de5170dL, 0xbdb7dcbdL, 0xb1a7c8b1L, 0x5439fc54L, 0x50c0f050L,
    0x03040503L, 0xa987e0a9L, 0x7dac877dL, 0x19d52b19L, 0x6271a662L, 0xe69a31e6L, 0x9ac3b59aL, 0x4505cf45L, 0x9d3ebc9dL,
    0x4009c040L, 0x87ef9287L, 0x15c53f15L, 0xeb7f26ebL, 0xc90740c9L, 0x0bed1d0bL, 0xec822fecL, 0x677da967L, 0xfdbe1cfdL,
    0xea8a25eaL, 0xbf46dabfL, 0xf7a602f7L, 0x96d3a196L, 0x5b2ded5bL, 0xc2ea5dc2L, 0x1cd9241cL, 0xae7ae9aeL, 0x6a98be6aL,
    0x5ad8ee5aL, 0x41fcc341L, 0x02f10602L, 0x4f1dd14fL, 0x5cd0e45cL, 0xf4a207f4L, 0x34b95c34L, 0x08e91808L, 0x93dfae93L,
    0x734d9573L, 0x53c4f553L, 0x3f54413fL, 0x0c10140cL, 0x5231f652L, 0x658caf65L, 0x5e21e25eL, 0x28607828L, 0xa16ef8a1L,
    0x0f14110fL, 0xb55ec4b5L, 0x091c1b09L, 0x36485a36L, 0x9b36b69bL, 0x3da5473dL, 0x26816a26L, 0x699cbb69L, 0xcdfe4ccdL,
    0x9fcfba9fL, 0x1b242d1bL, 0x9e3ab99eL, 0x74b09c74L, 0x2e68722eL, 0x2d6c772dL, 0xb2a3cdb2L, 0xee7329eeL, 0xfbb616fbL,
    0xf65301f6L, 0x4decd74dL, 0x6175a361L, 0xcefa49ceL, 0x7ba48d7bL, 0x3ea1423eL, 0x71bc9371L, 0x9726a297L, 0xf55704f5L,
    0x6869b868L, 0x00000000L, 0x2c99742cL, 0x6080a060L, 0x1fdd211fL, 0xc8f243c8L, 0xed772cedL, 0xbeb3d9beL, 0x4601ca46L,
    0xd9ce70d9L, 0x4be4dd4bL, 0xde3379deL, 0xd42b67d4L, 0xe87b23e8L, 0x4a11de4aL, 0x6b6dbd6bL, 0x2a917e2aL, 0xe59e34e5L,
    0x16c13a16L, 0xc51754c5L, 0xd72f62d7L, 0x55ccff55L, 0x9422a794L, 0xcf0f4acfL, 0x10c93010L, 0x06080a06L, 0x81e79881L,
    0xf05b0bf0L, 0x44f0cc44L, 0xba4ad5baL, 0xe3963ee3L, 0xf35f0ef3L, 0xfeba19feL, 0xc01b5bc0L, 0x8a0a858aL, 0xad7eecadL,
    0xbc42dfbcL, 0x48e0d848L, 0x04f90c04L, 0xdfc67adfL, 0xc1ee58c1L, 0x75459f75L, 0x6384a563L, 0x30405030L, 0x1ad12e1aL,
    0x0ee1120eL, 0x6d65b76dL, 0x4c19d44cL, 0x14303c14L, 0x354c5f35L, 0x2f9d712fL, 0xe16738e1L, 0xa26afda2L, 0xcc0b4fccL,
    0x395c4b39L, 0x573df957L, 0xf2aa0df2L, 0x82e39d82L, 0x47f4c947L, 0xac8befacL, 0xe76f32e7L, 0x2b647d2bL, 0x95d7a495L,
    0xa09bfba0L, 0x9832b398L, 0xd12768d1L, 0x7f5d817fL, 0x6688aa66L, 0x7ea8827eL, 0xab76e6abL, 0x83169e83L, 0xca0345caL,
    0x29957b29L, 0xd3d66ed3L, 0x3c50443cL, 0x79558b79L, 0xe2633de2L, 0x1d2c271dL, 0x76419a76L, 0x3bad4d3bL, 0x56c8fa56L,
    0x4ee8d24eL, 0x1e28221eL, 0xdb3f76dbL, 0x0a181e0aL, 0x6c90b46cL, 0xe46b37e4L, 0x5d25e75dL, 0x6e61b26eL, 0xef862aefL,
    0xa693f1a6L, 0xa872e3a8L, 0xa462f7a4L, 0x37bd5937L, 0x8bff868bL, 0x32b15632L, 0x430dc543L, 0x59dceb59L, 0xb7afc2b7L,
    0x8c028f8cL, 0x6479ac64L, 0xd2236dd2L, 0xe0923be0L, 0xb4abc7b4L, 0xfa4315faL, 0x07fd0907L, 0x25856f25L, 0xaf8feaafL,
    0x8ef3898eL, 0xe98e20e9L, 0x18202818L, 0xd5de64d5L, 0x88fb8388L, 0x6f94b16fL, 0x72b89672L, 0x24706c24L, 0xf1ae08f1L,
    0xc7e652c7L, 0x5135f351L, 0x238d6523L, 0x7c59847cL, 0x9ccbbf9cL, 0x217c6321L, 0xdd377cddL, 0xdcc27fdcL, 0x861a9186L,
    0x851e9485L, 0x90dbab90L, 0x42f8c642L, 0xc4e257c4L, 0xaa83e5aaL, 0xd83b73d8L, 0x050c0f05L, 0x01f50301L, 0x12383612L,
    0xa39ffea3L, 0x5fd4e15fL, 0xf94710f9L, 0xd0d26bd0L, 0x912ea891L, 0x5829e858L, 0x27746927L, 0xb94ed0b9L, 0x38a94838L,
    0x13cd3513L, 0xb356ceb3L, 0x33445533L, 0xbbbfd6bbL, 0x70499070L, 0x890e8089L, 0xa766f2a7L, 0xb65ac1b6L, 0x22786622L,
    0x922aad92L, 0x20896020L, 0x4915db49L, 0xff4f1affL, 0x78a08878L, 0x7a518e7aL, 0x8f068a8fL, 0xf8b213f8L, 0x80129b80L,
    0x17343917L, 0xdaca75daL, 0x31b55331L, 0xc61351c6L, 0xb8bbd3b8L, 0xc31f5ec3L, 0xb052cbb0L, 0x77b49977L, 0x113c3311L,
    0xcbf646cbL, 0xfc4b1ffcL, 0xd6da61d6L, 0x3a584e3aL,
    0x97f4a5f4L, 0xeb978497L, 0xc7b099b0L, 0xf78c8d8cL, 0xe5170d17L, 0xb7dcbddcL, 0xa7c8b1c8L, 0x39fc54fcL, 0xc0f050f0L,
    0x04050305L, 0x87e0a9e0L, 0xac877d87L, 0xd52b192bL, 0x71a662a6L, 0x9a31e631L, 0xc3b59ab5L, 0x05cf45cfL, 0x3ebc9dbcL,
    0x09c040c0L, 0xef928792L, 0xc53f153fL, 0x7f26eb26L, 0x0740c940L, 0xed1d0b1dL, 0x822fec2fL, 0x7da967a9L, 0xbe1cfd1cL,
    0x8a25ea25L, 0x46dabfdaL, 0xa602f702L, 0xd3a196a1L, 0x2ded5bedL, 0xea5dc25dL, 0xd9241c24L, 0x7ae9aee9L, 0x98be6abeL,
    0xd8ee5aeeL, 0xfcc341c3L, 0xf1060206L, 0x1dd14fd1L, 0xd0e45ce4L, 0xa207f407L, 0xb95c345cL, 0xe9180818L, 0xdfae93aeL,
    0x4d957395L, 0xc4f553f5L, 0x54413f41L, 0x10140c14L, 0x31f652f6L, 0x8caf65afL, 0x21e25ee2L, 0x60782878L, 0x6ef8a1f8L,
    0x14110f11L, 0x5ec4b5c4L, 0x1c1b091bL, 0x485a365aL, 0x36b69bb6L, 0xa5473d47L, 0x816a266aL, 0x9cbb69bbL, 0xfe4ccd4cL,
    0xcfba9fbaL, 0x242d1b2dL, 0x3ab99eb9L, 0xb09c749cL, 0x68722e72L, 0x6c772d77L, 0xa3cdb2cdL, 0x7329ee29L, 0xb616fb16L,
    0x5301f601L, 0xecd74dd7L, 0x75a361a3L, 0xfa49ce49L, 0xa48d7b8dL, 0xa1423e42L, 0xbc937193L, 0x26a297a2L, 0x5704f504L,
    0x69b868b8L, 0x00000000L, 0x99742c74L, 0x80a060a0L, 0xdd211f21L, 0xf243c843L, 0x772ced2cL, 0xb3d9bed9L, 0x01ca46caL,
    0xce70d970L, 0xe4dd4bddL, 0x3379de79L, 0x2b67d467L, 0x7b23e823L, 0x11de4adeL, 0x6dbd6bbdL, 0x917e2a7eL, 0x9e34e534L,
    0xc13a163aL, 0x1754c554L, 0x2f62d762L, 0xccff55ffL, 0x22a794a7L, 0x0f4acf4aL, 0xc9301030L, 0x080a060aL, 0xe7988198L,
    0x5b0bf00bL, 0xf0cc44ccL, 0x4ad5bad5L, 0x963ee33eL, 0x5f0ef30eL, 0xba19fe19L, 0x1b5bc05bL, 0x0a858a85L, 0x7eecadecL,
    0x42dfbcdfL, 0xe0d848d8L, 0xf90c040cL, 0xc67adf7aL, 0xee58c158L, 0x459f759fL, 0x84a563a5L, 0x40503050L, 0xd12e1a2eL,
    0xe1120e12L, 0x65b76db7L, 0x19d44cd4L, 0x303c143cL, 0x4c5f355fL, 0x9d712f71L, 0x6738e138L, 0x6afda2fdL, 0x0b4fcc4fL,
    0x5c4b394bL, 0x3df957f9L, 0xaa0df20dL, 0xe39d829dL, 0xf4c947c9L, 0x8befacefL, 0x6f32e732L, 0x647d2b7dL, 0xd7a495a4L,
    0x9bfba0fbL, 0x32b398b3L, 0x2768d168L, 0x5d817f81L, 0x88aa66aaL, 0xa8827e82L, 0x76e6abe6L, 0x169e839eL, 0x0345ca45L,
    0x957b297bL, 0xd66ed36eL, 0x50443c44L, 0x558b798bL, 0x633de23dL, 0x2c271d27L, 0x419a769aL, 0xad4d3b4dL, 0xc8fa56faL,
    0xe8d24ed2L, 0x28221e22L, 0x3f76db76L, 0x181e0a1eL, 0x90b46cb4L, 0x6b37e437L, 0x25e75de7L, 0x61b26eb2L, 0x862aef2aL,
    0x93f1a6f1L, 0x72e3a8e3L, 0x62f7a4f7L, 0xbd593759L, 0xff868b86L, 0xb1563256L, 0x0dc543c5L, 0xdceb59ebL, 0xafc2b7c2L,
    0x028f8c8fL, 0x79ac64acL, 0x236dd26dL, 0x923be03bL, 0xabc7b4c7L, 0x4315fa15L, 0xfd090709L, 0x856f256fL, 0x8feaafeaL,
    0xf3898e89L, 0x8e20e920L, 0x20281828L, 0xde64d564L, 0xfb838883L, 0x94b16fb1L, 0xb8967296L, 0x706c246cL, 0xae08f108L,
    0xe652c752L, 0x35f351f3L, 0x8d652365L, 0x59847c84L, 0xcbbf9cbfL, 0x7c632163L, 0x377cdd7cL, 0xc27fdc7fL, 0x1a918691L,
    0x1e948594L, 0xdbab90abL, 0xf8c642c6L, 0xe257c457L, 0x83e5aae5L, 0x3b73d873L, 0x0c0f050fL, 0xf5030103L, 0x38361236L,
    0x9ffea3feL, 0xd4e15fe1L, 0x4710f910L, 0xd26bd06bL, 0x2ea891a8L, 0x29e858e8L, 0x74692769L, 0x4ed0b9d0L, 0xa9483848L,
    0xcd351335L, 0x56ceb3ceL, 0x44553355L, 0xbfd6bbd6L, 0x49907090L, 0x0e808980L, 0x66f2a7f2L, 0x5ac1b6c1L, 0x78662266L,
    0x2aad92adL, 0x89602060L, 0x15db49dbL, 0x4f1aff1aL, 0xa0887888L, 0x518e7a8eL, 0x068a8f8aL, 0xb213f813L, 0x129b809bL,
    0x34391739L, 0xca75da75L, 0xb5533153L, 0x1351c651L, 0xbbd3b8d3L, 0x1f5ec35eL, 0x52cbb0cbL, 0xb4997799L, 0x3c331133L,
    0xf646cb46L, 0x4b1ffc1fL, 0xda61d661L, 0x584e3a4eL,
    0xf4a5f432L, 0x9784976fL, 0xb099b05eL, 0x8c8d8c7aL, 0x170d17e8L, 0xdcbddc0aL, 0xc8b1c816L, 0xfc54fc6dL, 0xf050f090L,
    0x05030507L, 0xe0a9e02eL, 0x877d87d1L, 0x2b192bccL, 0xa662a613L, 0x31e6317cL, 0xb59ab559L, 0xcf45cf40L, 0xbc9dbca3L,
    0xc040c049L, 0x92879268L, 0x3f153fd0L, 0x26eb2694L, 0x40c940ceL, 0x1d0b1de6L, 0x2fec2f6eL, 0xa967a91aL, 0x1cfd1c43L,
    0x25ea2560L, 0xdabfdaf9L, 0x02f70251L, 0xa196a145L, 0xed5bed76L, 0x5dc25d28L, 0x241c24c5L, 0xe9aee9d4L, 0xbe6abef2L,
    0xee5aee82L, 0xc341c3bdL, 0x060206f3L, 0xd14fd152L, 0xe45ce48cL, 0x07f40756L, 0x5c345c8dL, 0x180818e1L, 0xae93ae4cL,
    0x9573953eL, 0xf553f597L, 0x413f416bL, 0x140c141cL, 0xf652f663L, 0xaf65afe9L, 0xe25ee27fL, 0x78287848L, 0xf8a1f8cfL,
    0x110f111bL, 0xc4b5c4ebL, 0x1b091b15L, 0x5a365a7eL, 0xb69bb6adL, 0x473d4798L, 0x6a266aa7L, 0xbb69bbf5L, 0x4ccd4c33L,
    0xba9fba50L, 0x2d1b2d3fL, 0xb99eb9a4L, 0x9c749cc4L, 0x722e7246L, 0x772d7741L, 0xcdb2cd11L, 0x29ee299dL, 0x16fb164dL,
    0x01f601a5L, 0xd74dd7a1L, 0xa361a314L, 0x49ce4934L, 0x8d7b8ddfL, 0x423e429fL, 0x937193cdL, 0xa297a2b1L, 0x04f504a2L,
    0xb868b801L, 0x00000000L, 0x742c74b5L, 0xa060a0e0L, 0x211f21c2L, 0x43c8433aL, 0x2ced2c9aL, 0xd9bed90dL, 0xca46ca47L,
    0x70d97017L, 0xdd4bddafL, 0x79de79edL, 0x67d467ffL, 0x23e82393L, 0xde4ade5bL, 0xbd6bbd06L, 0x7e2a7ebbL, 0x34e5347bL,
    0x3a163ad7L, 0x54c554d2L, 0x62d762f8L, 0xff55ff99L, 0xa794a7b6L, 0x4acf4ac0L, 0x301030d9L, 0x0a060a0eL, 0x98819866L,
    0x0bf00babL, 0xcc44ccb4L, 0xd5bad5f0L, 0x3ee33e75L, 0x0ef30eacL, 0x19fe1944L, 0x5bc05bdbL, 0x858a8580L, 0xecadecd3L,
    0xdfbcdffeL, 0xd848d8a8L, 0x0c040cfdL, 0x7adf7a19L, 0x58c1582fL, 0x9f759f30L, 0xa563a5e7L, 0x50305070L, 0x2e1a2ecbL,
    0x120e12efL, 0xb76db708L, 0xd44cd455L, 0x3c143c24L, 0x5f355f79L, 0x712f71b2L, 0x38e13886L, 0xfda2fdc8L, 0x4fcc4fc7L,
    0x4b394b65L, 0xf957f96aL, 0x0df20d58L, 0x9d829d61L, 0xc947c9b3L, 0xefacef27L, 0x32e73288L, 0x7d2b7d4fL, 0xa495a442L,
    0xfba0fb3bL, 0xb398b3aaL, 0x68d168f6L, 0x817f8122L, 0xaa66aaeeL, 0x827e82d6L, 0xe6abe6ddL, 0x9e839e95L, 0x45ca45c9L,
    0x7b297bbcL, 0x6ed36e05L, 0x443c446cL, 0x8b798b2cL, 0x3de23d81L, 0x271d2731L, 0x9a769a37L, 0x4d3b4d96L, 0xfa56fa9eL,
    0xd24ed2a6L, 0x221e2236L, 0x76db76e4L, 0x1e0a1e12L, 0xb46cb4fcL, 0x37e4378fL, 0xe75de778L, 0xb26eb20fL, 0x2aef2a69L,
    0xf1a6f135L, 0xe3a8e3daL, 0xf7a4f7c6L, 0x5937598aL, 0x868b8674L, 0x56325683L, 0xc543c54eL, 0xeb59eb85L, 0xc2b7c218L,
    0x8f8c8f8eL, 0xac64ac1dL, 0x6dd26df1L, 0x3be03b72L, 0xc7b4c71fL, 0x15fa15b9L, 0x090709faL, 0x6f256fa0L, 0xeaafea20L,
    0x898e897dL, 0x20e92067L, 0x28182838L, 0x64d5640bL, 0x83888373L, 0xb16fb1fbL, 0x967296caL, 0x6c246c54L, 0x08f1085fL,
    0x52c75221L, 0xf351f364L, 0x652365aeL, 0x847c8425L, 0xbf9cbf57L, 0x6321635dL, 0x7cdd7ceaL, 0x7fdc7f1eL, 0x9186919cL,
    0x9485949bL, 0xab90ab4bL, 0xc642c6baL, 0x57c45726L, 0xe5aae529L, 0x73d873e3L, 0x0f050f09L, 0x030103f4L, 0x3612362aL,
    0xfea3fe3cL, 0xe15fe18bL, 0x10f910beL, 0x6bd06b02L, 0xa891a8bfL, 0xe858e871L, 0x69276953L, 0xd0b9d0f7L, 0x48384891L,
    0x351335deL, 0xceb3cee5L, 0x55335577L, 0xd6bbd604L, 0x90709039L, 0x80898087L, 0xf2a7f2c1L, 0xc1b6c1ecL, 0x6622665aL,
    0xad92adb8L, 0x602060a9L, 0xdb49db5cL, 0x1aff1ab0L, 0x887888d8L, 0x8e7a8e2bL, 0x8a8f8a89L, 0x13f8134aL, 0x9b809b92L,
    0x39173923L, 0x75da7510L, 0x53315384L, 0x51c651d5L, 0xd3b8d303L, 0x5ec35edcL, 0xcbb0cbe2L, 0x997799c3L, 0x3311332dL,
    0x46cb463dL, 0x1ffc1fb7L, 0x61d6610cL, 0x4e3a4e62L]
blakeS = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
          [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
          [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
          [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
          [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
          [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
          [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
          [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
          [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
          [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0],
          [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
          [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
          [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
          [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
          [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
          [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
          [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
          [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
          [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
          [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0]]

if __name__ == '__main__':
    main()

