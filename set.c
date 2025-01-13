#include "faisceau.h"


Set *createSet(int taille) {
    Set *set = (Set *)malloc(sizeof(Set));
    set->data = (int *)malloc(sizeof(int) * taille);
    set->max = taille;
    set->quantitax =0;
    set->key =  (int *)malloc(sizeof(int) * taille);
    for (int i = 0; i < taille; i++)
    {
       set->data[i]=0;
       set->key[i]=0;
    }
    
    return set;
}

int inset(Set *set, int value){
    for (int i = 0; i < set->quantitax+1; i++)
    {if (set->key[i]==value)
        {
            return 1;
        }
    }
     
        
    return 0;
    
}

void add(Set *set, int value) {

    if (set->max  > value) {
        if(set->data[value]==0){
            set->data[value] = value;
            set->key[set->quantitax]=value;
            set->quantitax=set->quantitax+1;}


    }
    else{
        set->data=realloc(set->data,(value+1)*sizeof(int));
        set->key=realloc(set->key,(value+1)*sizeof(int));
    for (int i = set->max; i < value+1; i++)
    {
       set->data[i]=0;
       set->key[i]=0;
    }

        set->key[set->quantitax]=value;
        set->quantitax=set->quantitax+1;
        set->data[value] = value;
        set->max=value+1;
    }
}


void freeset(Set *set) {
    free(set->data);
    free(set->key);
    free(set);
}
