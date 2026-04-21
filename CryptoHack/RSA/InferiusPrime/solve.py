from sympy import factorint
from Crypto.Util.number import long_to_bytes


###### DATA

n = 984994081290620368062168960884976209711107645166770780785733
e = 65537
ct = 948553474947320504624302879933619818331484350431616834086273

######


if __name__ == '__main__':
    p, q = factorint(n)
    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)
    msg = pow(ct, d, n)
    msg = long_to_bytes(msg)
    
    print(msg.decode())