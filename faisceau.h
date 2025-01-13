#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int top;
    int taille;
} Pile;

typedef struct {
    int *data;
    int max;
    int *key;
    int quantitax;
} Set;


Set *createSet(int);

void add(Set *,int);
int inset(Set *set, int value);
void freeset(Set *);

Pile *createPile(int);


int isEmpty(Pile *);

void push(Pile *, int);

int pop(Pile *);

void freepile(Pile *);

int *dfs(Set **graphe, int sommet, Set *visite, int nb_sommets);

int **composantes_connexes(Set **graphe, int nb_sommets);
