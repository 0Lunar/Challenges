import OpenSSL
from pwn import *
import json


SECRET_KEY = b"G_ab!bb_oR_oss_o"


def generate_cert(emailAddress="gabibbo@olicyber",
                    commonName="1337.olicyber",
                    countryName="IT",
                    localityName="ILO",
                    stateOrProvinceName="Piemonte",
                    organizationName="Olicyber",
                    organizationUnitName="repartoGabibbi",
                    serialNumber=0,
                    validityStartInSeconds=0,
                    validityEndInSeconds=10*365*24*60*60,
                    KEY_FILE = "private.key",
                    CERT_FILE="selfsigned.crt"):
    k = OpenSSL.crypto.PKey()
    k.generate_key(OpenSSL.crypto.TYPE_RSA, 4096)
    cert = OpenSSL.crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert).decode("utf-8")
    

if __name__ == "__main__":
    with open("codes.json", "rt") as f:
        data = json.load(f)

    conn = remote("snecc.challs.olicyber.it", 12310)
    code = conn.recvline().strip().decode()
    
    while code not in data:
        conn.close()
        conn = remote("snecc.challs.olicyber.it", 12310)
        code = int(conn.recvline().strip().decode())
    
    conn.sendline(str(data[code]).encode())
    conn.sendlineafter(b'> ', b'2')
    encrypted = bytes.fromhex(conn.recvline().strip().decode())
    encrypted = xor(encrypted, SECRET_KEY).decode()
    
    cert = generate_cert()
    encCert = xor(cert, SECRET_KEY).hex()
    
    conn.sendline(encCert.encode())
    data = bytes.fromhex(conn.recvline().strip().decode()[2:])
    data = xor(data, SECRET_KEY).decode()
    
    print(data)
    
    conn.interactive()
    conn.close()