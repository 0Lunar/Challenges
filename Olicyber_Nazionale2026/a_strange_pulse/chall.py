#!/usr/bin/env python3
import time
import subprocess
import numpy as np
import sys
import os

TARGET = "10.10.0.1"
N = 10

A = 1337
B = 0xFFFF
C = 100
D = 150
E = 200
F = 250


def v1(s, i):
    a = (s ^ (i * A)) & B
    b = [C, D, E, F]
    np.random.seed(a)
    np.random.shuffle(b)
    return b


def ping(host):
    subprocess.run(
        ["ping", "-c", "1", "-W", "1", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def run(data, s):
    assert data[:5] == "flag{"
    ping(TARGET)
    for idx, c in enumerate(data):
        lvls = v1(s, idx)
        v = ord(c)
        for k in range(4):
            chunk = (v >> (6 - 2 * k)) & 0x3
            base = lvls[chunk]
            for _ in range(N):
                d = (base + np.random.normal(0, 15)) / 1000.0
                time.sleep(max(d, 0.01))
                ping(TARGET)


SEED = os.urandom(2)
run(sys.argv[1], SEED[0] << 8 | SEED[1])
