#include <stdio.h>
#include <stdlib.h>

int main(){
    while(1){
    int* ptr;
    ptr = (int *)malloc(52428800 * sizeof(int));
    delay(10000);                        
    free(ptr);
    
    }
}