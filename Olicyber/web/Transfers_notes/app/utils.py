import hashlib
import random
import json
import time
import os

Users = dict()
Ids = dict()
Path = './data/'


def padding(s: str, n: int):
    # forza il padding
    if len(s) % n == 0:
        s += ' '
        
    # aggiunge caratteri randomici finchè la lunghezza di s è diversa da un multiplo di n
    while len(s) % n != 0:
        s += random.choice('abcdefghijklnoqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    
    return s


def xor(a: bytes, b: bytes):
    n = len(b)
    
    if isinstance(a, str):
        a = a.encode()

    if isinstance(b, str):
        b = b.encode()

    return bytes([ a[i] ^ b[i%n] for i in range(len(a)) ]).hex()    # type: ignore


class UserChannel:
    def __init__(self, username: str, password: str='', hashed: bytes | None = None) -> None:
        self.__transactions = dict()

        self.username = username
        self.path = Path + username + '.json'
        
        if hashed is None:
            self.__hashed = hashlib.sha256(password.encode()).digest()
            
        elif password == '':
            self.__hashed = hashed
            
        else:
            raise ValueError('Either one of \'password\' and \'hashed\' must be empty')
        
        self.__secret = os.urandom(1)


    @property
    def transactions(self):
        return self.encode(self.__transactions)


    def check(self, password: str):
        return password is not None and hashlib.sha256(password.encode()).digest() == self.__hashed


    def encode(self, transactions: list):
        return {transaction: self.encode_transaction(transactions[transaction]) for transaction in transactions}


    def encode_transaction(self, transaction: str):
        # padding transazione
        index = transaction.index(' <- ')
        enc = padding(transaction[:index], 64) + ' <- '
        
        # padding amount
        pipe = transaction.index(' | ')
        enc += padding(transaction[index+4:pipe], 16)
        
        # padding descrizione
        enc += transaction[pipe:]
        enc = padding(enc, 128)
        
        # xor enc col segreto (1 byte)
        return xor(enc.encode(), self.__secret)


    def new_transaction(self, password: str, amount: int, receiver: str, description: str):
        if not self.check(password):
            raise ValueError("Wrong password")

        self.__transactions[str(time.time_ns())] = f"{receiver} <- {amount} | {description}"


    def read_transactions(self, password: str):
        if self.check(password):
            return self.__transactions.copy()
        else:
            return self.transactions


    def save(self):
        data = json.dumps({'transactions': self.__transactions, 'hashed': self.__hashed.hex(), 'username': self.username})
        with open(self.path, 'w') as file:
            file.write(data)


    @staticmethod
    def from_file(path):
        with open(path, 'r') as file:
            data = json.loads(file.read())
        channel = UserChannel(data['username'], hashed=bytes.fromhex(data['hashed']))
        channel.__transactions = data['transactions']
        channel.path = path
        return channel


# Restituisce tutti i file che finiscono con .json
def users():
    result = list()
    
    for name in os.listdir(Path):
        if name[-5:] == '.json':
            result.append(name[:-5])
            
    return result


def save_all():
    for user in Users:
        if user in ['Admin', 'Alice', 'Bob', 'Carl']:
            continue

        Users[user].save()


def login(username: str, password: str):
    if Users[username].check(password):
        return username, password
    else:
        return None, None


def register(username: str, password: str):
    if username in Users.keys():
        print('User already exists')
        return None, None
    Users[username] = UserChannel(username, password=password)
    Users[username].save()

    userid = os.urandom(3).hex()
    while userid in Ids.values():
        userid = os.urandom(3).hex()
    Ids[username] = userid
    print('Successfully registered')

    return username, password


def transactions(username: str, password: str):
    transactions = list()
    
    for name in Users:
        user = Users[name]
        
        if user.username == username:
            t = user.read_transactions(password)
            
        else:
            t = user.read_transactions(None)
            
        for timestamp in t:
            transactions.append((Ids[name], timestamp, t[timestamp]))
            
    transactions.sort(key=lambda e: int(e[1]))
    return transactions


for user in users():
    Users[user] = UserChannel.from_file(Path + user + '.json')
    userid = os.urandom(3).hex()
    while userid in Ids.values():
        userid = os.urandom(3).hex()
    Ids[user] = userid
