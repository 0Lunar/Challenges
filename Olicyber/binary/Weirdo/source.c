#include <stdio.h>
#include <stdlib.h>
#include <string.h>



const char *the_username = {
    0xe5, 0xfd, 0x8d, 0x2c,
    0xd9, 0x02, 0x6b, 0xc6,
    0xe6, 0xce, 0x89, 0x2d,
    0xc4, 0x42, 0x39, 0xd6,
    0xf0, 0xce, 0x8b, 0x7b,
    0xcc, 0x14, 0x05, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x83, 0x91, 0xec, 0x4b,
    0xa2, 0x71, 0x5a, 0xa2,
    0x17, 0x00, 0x00, 0x00
};



const char *the_password = {
    0x5d, 0xfe, 0xe6, 0xa1,
    0x41, 0x57, 0x4d, 0x6c,
    0x47, 0xc7, 0xb1, 0x9f,
    0x86, 0x28, 0x53, 0x6e,
    0x16, 0xcb, 0xdf, 0x6e,
    0x51, 0x5d, 0x99, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0xe6, 0x95, 0x7a, 0x3d,
    0x20, 0xf8, 0x1c, 0x3b,
    0x17, 0x00, 0x00, 0x00
};



size_t weirdo_strlen(char *input);
int weirdo_strcmp(char *src, char *dst);
int weirdo_memcpy(char *__dest, char *__src, size_t __sz);
int weirdo_memcmp(char *src, char *dst, size_t sz);



int main(int argc, char **argv) {
    char username[44];
    char password[44];
    size_t var_len;
    int cmp;


    if ( argc < 3 ) {
        puts("nop :(");
    }
    else {
        memset(username, 0, 40);
        *(int *)( username + 40 ) = 0x7B;
        
        var_len = weirdo_strlen(argv[1]);
        *(int *)( username + 40 ) = weirdo_memcpy(username, argv[1], var_len);

        memset(password, 0, 40);
        *(int *)( password + 40 ) = 0x7B;

        var_len = weirdo_strlen(argv[2]);
        *(int *)( password + 40 ) = weirdo_memcpy(password, argv[2], var_len);

        if (weirdo_strcmp(username, the_username) == 0 && weirdo_memcmp(password, the_password, 0) == 0) {
            puts("ggwp :)");
        }
        else {
            puts("nop :(");
        }
    }

    return 0;
}


size_t weirdo_strlen(char *input) {
    int cnt;
    
    for ( cnt = 0; input[cnt] != 0; cnt++ )
        input[cnt] ^= 2;

    return (size_t)cnt;
}


int weirdo_strcmp(char *src, char *dst) {
    int res;
    int cnt;

    if ( *(int *)( src + 40 ) == *(int *)( dst + 40 ) ) {
        for ( cnt = 0; cnt < *(int *)( src + 40 ); cnt++ ) {
            res |= (unsigned char)(dst[cnt] ^ src[cnt] ^ dst[(cnt % 8) + 32]);
        }
    }
}


int weirdo_memcpy(char *__dest, char *__src, size_t __sz) {
    int sz;
    char *dest;
    char *src;
    
    sz = __sz;
    dest = __dest;
    src = __src;

    while ( ( sz < 32 && ( sz != 0 ) ) ) {
        *dest = *src ^ 64;

        sz--;
        dest++;
        src++;
    }

    return __sz;
}

//password, the_password
int weirdo_memcmp(char *src, char *dst, size_t sz) {
    int return_value;
    char val;
    int cnt;
  
    val = 0;
    if ( *(int *)( src + 40 ) == *(int *)( dst + 40 ) ) {
        for ( cnt = 0; cnt < *(int *)( src + 40 ); cnt++ ) {
            val |= dst[(cnt % 8) + 32] + src[cnt] ^ dst[cnt];
        }
        
        return_value = val;
    }
    else {
        return_value = 1;
    }
    return return_value;
}