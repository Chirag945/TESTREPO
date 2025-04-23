#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct node * NODE;
struct node{
    int ele;
    NODE next;
};


typedef struct linked_list * LIST;
struct linked_list{
    int count;
    NODE head;
};


LIST createNewList()
{
    LIST myList;
    myList = (LIST) malloc(sizeof(struct linked_list));
    myList->count=0;
    myList->head=NULL;
    return myList;
}


NODE createNewNode(int value)
{
    NODE myNode;
    myNode = (NODE) malloc(sizeof(struct node));
    myNode->ele=value;
    myNode->next=NULL;
    return myNode;
}

// Recursive function to compute sum of integers in a linked list
int llSumNTR(NODE head)
{
    if (head == NULL)
        return 0;
    return head->ele + llSumNTR(head->next); // Pay close attention here
}

// This is just a wrapper function to take LIST as input, but run the recursive sum function on its NODEs starting from the head
int llSumNTRWrapper(LIST list)
{
    return llSumNTR(list->head);
}
int llSumTR(NODE head, int acc){
    if (head == NULL)
        return 0;
    return llSumTR(head->next,head->ele+acc); // Pay close attention here
}
int llSumTRWrapper(LIST list){
    return llSumTR(list->head,0);
}
int llSumIt(NODE head){
    int sum=0;
    while(head!=NULL){
        sum+=head->ele;
        head=head->next;
    }
    return sum;
}
// Driver code
int main()
{
    // Reads the file numbers1000.txt and creates a linked list with those integers
    FILE *fp;
    fp = fopen("numbers1000.txt", "r");
    if (fp == NULL)
    {
        printf("Error opening file\n");
        exit(1);
    }
    int num;
    LIST myList = createNewList();
    while (fscanf(fp, "%d", &num) != EOF)
    {
        NODE myNode = createNewNode(num);
        myNode->next = myList->head;
        myList->head = myNode;
        myList->count++;
    }
    fclose(fp);

    struct timeval t1, t2,t3,t4,t5,t6;
    double time_taken;
    gettimeofday(&t1, NULL);
    printf("Non tail recursive answer - %d\n",llSumNTRWrapper(myList));
    gettimeofday(&t2, NULL);
    time_taken = (t2.tv_sec - t1.tv_sec) * 1e6;
    time_taken = (time_taken + (t2.tv_usec - t1.tv_usec)) * 1e-6;
    printf("Non tail Recursive took %f seconds to execute\n",time_taken);
    gettimeofday(&t3, NULL);
    printf("Tail recrusive answer - %d\n", llSumTRWrapper(myList));
    gettimeofday(&t4, NULL);
    time_taken = (t4.tv_sec - t3.tv_sec) * 1e6;
    time_taken = (time_taken + (t4.tv_usec - t3.tv_usec)) * 1e-6;
    printf("Tail Recursive took %f seconds to execute\n", time_taken);
    gettimeofday(&t5, NULL);
    printf("Iterative answer - %d\n", llSumIt(myList->head));
    gettimeofday(&t6, NULL);
    time_taken = (t6.tv_sec - t5.tv_sec) * 1e6;
    time_taken = (time_taken + (t6.tv_usec - t5.tv_usec)) * 1e-6;
    printf("Iterative took %f seconds to execute\n", time_taken);

    
}