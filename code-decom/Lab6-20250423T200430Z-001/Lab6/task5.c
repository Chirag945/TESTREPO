#include<stdio.h>
#include<stdlib.h>
#include <sys/time.h>
void insertionSort(int arr[], int lo,int hi)
{
    for (int i = lo; i < hi; ++i) {
        int key = arr[i];
        int j = i - 1;

        /* Move elements of arr[0..i-1], that are
           greater than key, to one position ahead
           of their current position */
        while (j >= lo && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
int part(int Ls[], int lo, int hi, int pInd){
	int t=Ls[pInd];
	Ls[pInd]=Ls[lo];
	Ls[lo]=t;
	int pivPos, lt, rt, pv;
	lt = lo + 1;
	rt = hi;
	pv = Ls[lo];
	while (lt < rt){
		for (; lt <= hi && Ls[lt] <= pv; lt++);
		for (; Ls[rt] > pv; rt--);
		if (lt < rt){
			t=Ls[lt];
			Ls[lt]=Ls[rt];
			Ls[rt]=t;
			lt++;
			rt--;
		}
	}
	if (Ls[lt] < pv && lt <= hi)
	pivPos = lt;
	else pivPos = lt - 1;
	t=Ls[lo];
	Ls[lo]=Ls[pivPos];
	Ls[pivPos]=t;
	return pivPos;
}


int Sselect(int L[], int n, int k){
	if (k == 0) return L[0];
	if (n <= 5){
		for (int i = 1; i < n; i++)
		for (int j = i-1; j >= 0; j--)
		if (L[j] > L[j+1]){
			int t=L[j];
			L[j]=L[j+1];
			L[j+1]=t;
		}
		else break;
		return L[k-1];
	}
	int numGroups;
	if (n % 5 == 0)	numGroups = n/5;
	else numGroups = n/5 + 1;
	int medians[numGroups];
	for (int i = 0; i < numGroups; i++)	{
		int l,h;
		if(5<(n-(5*i))) l=5;
		else l=n-(5*i);
		if(5<(n-(5*i))) h=5;
		else h=n-(5*i);
		h/=2;
		medians[i] = Sselect(L + (i*5),l,h);
	}
	int M = Sselect(medians, numGroups, (numGroups+1)/2);
	int mInd;
	for (int i = 0; i < n; i++){
		if (L[i] == M){
			mInd = i;
			break;
		}
	}
	int pInd = part(L, 0, n-1, mInd);
	if (k <= pInd) return Sselect(L, pInd, k);
	else if (k > pInd + 1) return Sselect(L + pInd + 1, n - pInd - 1, k - pInd - 1);
	else return L[pInd];
}
void qsort_hybrid(int Ls[], int lo, int hi){
	if (hi - lo < 10){
		insertionSort(Ls, lo, hi);
		return;
	}
	else if (lo < hi){
		int p = Sselect(Ls, lo, hi);
		p = part(Ls, lo, hi, p);
		qsort_hybrid(Ls, lo, p - 1);
		qsort_hybrid(Ls, p + 1, hi);
	}
}
void hqsort(int Ls[],int lo,int hi){
	if (hi - lo < 10){
		return;
	}
	else if (lo < hi){
		int p = Sselect(Ls, lo, hi);
		p = part(Ls, lo, hi, p);
		qsort_hybrid(Ls, lo, p - 1);
		qsort_hybrid(Ls, p + 1, hi);
	}
}
void hybrid_qsort(int Ls[],int lo,int hi){
	hqsort(Ls,lo,hi);
	insertionSort(Ls,lo,hi);
}
void helper(int numbers[],char* fname,int n){
	FILE *fp = fopen(fname, "r");
    if (fp == NULL) {
        printf("Error opening file %s\n", fname);
        return;
    }

    int i = 0;
    while (i < n && fscanf(fp, "%d", &numbers[i]) != EOF) {
        i++;
    }
    fclose(fp);

    printf("********** Sorting %s file now***********\n", fname);

    struct timeval t1, t2;
    double time_taken;
    gettimeofday(&t1, NULL);
    qsort_hybrid(numbers, 0, n - 1);
    gettimeofday(&t2, NULL);
    time_taken = (t2.tv_sec - t1.tv_sec) * 1e6;
    time_taken = (time_taken + (t2.tv_usec - t1.tv_usec)) * 1e-6;
    printf("qsort_hybrid partition take %f seconds\n", time_taken);

    struct timeval t3, t4;
    gettimeofday(&t3, NULL);
    hybrid_qsort(numbers, 0, n - 1);
    gettimeofday(&t4, NULL);
    time_taken = (t4.tv_sec - t3.tv_sec) * 1e6;
    time_taken = (time_taken + (t4.tv_usec - t3.tv_usec)) * 1e-6;
    printf("hybrid_qsort partition take %f seconds\n", time_taken);
}
int main(){
	int numbers[1000];
	//helper(numbers,"int1.txt",1000);
	helper(numbers,"int2.txt",999);
	// helper(numbers,"int3.txt",50);
	// helper(numbers,"int4.txt",1000);
	//helper("int5.txt",1000000);
}