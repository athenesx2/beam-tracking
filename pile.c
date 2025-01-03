#include "faisceau.h"


Pile *createPile(int taille) {
    Pile *pile = (Pile *)malloc(sizeof(Pile));
    pile->data = (int *)malloc(sizeof(int) * taille);
    pile->top = -1;
    pile->taille = taille;
    return pile;
}

int isEmpty(Pile *pile) {
    return pile->top == -1;
}

void push(Pile *pile, int value) {
    if (pile->top + 1 < pile->taille) {
        pile->data[++pile->top] = value;
    }
}

int pop(Pile *pile) {
    if (!isEmpty(pile)) {
        return pile->data[pile->top--];
    }
    return -1; 
}

void freepile(Pile *pile) {
    free(pile->data);
    free(pile);
}
