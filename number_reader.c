#include <stdio.h>
#include <sys/time.h>

void insertionSortR(int *arr, int n)
{
{
int last = arr[i];
int j = i-1;
while (j >= 0 && arr[j] > last)
{
arr[j+1] = arr[j];
j--;
}
arr[j+1] = last;
}
}
int helper(char* fname,int n)
{
    // Reads the numbers stored in numbers1000.txt and stores them into an integer array
    FILE *fp = fopen(fname, "r");
    int numbers[n];
    int i = 0;
    while (fscanf(fp, "%d", &numbers[i]) != EOF)
    {
        i++;
    }
    fclose(fp);
    struct timeval t1, t2;
    double time_taken;
    gettimeofday(&t1, NULL);
    insertionSortR(numbers,n);
    gettimeofday(&t2, NULL);
    time_taken = (t2.tv_sec - t1.tv_sec) * 1e6;
    time_taken = (time_taken + (t2.tv_usec - t1.tv_usec)) * 1e-6;
    printf("Recursive sorting of %d numbers took %f seconds to execute\n",n, time_taken);
        int dup[n];
    for(int i=0;i<n;i++){
        dup[i]=numbers[i];
    }

    gettimeofday(&t1, NULL);
    insertionSortI(dup,n);
    gettimeofday(&t2, NULL);
    time_taken = (t2.tv_sec - t1.tv_sec) * 1e6;
    time_taken = (time_taken + (t2.tv_usec - t1.tv_usec)) * 1e-6;
    printf("Iterative sorting  of %d numbers took %f seconds to execute\n",n, time_taken);
    

}
int main(){
    helper("numbers10000.txt",10000);
    helper("numbers100000.txt",100000);
    //("numbers500000.txt",500000);
    return 0;
}
