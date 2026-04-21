flag = "fcnpf}l3_odda_tse8g4r4d3{g4n_80n1s5f"
rows = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]]


cnt = 0

for i in range(len(rows)):
    for j in range(len(rows)):
        rows[j][(i+j) % len(rows[0])] = flag[cnt]
        cnt += 1

out = ''

for row in rows:
    out += ''.join(row)
    
print(out)