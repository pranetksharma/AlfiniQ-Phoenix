from tinyec.ec import SubGroup, Curve

# Domain parameters for the `secp256k1` curve
# (as defined in http://www.secg.org/sec2-v2.pdf)

"""
name: The name of the elliptic curve.
p: The prime modulus of the finite field.
n: The order of the base point (g).
a, b: The coefficients of the elliptic curve equation y^2 = x^3 + ax + b.
g: The base point on the elliptic curve.
h: The cofactor of the curve.
"""

name = 'ATTTCATACGATATACGTATCGACGTACGTGACG'

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
a = 0x0000000000000000000000000000000000000000000000000000000000000000
b = 0x0000000000000000000000000000000000000000000000000000000000000007
g = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
     0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
h = 1

curve = Curve(a, b, SubGroup(p, g, n, h), name)

"""
curve: An instance of the Curve class representing the elliptic curve
       with the specified domain parameters.
"""

print('curve:', curve)

"""
privKey: A hexadecimal string representing the private key.
"""

privKey = int('0x51897b64e85c3f714bba707e867914295a1377a7463a9dae8ea6a8b914246319', 16)
print('privKey:', hex(privKey)[2:])

"""
pubKey: The public key derived from the private key using
        the elliptic curve point multiplication (scalar multiplication).
        The public key is represented in compressed form,
        which is a 33-byte string starting with 0x02 or 0x03,
        followed by the x-coordinate of the point.
"""

pubKey = curve.g * privKey
pubKeyCompressed = '0' + str(2 + pubKey.y % 2) + str(hex(pubKey.x)[2:])
print('pubKey:', pubKeyCompressed)
