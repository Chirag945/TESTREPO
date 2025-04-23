#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
int factNTR(int n) {
if (n == 0)
{
return 1;
}
else
{
return n * factNTR(n - 1);
}
}
int factTR(int n, int acc) {
if (n == 0)
{
return acc;
}
else
{
return factTR(n - 1, n * acc);
}}

int factI(int n)
{
int acc = 1;
while (n > 0)
{
acc = acc * n;
n = n - 1;
}
return acc;
}

int main(){
	int n=9000;
	struct timeval t1, t2,t3,t4,t5,t6;
    double time_taken;
    gettimeofday(&t1, NULL);
	printf("Non tail recursive answer - %d\n",factNTR(n));
	gettimeofday(&t2, NULL);
    time_taken = (t2.tv_sec - t1.tv_sec) * 1e6;
    time_taken = (time_taken + (t2.tv_usec - t1.tv_usec)) * 1e-6;
    printf("Non tail Recursive took %f seconds to execute\n",time_taken);
    gettimeofday(&t3, NULL);
	printf("Tail recrusive answer - %d\n", factTR(n,1));
	gettimeofday(&t4, NULL);
    time_taken = (t4.tv_sec - t3.tv_sec) * 1e6;
    time_taken = (time_taken + (t4.tv_usec - t3.tv_usec)) * 1e-6;
    printf("Tail Recursive took %f seconds to execute\n", time_taken);
	gettimeofday(&t5, NULL);
	printf("Iterative answer - %d\n", factI(n));
	gettimeofday(&t6, NULL);
    time_taken = (t6.tv_sec - t5.tv_sec) * 1e6;
    time_taken = (time_taken + (t6.tv_usec - t5.tv_usec)) * 1e-6;
    printf("Iterative took %f seconds to execute\n", time_taken);
}
