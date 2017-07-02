#include <stdio.h>
#include <stdlib.h>
#include "/Users/huhai/Desktop/segmenter_hai/foma/OSX/include/fomalib.h"

// read in a text file in command line
// Hai Hu, adapted from Lwin's code

int main(int argc, char *argv[]) {
    if (argc <= 2) {
        printf("Usage: segment foo.foma textfilename\n");
        exit(1);
    }

    struct fsm *net;
    struct apply_handle *ah;
    char *result;

    char *filename = argv[1];

    net = fsm_read_binary_file(filename);
    if (net == NULL) {
        perror("Error loading file");
        exit(EXIT_FAILURE);
    }
    ah = apply_init(net);
    printf("FST name  : %s\n", argv[1]);
    printf("segmenting: %s ...\n", argv[2]);
    
    // output file 
    FILE *outfile = fopen("output.txt", "w");

    // read in text
    FILE *infile = fopen(argv[2], "r");
    char buf[10000];
    if (!infile){
        printf("Error reading textfile");
    }

    while (fgets(buf, 10000, infile) != NULL){
        //printf("%s", buf);
        result = apply_down(ah, buf);
        while (result != NULL) {
            // print segmented sent and write to output.txt
            //printf("%s\n", result);
            fprintf(outfile, "%s", result); // was: fprintf(outfile, "%s\n", result);
            result = apply_down(ah, NULL);
        }
    }

    apply_clear(ah);
    fsm_destroy(net);

    fclose(infile);
    fclose(outfile);
    printf("done!\nsegmented file is saved in output.txt\n");
    
    /*
    char *str = argv[2];
    result = apply_down(ah, str);
    while (result != NULL) {
        printf("%s\n", result);
        result = apply_down(ah, NULL);
    }
    apply_clear(ah);
    fsm_destroy(net);
    */
}
