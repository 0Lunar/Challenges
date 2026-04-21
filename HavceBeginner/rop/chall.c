#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

char secret;

void unlock_navigation(int key) {
    if ((0x41 ^ (uintptr_t)&secret ^ key) == 0x41) {

        puts("[ACCESS GRANTED] Navigation codes:");
        printf("%s\n", getenv("FLAG"));

        return;
    }

    puts("[ACCESS DENIED] Invalid access sequence.");
}

void gadget_collection() {
    __asm__ volatile (
        "pop %rdi; ret;"
    );
}

void intro() {
    puts("       ✦      .       *        ✦       .      *       ✦");
    puts("   .        ✦       *        .       ✦        *      .");
    puts("        ✦        /^\\       *       ✦        .");
    puts("        *       /___\\       .        ✦       *");
    puts("   .     ✦     |=   =|        ASTRA-7 Autonomous Console v3.4       *");
    puts("    ✦          |     |      *        .       ✦");
    puts("         *     |     |    ✦       *       .");
    puts("           .   |     |        .       ✦      *");
    puts("      *       /|##!##|\\      ✦       .       *");
    puts("    ✦        / |##!##| \\   *       ✦       .");
    puts("            /  |##!##|  \\       .       *       ✦");
    puts("      *    |  / ^ | ^ \\  |    ✦       *       .");
    puts("           | /  ( | )  \\ |       .        ✦      *");
    puts("   ✦       |/   ( | )   \\|    *       .       ✦");
    puts("     ✦         ((   ))        ✦       *       .");
    puts("    ✦      ✦  ((  :  ))     *        .      ✦");
    puts("        ✦     ((  :  ))        ✦       *");
    puts("               ((   ))     *        .       ✦");
    puts("       *        (( ))        ✦       *       .");
    puts("                 ( )      *        .       ✦");
    puts("         .           *       ✦       .       *");
    puts(">> Input command:");
}

int main() {

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    char buffer[32];
    intro();
    scanf("%s", buffer);   // Still vulnerable (no bounds check on return)

    puts("Command processed.");
    return 0;
}

//gcc -Wall -Wextra -fno-stack-protector -no-pie chall.c -Wl,-u,execve -o chall
