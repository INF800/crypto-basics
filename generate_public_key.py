from crypto_identity import Point


INF = Point(None, None, None) # special point at "infinity", kind of like a zero

def extended_euclidean_algorithm(a, b):
    """
    Returns (gcd, x, y) s.t. a * x + b * y == gcd
    This function implements the extended Euclidean
    algorithm and runs in O(log b) in the worst case,
    taken from Wikipedia.
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t

def inv(n, p):
    """ returns modular multiplicate inverse m s.t. (n * m) % p == 1 """
    gcd, x, y = extended_euclidean_algorithm(n, p) # pylint: disable=unused-variable
    return x % p

def elliptic_curve_addition(self, other: Point) -> Point:
    # handle special case of P + 0 = 0 + P = 0
    if self == INF:
        return other
    if other == INF:
        return self
    # handle special case of P + (-P) = 0
    if self.x == other.x and self.y != other.y:
        return INF
    # compute the "slope"
    if self.x == other.x: # (self.y = other.y is guaranteed too per above check)
        m = (3 * self.x**2 + self.curve.a) * inv(2 * self.y, self.curve.p)
    else:
        m = (self.y - other.y) * inv(self.x - other.x, self.curve.p)
    # compute the new point
    rx = (m**2 - self.x - other.x) % self.curve.p
    ry = (-(m*(rx - self.x) + self.y)) % self.curve.p
    return Point(self.curve, rx, ry)


# monkey patch addition into the Point class
Point.__add__ = elliptic_curve_addition 


"""
the public key is the point on the curve that results from adding the generator point to itself secret_key times
i.e pub_key = G + G + G + ... (secret_key times)

Note:
- The secret key is an integer, but the generator point G is an (x,y) tuple that is a Point on the Curve, resulting in an (x,y) tuple public key
- So, define the Addition operator on an elliptic curve. It has a very specific definition and a geometric interpretation
"""


if __name__ == '__main__':
    from crypto_identity import G
    import utils

    # if secret key = 1, then our public key would be G:
    pvt = 2
    pub = G

    print(f'pvt: {pvt}\npub: ({str(pub.x)[:20]}, {str(pub.y)[:20]})')
    
    #! ALWAYS PRINTING TRUE ...
    print('match:', utils.is_point_on_curve(pub, pub.curve))
