"""
an identity is (private, public) keypair. 
bitcoin uses "elliptic curve cryptography" instead of something more common like rsa.
more specifically, bitcoin uses the secp256k1 curve
"""


from __future__ import annotations
from dataclasses import dataclass 


@dataclass
class Curve:
    """
    Elliptic Curve over the field of integers modulo a prime.
    Points on the curve satisfy y^2 = x^3 + a*x + b (mod p).
    """
    p: int # the prime modulus of the finite field
    a: int
    b: int


# generator point: 
# fixed starting point to kick off the “random walk” around the curve
@dataclass
class Point:
    """ An integer point (x,y) on a Curve """
    curve: Curve
    x: int
    y: int


@dataclass
class Generator:
    """
    A generator over a curve: an initial point and the (pre-computed) order
    """
    G: Point     # a generator point on the curve
    n: int       # the order of the generating point, so 0*G = n*G = INF


# secp256k1 uses a = 0, b = 7, so we're dealing with the curve y^2 = x^3 + 7 (mod p)
bitcoin_curve = Curve(p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
                      a = 0x0000000000000000000000000000000000000000000000000000000000000000,  # a = 0
                      b = 0x0000000000000000000000000000000000000000000000000000000000000007,) # b = 7

G = Point(bitcoin_curve,
          x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
          y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,)

bitcoin_gen = Generator(G = G,
                        # the order of G is known and can be mathematically derived
                        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,)


if __name__ == '__main__':
    import utils


    # we can verify that the generator point is indeed on the curve, i.e. y^2 = x^3 + 7 (mod p)
    print("Generator is on the curve: ", utils.is_point_on_curve(G, bitcoin_curve))

    # random point 
    import random
    random.seed(111)
    rnd_point = Point(x=random.randrange(0, bitcoin_curve.p),
                      y=random.randrange(0, bitcoin_curve.p),
                      curve=None)

    print("random point on the curve: ", utils.is_point_on_curve(rnd_point, bitcoin_curve))