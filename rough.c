#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHUNK_SIZE 100  // max elements in RAM per chunk
#define MAX_RUNS 100    // max temporary runs created

// Utility: Compare function for qsort
int compare(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

// Step 1: Split input file into sorted runs
int createSortedRuns(const char *inputFile) {
    FILE *in = fopen(inputFile, "r");
    if (!in) {
        perror("Error opening input file");
        exit(EXIT_FAILURE);
    }

    int buffer[CHUNK_SIZE];
    int runCount = 0;

    while (!feof(in)) {
        int count = 0;
        while (count < CHUNK_SIZE && fscanf(in, "%d", &buffer[count]) == 1) {
            count++;
        }

        if (count == 0) break;  // nothing more to read

        qsort(buffer, count, sizeof(int), compare);

        char filename[20];
        sprintf(filename, "run%d.txt", runCount);
        FILE *out = fopen(filename, "w");
        for (int i = 0; i < count; i++) {
            fprintf(out, "%d\n", buffer[i]);
        }
        fclose(out);
        runCount++;
    }

    fclose(in);
    return runCount;
}

// Merge two sorted files into one
void mergeFiles(const char *file1, const char *file2, const char *outputFile) {
    FILE *f1 = fopen(file1, "r");
    FILE *f2 = fopen(file2, "r");
    FILE *out = fopen(outputFile, "w");

    int a, b;
    int hasA = fscanf(f1, "%d", &a);
    int hasB = fscanf(f2, "%d", &b);

    while (hasA == 1 && hasB == 1) {
        if (a <= b) {
            fprintf(out, "%d\n", a);
            hasA = fscanf(f1, "%d", &a);
        } else {
            fprintf(out, "%d\n", b);
            hasB = fscanf(f2, "%d", &b);
        }
    }

    while (hasA == 1) {
        fprintf(out, "%d\n", a);
        hasA = fscanf(f1, "%d", &a);
    }

    while (hasB == 1) {
        fprintf(out, "%d\n", b);
        hasB = fscanf(f2, "%d", &b);
    }

    fclose(f1);
    fclose(f2);
    fclose(out);
}

// Step 2 & 3: Keep merging runs until one final sorted file
void mergeAllRuns(int runCount) {
    int currentRuns = runCount;
    int pass = 0;

    while (currentRuns > 1) {
        int newRun = 0;
        for (int i = 0; i < currentRuns; i += 2) {
            char file1[20], file2[20], outFile[20];
            sprintf(file1, "run%d.txt", i);
            sprintf(outFile, "run%d.txt", newRun);

            if (i + 1 < currentRuns) {
                sprintf(file2, "run%d.txt", i + 1);
                mergeFiles(file1, file2, outFile);
                remove(file1);
                remove(file2);
            } else {
                // Odd run out, move as-is
                rename(file1, outFile);
            }
            newRun++;
        }
        currentRuns = newRun;
        pass++;
    }

    // Final sorted file will be run0.txt
    rename("run0.txt", "sorted_output.txt");
}

int main() {
    const char *inputFile = "input.txt";

    printf("Creating sorted runs...\n");
    int runCount = createSortedRuns(inputFile);

    printf("Merging %d runs...\n", runCount);
    mergeAllRuns(runCount);

    printf("Sorting complete. Output in 'sorted_output.txt'\n");
    return 0;
}
