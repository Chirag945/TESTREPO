#include<stdio.h>
#include<stdlib.h>
#include <sys/time.h>
int main(){
	int n=6;
	int numbers[]={1,0,1,0,0,1};
	int l=0;
	for(int i=0;i<n;i++){
		if(numbers[i]==0){
			numbers[l]=0;
			numbers[i]=1;
			l++;
		}
	}
	for(int i=0;i<n;i++){
		printf("%d , ",numbers[i]);
	}
	printf("\n");
}