#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char byte;

int encode(byte *buffer, byte *key, int fileSize, int keyLen) {
    for (int i = 0; i < fileSize; i++) {
        buffer[i] = buffer[i] ^ key[i % keyLen];
    }
}

void readKey(byte *key, int keyLen) {
    FILE *fd = fopen("key.bin", "rb");
    if (fd == NULL) {
        perror("Failed to open file");
        exit(1);
    }
    
    fread(key, 1, keyLen, fd);
    fclose(fd);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s [input_file] [output_file]", argv[0]);
        return 1;
    }

    // read key from file 
    int keyLen = 128;

    byte *key = malloc(keyLen * sizeof(byte));
    readKey(key, keyLen);

    FILE *fd = fopen(argv[1], "rb");
    if (fd == NULL) {
        perror("Failed to open file");
        return 1;
    }

    // calc the len of the file
    fseek(fd, 0, SEEK_END);
    long fileSize = ftell(fd);
    rewind(fd);  
    
    // read all the file content
    byte *buffer = malloc(fileSize * sizeof(byte));
    if (buffer == NULL) {
        perror("Memory allocation failed");
        fclose(fd);
        return 1;
    }
    fread(buffer, 1, fileSize, fd);
    fclose(fd);

    // encode the content
    encode(buffer, key, fileSize, keyLen);

    // write the result
    FILE *fw = fopen(argv[2], "wb");
    fwrite(buffer, 1, fileSize, fw);
    fclose(fd);

    return 0;   
}