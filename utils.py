from crypto_identity import Point, Curve


def is_point_on_curve(p: Point, c: Curve) -> bool:
    """
    verify that point is on the curve, i.e. y^2 = x^3 + 7 (mod p) 
        - true if (y^2 - x^3 - 7) % p == 0 
        - false if (y^2 - x^3 - 7) % p != 0 
    """
    return (p.y**2 - p.x**3 - 7) % c.p == 0

