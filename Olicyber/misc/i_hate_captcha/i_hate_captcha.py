#!/usr/bin/python3
#script made by LunarStone292

from pwn import *
from time import sleep
from colorama import Fore

def calcoli(data):
    data = data.decode()
    if "contrario" in data:
        data = data.split(" ")
        data = data[-1:] #prende l'ultimo elemento dell'array
        data = data[0]
        return str((data[::-1]).split("\n")[1])
    if "volte" in data:
        data = data.split(" ")
        key = data[5]
        data = data[-1:]
        data = data[0]
        return str(len(data.split(key))-1)
    if "posizioni" in data:
        if len(data) > 73:
            data = data.split(",")
        #posizioni
        try:
            num1 = (int(data[0].split(" ")[-1].split("[")[1]))-1
            num2 = (int(data[1].split(" ")[1]))-1
            num3 = (int(data[2].split(" ")[1]))-1
            num4 = (int(data[-1].split("]")[0].split(" ")[1]))-1
            text = data[-1].split(" ")[-1].split("?")[0]
            final = str(text[num1] + text[num2] + text[num3] + text[num4])
            return str(final)
        except ValueError:
            try:
                num1 = (int(data[0].split(" ")[-1].split("[")[1]))-1
                num2 = (int(data[1].split(" ")[1]))-1
                num3 = (int(data[-1].split("]")[0].split(" ")[1]))-1
                text = data[-1].split(" ")[-1].split("?")[0]
                final = str(text[num1] + text[num2] + text[num3])
                return str(final)
            except ValueError:
                try:
                    num1 = (int(data[0].split(" ")[-1].split("[")[1]))-1
                    num2 = (int(data[-1].split("]")[0].split(" ")[1]))-1
                    text = data[-1].split(" ")[-1].split("?")[0]
                    final = str(text[num1] + text[num2])
                    return str(final)
                except ValueError: #se ha tanta sfiga
                    try:
                        num = (int(data.split("[")[1].split("]")[0]))-1
                        text = data.split(" ")[-1].split("?")[0]
                        return str(text[num])
                    except ValueError:
                        return ("error")

    if "risultato" in data:
        data = data.split(" ")
        num1 = data[-3]
        num2 = data[-1].split("?")[0]
        symbol = data[-2]
        if symbol == "-":
            return str(int(num1)-int(num2))
        if symbol == "/":
            return str(int(int(num1)/int(num2)))
        if symbol == "*":
            return str(int(num1)*int(num2))
        if symbol == "+":
            return str(int(num1)+int(num2))

def main():
    flag = ""
    print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + " Resolving the Captcha..." + Fore.RESET)
    conn = remote("ihc.challs.olicyber.it", 34008)
    conn.recv()
    conn.send(b'\n')
    while True:
        data = conn.recvline()
        conn.recv()
        ret = calcoli(data)
        ret += "\n"
        conn.send(str(ret).encode())
        check = str((conn.recvline()).decode())
        if "Sbagliato" in check:
            pass
        else:
            flag += check.split(":")[1]
        if "}" in flag:
            print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + "Captcha resolved, printing the flag..." + Fore.RESET)
            return flag

if __name__ == "__main__":
    out = main()
    flag = ""
    for i in range(len(out)):
        flag += out[i].split("\n")[0].split(" ")[0]
    if "flag" in flag:
        print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + "Flag: " + Fore.YELLOW + flag + Fore.RESET)
    else:
        print("[" + Fore.RED + "+" + Fore.RESET + "]" + Fore.RED + " Flag not found" + Fore.RESET)
