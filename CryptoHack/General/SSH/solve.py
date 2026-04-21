from Crypto.PublicKey import RSA


if __name__ == '__main__':
    with open('bruce_rsa.pub', 'rt') as f:
        id_rsa_pub = f.read().strip()
        
    key = RSA.import_key(id_rsa_pub)
    print(key.n)