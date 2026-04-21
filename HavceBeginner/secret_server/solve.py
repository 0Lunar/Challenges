from pwn import xor
from pytesseract import image_to_string


if __name__ == '__main__':
    with open("flag.enc", "rb") as f:
        xored_flag = f.read()

    with open("key.bin", "rb") as f:
        key = f.read()

    flag = xor(xored_flag, key)

    with open("flag.jpeg", "wb") as f:
        f.write(flag)

    flag = image_to_string("flag.jpeg")
    print(flag)