encrypted_flag = "f{anuiraaso_lfltnfi_sin_aime_rotpze_gne_ca_roi}_"


def decrpyt(data):
    n = 4
    cols = [data[i:i + (len(data) // 4)] for i in range(0, len(data), (len(data) // 4))]
    res = ''

    for x in range(len(cols[0])):
        for i in range(n):
            res += cols[i][x]
    
    return ''.join(res).rstrip('_')


if __name__ == '__main__':
    flag = decrpyt(encrypted_flag)
    print(flag)