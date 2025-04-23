#include<stdio.h>
#include<stdlib.h>
#include <sys/time.h>
struct person{
int id;
char *name;
int age;
int height;
int weight;
};
int part(struct person Ls[], int lo, int hi, int pInd){
struct person t=Ls[pInd];
Ls[pInd]=Ls[lo];
Ls[lo]=t;
int pivPos, lt, rt, pv;
lt = lo + 1;
rt = hi;
pv = Ls[lo].height;
while (lt < rt)
{
for (; lt <= hi && Ls[lt].height <= pv; lt++);
// Ls[j]<=pv for j in lo..lt-1
for (; Ls[rt].height > pv; rt--);
// Ls[j]>pv for j in rt+1..hi
if (lt < rt)
{
 t=Ls[lt];
Ls[lt]=Ls[rt];
Ls[rt]=t;
lt++;
rt--;
}
}
if (Ls[lt].height < pv && lt <= hi)
pivPos = lt;
else
pivPos = lt - 1;
 t=Ls[lo];
Ls[lo]=Ls[pivPos];
Ls[pivPos]=t;
return pivPos;
}
int threePart(struct person Ls[], int lo, int hi, int pInd)
{
	struct person t;
//swap(Ls, pInd, hi - 1);
t=Ls[pInd];
Ls[pInd]=Ls[hi-1];
Ls[hi-1]=t;
int pivPos, lt, rt, mid, pv;
lt = lo;
rt = hi - 2;
mid = lo;
pv = Ls[hi - 1].height;
while (mid <= rt)
{
if (Ls[mid].height < pv)
{
//swap(Ls, lt, mid);
t=Ls[lt];
Ls[lt]=Ls[mid];
Ls[mid]=t;
lt++;
mid++;
}
else if (Ls[mid].height > pv)
{
t=Ls[rt];
Ls[rt]=Ls[mid];
Ls[mid]=t;
rt--;
}
else
{
mid++;
}
}
t=Ls[hi-1];
Ls[hi-1]=Ls[mid];
Ls[mid]=t;
return mid;
}
void partition(struct person arr[], int n) {
    struct person pivot = arr[n - 1];
    
    // i acts as boundary between smaller and 
    // larger element compared to pivot
    int i = -1;
    for (int j = 0; j < n; j++) {
        
        // If smaller element is found expand the 
        // boundary and swapping it with boundary element.
        if (arr[j].height < pivot.height) {
            i++;
            struct person temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    
    // place the pivot at its correct position
    struct person temp = arr[i + 1];
    arr[i + 1] = arr[n - 1];
    arr[n - 1] = temp;
}
int main(){
	int n=1000;
	char* fname="dat1000.csv";
	FILE *fp = fopen(fname, "r");
    struct person numbers1[n];
    struct person numbers2[n];
    struct person numbers3[n];
    int i = 0;
    struct person temp;
    int id,age,height,weight;
    char name[100];
    while (fscanf(fp, "%d,%99[^,],%d,%d,%d", &id, name, &age, &height, &weight) != EOF){	
    	temp.id=id;
    	temp.name=name;
    	temp.age=age;
    	temp.height=height;
    	temp.weight=weight;
    	numbers1[i]=temp;
    	numbers2[i]=temp;
    	numbers3[i]=temp;
        i++;
    }
    fclose(fp);
    struct timeval t1, t2;
    double time_taken;
    gettimeofday(&t1, NULL);
    part(numbers1,0,999,500);
    gettimeofday(&t2, NULL);
    time_taken = (t2.tv_sec - t1.tv_sec) * 1e6;
    time_taken = (time_taken + (t2.tv_usec - t1.tv_usec)) * 1e-6;
    printf("2 way partition take %f seconds\n",time_taken);
    struct timeval t3, t4;
 
    gettimeofday(&t3, NULL);
    threePart(numbers2,0,999,500);
    gettimeofday(&t4, NULL);
    time_taken = (t4.tv_sec - t3.tv_sec) * 1e6;
    time_taken = (time_taken + (t4.tv_usec - t3.tv_usec)) * 1e-6;
    printf("3 way partition take %f seconds\n",time_taken);
    struct timeval t5, t6;
  
    gettimeofday(&t5, NULL);
    partition(numbers3,999);
    gettimeofday(&t6, NULL);
    time_taken = (t6.tv_sec - t5.tv_sec) * 1e6;
    time_taken = (time_taken + (t6.tv_usec - t5.tv_usec)) * 1e-6;
    printf("Lumou partition take %f seconds",time_taken);
}

