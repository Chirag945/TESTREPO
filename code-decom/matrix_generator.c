#include <stdio.h>
#include <sys/time.h>
#include<stdlib.h>
void rowAdder(int m1[500][500], int m2[500][500], int n){
    int m3[n][n];
    for (int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            m3[i][j] = m2[i][j] + m1[i][j];
         }
   }
   //printArr(m3);
}
void colAdder(int m1[][500], int m2[500][500], int n){
    int m3[n][n];
    for (int j=0; j<n; j++){
        for(int i=0; i<n; i++){
            m3[i][j] = m2[i][j] + m1[i][j];
         }
   }
   //printArr(m3);
}
int main(){
    int n=500;
    //printf("Enter n: ");
    //scanf("%d", &n);
    int m1[n][n];
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            m1[i][j] = rand() % 100;
        }
    }
    int m2[n][n];
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            m2[i][j] = rand() % 100;
        }
    }
    struct timeval t1, t2,t3,t4,t5,t6;
    double time_taken;
    gettimeofday(&t1, NULL);
    rowAdder(m1,m2,n);
    gettimeofday(&t2, NULL);
    time_taken = (t2.tv_sec - t1.tv_sec) * 1e6;
    time_taken = (time_taken + (t2.tv_usec - t1.tv_usec)) * 1e-6;
    printf("Row adder took %f seconds to execute\n",time_taken);
    gettimeofday(&t3, NULL);
    colAdder(m1,m2,n);
    gettimeofday(&t4, NULL);
    time_taken = (t4.tv_sec - t3.tv_sec) * 1e6;
    time_taken = (time_taken + (t4.tv_usec - t3.tv_usec)) * 1e-6;
    printf("Col adder took %f seconds to execute\n", time_taken);
    return 0;
}