import json


if __name__ == '__main__':
    d = {"m1": b'a'.hex(), "m2": (b'a' + b'\x1f' * 31).hex()}
    print(json.dumps(d))