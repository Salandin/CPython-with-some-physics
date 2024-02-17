#include <stdio.h>

void writingAFile(char text[]) {
    FILE *fp;

    // Open the file for writing
    fp = fopen("texto.txt", "a+");
    
    fprintf(fp, text);
    // Close the file
    fclose(fp);
    return 0;
};

void readingAFile(){
    FILE *fp;
    char ch;

    fp = fopen("texto.txt", "r");

    while ((ch = fgetc(fp)) != EOF) {
        printf("%c", ch);
    }

    fclose(fp);
};