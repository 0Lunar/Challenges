encrypted = bytes.fromhex("64909297d7d9d4dbe1db9b686594cfa5ace7ad6da7db9bacd8c498a5e7ece5cdbe9267a2cd96a9a3a1dee1ead6d3a4608fd4dddbe7a864a9dfdadc9b")
l = len(encrypted)


for k in range(3, len(encrypted), 2):
    dec = []
    
    for i in [( k * i - 1 ) % l for i in range(l, -1, -1)]:
        dec.append((encrypted[i] + encrypted[( i + k ) % l]) & 0xff)
    
    print(bytes(dec))