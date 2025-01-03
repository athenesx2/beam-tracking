#include "faisceau.h"

int *dfs(Set **graphe, int sommet, Set *visite,int nb_sommets) {
    Pile *pile = createPile(nb_sommets);
    push(pile, sommet);
    int *composantes=(int *)malloc((nb_sommets+1)*sizeof(int));
    int nb_composantes=0;
    while (!isEmpty(pile))
    {   
        int s = pop(pile);
        if (inset(visite,s)==0)
        {
            add(visite,s);
            composantes[nb_composantes+1]=s;
            nb_composantes=nb_composantes+1;
            for (int k = 0; k < graphe[s]->quantitax+1; k++)
            {   int voisin =graphe[s]->key[k];
                if(inset(visite,voisin)==0){
                    push(pile,voisin);
                }
            }
            
        }
        
    }
    composantes[0]=nb_composantes;
    freepile(pile);
    return composantes;
}

int **composantes_connexes(Set **graphe, int nb_sommets) {
    Set *visite=createSet(nb_sommets);
    int nbcomposantes=0;
    int **sousgraphes=(int **)malloc((nb_sommets+1)*sizeof(int *));
    for (int sommet = 1; sommet < nb_sommets+1; sommet++)
    {if (inset(visite,sommet)==0)
    {
        int *composantes=dfs(graphe,sommet,visite,nb_sommets);
        sousgraphes[nbcomposantes+1]=composantes;
        nbcomposantes=nbcomposantes+1;
    }
    }
    sousgraphes[0]=(int *)malloc(sizeof(int));
    sousgraphes[0][0]=nbcomposantes;
    
    
    freeset(visite);
    return sousgraphes;
}
