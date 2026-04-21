#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void secret_admin(){
    const char* flag = getenv("FLAG");
    if (flag != NULL) {
        printf("%s\n", flag);
    } else {
        printf("havceCTF{dummy_fl4g}\n");
    }
}

void print_menu(){
    puts("=== Welcome to PwnMe 3000 ===");
    puts("1) Inserisci input");
    puts("2) Esci");
    printf("> ");
}

typedef struct {
    char buffer[64];
    char my_canary[8];
    int privilege;
} canary;

int main() {
    int choice;
    canary secure;

    strncpy(secure.my_canary, "CANARY!!", 8);
    secure.privilege = 0;

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    print_menu();
    scanf("%d", &choice);

    if(choice != 1){
        puts("Ciao!");
        return 0;
    }

    puts("Inserisci il tuo nome:");
    scanf("%s", secure.buffer);

    if (strncmp(secure.my_canary, "CANARY!!", 8) != 0) {
        puts("Stack smashing detected!");
        exit(1);
    }

    if (secure.privilege) {
        puts("Privilegi elevati!");
        secret_admin();
    } else {
        puts("Accesso negato.");
    }

    return 0;
}

//gcc -o chal chal.c -fno-stack-protector -no-pie -Wl,-z,norelro
