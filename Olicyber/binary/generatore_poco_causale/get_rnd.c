#include <stdio.h>
#include <stdlib.h>


int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <seed> <index>", argv[0]);
        return -1;
    }

    if (atol(argv[1]) < 0 || atol(argv[2]) < 0) {
        fprintf(stderr, "Usage: %s <seed> <index>", argv[0]);
        return -1;
    }

    srand((unsigned int)atol(argv[1]));

    for (size_t cnt = 0; cnt < (unsigned long)atol(argv[2]); cnt++) {
        rand();
    }

    printf("%u", rand());
}