#include "faisceau.h"

typedef struct {
    int r, g, b;
} Pixel;
typedef struct {
    long int x,y,m;
} Barycentre;

int voisin(int x, int y,int **matrice,int **matricecouleur, int multitrack,int *couleurs, int *couleurcount,Set **dicoclr) {
    
    if (matrice[x][y]==0){

        return 0;
    }
    int **ssmatrice = NULL;
    int taillessmatrice = 0;
    ssmatrice=(int **)malloc(3*sizeof(int *));
    for (size_t i = 0; i < 3; i++)
    {
        ssmatrice[i]=(int *)malloc(2*sizeof(int));
    }
    if (x!=0 && y !=0){
        taillessmatrice=3;
        ssmatrice[0][0]=x-1;
        ssmatrice[0][1]=y-1;
        ssmatrice[1][0]=x;
        ssmatrice[1][1]=y-1;
        ssmatrice[2][0]=x-1;
        ssmatrice[2][1]=y;
        }
    else if (x==0 && y !=0)
    {taillessmatrice=1;
    ssmatrice[0][0]=x;
    ssmatrice[0][1]=y-1;
    ssmatrice[1][0]=0;
    ssmatrice[1][1]=0;
    ssmatrice[2][0]=0;
    ssmatrice[2][1]=0;
    }
    else if (x!=0 && y ==0)
    {taillessmatrice=1;
    ssmatrice[0][0]=x-1;
    ssmatrice[0][1]=y;
    ssmatrice[1][0]=0;
    ssmatrice[1][1]=0;
    ssmatrice[2][0]=0;
    ssmatrice[2][1]=0;}
    else
    {
    taillessmatrice=0;
    ssmatrice[0][0]=0;
    ssmatrice[0][1]=0;
    ssmatrice[1][0]=0;
    ssmatrice[1][1]=0;
    ssmatrice[2][0]=0;
    ssmatrice[2][1]=0;}
    int retour = 0;
    int *archretour =(int *)malloc(taillessmatrice*sizeof(int));
    int archretourtaille=0;
    if (multitrack==1)
    {   
        for (int k = 0; k < taillessmatrice; k++)
        {   
            if (matrice[ssmatrice[k][0]][ssmatrice[k][1]]==matrice[x][y])
            {   for (int i = 0; i < archretourtaille; i++)
            {if (i<archretourtaille)
            {int checkbar=archretour[i];
                if(checkbar!=matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]) {
                    add(dicoclr[checkbar],matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]);
                    add(dicoclr[matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]],checkbar);
                }
            }
            }
            retour=matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]];
            archretour[archretourtaille]=retour;
            archretourtaille=archretourtaille+1;
            
                // if(retour !=0 && retour != matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]){
                //     add(dicoclr[retour],matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]);
                //     add(dicoclr[matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]],retour);
                // }
                
                // retour = matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]];
            }
            
        }
    } else
    {
        for (int k = 0; k < taillessmatrice; k++)
        {   
            if (matrice[ssmatrice[k][0]][ssmatrice[k][1]]!=0)
            {
                if(retour !=0 && retour != matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]){
                    add(dicoclr[retour],matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]);
                    add(dicoclr[matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]]],retour);
                }
                
                retour = matricecouleur[ssmatrice[k][0]][ssmatrice[k][1]];
            }
            
        }
        
    }
    if (retour==0)
    {
        retour=couleurs[*couleurcount]+1;
        *couleurcount=*couleurcount+1;
        couleurs[*couleurcount]=retour;
        dicoclr[retour]=createSet(50);
    }
    
    for (int i = 0; i < 3; i++)
    {
    free(ssmatrice[i]);
    }
    free(ssmatrice);
    free(archretour);
    ssmatrice=NULL;
    return retour;}

Barycentre *detecte_faisceau(int maxou,int l,int L,Pixel **image,int multitrack,int seuille,int nuit ){

    int *clr=(int *)malloc(l*L*sizeof(int));
    clr[0]=0;
    Set **dicoclr=(Set **)malloc(l*L*sizeof(Set *));
    int **matrice=(int **)malloc(l*sizeof(int *));
    int **couleur=(int **)malloc(l*sizeof(int *));
    int clrcount=0;

    for (int i = 0; i < l; i++)
    {
        matrice[i]=(int *)malloc(L*sizeof(int));
        couleur[i]=(int *)malloc(L*sizeof(int));
        for (int j = 0; j < L; j++)
    {   matrice[i][j]=0;
        int R=image[i][j].r;
        int G=image[i][j].g;
        int B=image[i][j].b;
        if (R*nuit<maxou*nuit)
            {if (G*nuit<maxou*nuit)
                {if (B*nuit< maxou*nuit)
                    {matrice[i][j]=111;
                    }
                else
                    {matrice[i][j]=110;
                    }
                }
            else
                {if (B*nuit< maxou*nuit)
                    {matrice[i][j]=101;
                    }
                else
                    {matrice[i][j]=100;
                    }
                }
            }
        else
            {if (G*nuit<maxou*nuit)
                {if (B*nuit< maxou*nuit)
                    {matrice[i][j]=11;
                    }
                else
                    {matrice[i][j]=10;
                    }
                }
            else
                {if (B*nuit< maxou*nuit)
                    {matrice[i][j]=1;
                    }
                else
                    {matrice[i][j]=0;
                    }
                }
            } 
            
        couleur[i][j] =voisin(i,j,matrice,couleur,multitrack,clr,&clrcount,dicoclr);
    }}


    int **prime=composantes_connexes(dicoclr,clrcount);
    for (int i = 1; i < clrcount+1; i++)
    {
        freeset(dicoclr[i]);
    }
    
    free(clr);
    clr=NULL;
    free(dicoclr);
    dicoclr=NULL;
    for (int i = 0; i < l; i++)
    {free(matrice[i]);
        }
    free(matrice);
    matrice=NULL;
    matrice=NULL;
    Barycentre *barycentre=(Barycentre *)malloc((prime[0][0]+1)*sizeof(Barycentre));
    int *masse=(int *)malloc((prime[0][0])*sizeof(int));
    int *count=(int *)malloc((prime[0][0])*sizeof(int));
    int *dicof=(int *)malloc((clrcount+1)*sizeof(int ));
    for (int k = 1; k < prime[0][0]+1; k++)
    {   barycentre[k].x=0;
        barycentre[k].y=0;
        barycentre[k].m=0;
        masse[k-1]=0;
        count[k-1]=0;
        for(int l=1;l<prime[k][0]+1;l++){
            int key=prime[k][l];
            dicof[key]=k;
        }
        free(prime[k]);
    }
    

    for (int n = 0; n < l; n++)
    {for (int m = 0; m < L; m++)
    {int localcolor=0;

        if (couleur[n][m]!=0)
        {
        localcolor=dicof[couleur[n][m]];
        
        barycentre[localcolor].x=barycentre[localcolor].x+n*(image[n][m].r+image[n][m].g+image[n][m].b);
        barycentre[localcolor].y=barycentre[localcolor].y+m*(image[n][m].r+image[n][m].g+image[n][m].b);
        masse[localcolor-1]=masse[localcolor-1]+(image[n][m].r+image[n][m].g+image[n][m].b);
        count[localcolor-1]=count[localcolor-1]+1;
        
        }
        
        
        }
        
        free(couleur[n]);
    }

    free(couleur);
    free(dicof);
    dicof=NULL;
    couleur=NULL;

    for (int k = 1; k < prime[0][0]+1; k++)
    {if(masse[k-1]!=0){
        barycentre[k].x=barycentre[k].x/masse[k-1];
        barycentre[k].y=barycentre[k].y/masse[k-1];
        barycentre[k].m=masse[k-1];
    }
    if(count[k-1]<seuille){
        barycentre[k].x=2143;
    }
    }
    barycentre[0].x=prime[0][0];
    barycentre[0].y=143;
    barycentre[0].m=3812155;
    free(masse);
    free(count);
    masse=NULL;
    free(prime[0]);
    free(prime);
    prime=NULL;
    return barycentre;
}

int **voisindirect(int x, int y,int l, int L) {
    int **ssmatrice=malloc(4*sizeof(int *));
        ssmatrice[0]=malloc(2*sizeof(int));
        ssmatrice[1]=malloc(2*sizeof(int));
        ssmatrice[2]=malloc(2*sizeof(int));
        ssmatrice[3]=malloc(2*sizeof(int));
    if (x!=0 && y !=0 && x!=l-1 && y !=L-1){
        ssmatrice[0][0]=x-1;
        ssmatrice[1][0]=x+1;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=y-1;
        ssmatrice[3][1]=y+1;
        }
    else if (x==0 && y !=0 && y !=L-1){
        ssmatrice[0][0]=2143;
        ssmatrice[1][0]=x+1;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=y-1;
        ssmatrice[3][1]=y+1;
    }
    else if (x==l-1 && y !=0 && y !=L-1)
    {
        ssmatrice[0][0]=x-1;
        ssmatrice[1][0]=2143;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=y-1;
        ssmatrice[3][1]=y+1;
    }
    else if (x!=0 && x!=l-1 && y==0)
    {
        ssmatrice[0][0]=x-1;
        ssmatrice[1][0]=x+1;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=2143;
        ssmatrice[3][1]=y+1;
    }
    else if (x!=0 && x!=l-1 && y==L-1)
    {
        ssmatrice[0][0]=x-1;
        ssmatrice[1][0]=x+1;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=y-1;
        ssmatrice[3][1]=2143;
    }
    else if (x==0 && y==0)
    {
        ssmatrice[0][0]=2143;
        ssmatrice[1][0]=x+1;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=2143;
        ssmatrice[3][1]=y+1;
    }
    else if (x==0 && y==L-1)
    {
        ssmatrice[0][0]=2143;
        ssmatrice[1][0]=x+1;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=y-1;
        ssmatrice[3][1]=2143;
    }
    else if (x==l-1 && y==0)
    {
        ssmatrice[0][0]=x-1;
        ssmatrice[1][0]=2143;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=2143;
        ssmatrice[3][1]=y+1;
    }
    else if (x==l-1 && y==L-1)
    {
        ssmatrice[0][0]=x-1;
        ssmatrice[1][0]=2143;
        ssmatrice[2][0]=x;
        ssmatrice[3][0]=x;
        ssmatrice[0][1]=y;
        ssmatrice[1][1]=y;
        ssmatrice[2][1]=y-1;
        ssmatrice[3][1]=2143;
    }

return ssmatrice;
}

int ***contour(int maxou,int l,int L,Pixel **image,int multitrack,int seuille, int nuit ){

    int *clr=(int *)malloc(l*L*sizeof(int));
    clr[0]=0;
    Set **dicoclr=(Set **)malloc(l*L*sizeof(Set *));
    int **matrice=(int **)malloc(l*sizeof(int *));
    int **couleur=(int **)malloc(l*sizeof(int *));
    int clrcount=0;

    for (int i = 0; i < l; i++)
    {
        matrice[i]=(int *)malloc(L*sizeof(int));
        couleur[i]=(int *)malloc(L*sizeof(int));
        for (int j = 0; j < L; j++)
    {   matrice[i][j]=0;
        int R=image[i][j].r;
        int G=image[i][j].g;
        int B=image[i][j].b;
        if (R*nuit<maxou*nuit)
            {if (G*nuit<maxou*nuit)
                {if (B*nuit< maxou*nuit)
                    {matrice[i][j]=111;
                    }
                else
                    {matrice[i][j]=110;
                    }
                }
            else
                {if (B*nuit< maxou*nuit)
                    {matrice[i][j]=101;
                    }
                else
                    {matrice[i][j]=100;
                    }
                }
            }
        else
            {if (G*nuit<maxou*nuit)
                {if (B*nuit< maxou*nuit)
                    {matrice[i][j]=11;
                    }
                else
                    {matrice[i][j]=10;
                    }
                }
            else
                {if (B*nuit< maxou*nuit)
                    {matrice[i][j]=1;
                    }
                else
                    {matrice[i][j]=0;
                    }
                }
            } 
            
        couleur[i][j] =voisin(i,j,matrice,couleur,multitrack,clr,&clrcount,dicoclr);
    }}


    int **prime=composantes_connexes(dicoclr,clrcount);
    for (int i = 1; i < clrcount+1; i++)
    {
        freeset(dicoclr[i]);
    }
    
    free(clr);
    clr=NULL;
    free(dicoclr);
    dicoclr=NULL;
    for (int i = 0; i < l; i++)
    {free(matrice[i]);
        }
    free(matrice);
    matrice=NULL;
    matrice=NULL;
    Barycentre *barycentre=(Barycentre *)malloc((prime[0][0]+1)*sizeof(Barycentre));
    int *masse=(int *)malloc((prime[0][0])*sizeof(int));
    int *count=(int *)malloc((prime[0][0])*sizeof(int));
    int *dicof=(int *)malloc((clrcount+1)*sizeof(int ));
    int ***contour=(int ***)malloc((prime[0][0]+1)*sizeof(int **));
    for (int k = 1; k < prime[0][0]+1; k++)
    {   barycentre[k].x=0;
        contour[k]=(int**)malloc((l*L+1)*sizeof(int*));
        contour[k][0]=(int*)malloc(sizeof(int));
        contour[k][0][0]=0;
        barycentre[k].y=0;
        barycentre[k].m=0;
        masse[k-1]=0;
        count[k-1]=0;
        for(int l=1;l<prime[k][0]+1;l++){
            int key=prime[k][l];
            dicof[key]=k;
        }
        free(prime[k]);
        prime[k]=NULL;
    }
    
    contour[0]=(int**)malloc(sizeof(int*));
    contour[0][0]=(int*)malloc(sizeof(int));
    contour[0][0][0]=prime[0][0];
    for (int n = 0; n < l; n++)
        {for (int m = 0; m < L; m++)
            {int localcolor=0;
            if (couleur[n][m]!=0)
                {
                localcolor=dicof[couleur[n][m]];
                
                int **voisinnm=voisindirect(n,m,l,L);
                for (int i = 0; i < 4; i++)
                    {
                    if (voisinnm[i][0]!=2143&&voisinnm[i][1]!=2143){
                        if(couleur[voisinnm[i][0]][voisinnm[i][1]]==0){
                            contour[localcolor][0][0]=contour[localcolor][0][0]+1;
                            contour[localcolor][contour[localcolor][0][0]]=(int *)malloc(2*sizeof(int));
                            contour[localcolor][contour[localcolor][0][0]][0]=n;
                            contour[localcolor][contour[localcolor][0][0]][1]=m;
                        }
                        else if(
                            
                            dicof[couleur[voisinnm[i][0]][voisinnm[i][1]]] !=localcolor){
                            contour[localcolor][0][0]=contour[localcolor][0][0]+1;
                            contour[localcolor][contour[localcolor][0][0]]=(int *)malloc(2*sizeof(int));
                            contour[localcolor][contour[localcolor][0][0]][0]=n;
                            contour[localcolor][contour[localcolor][0][0]][1]=m;
                        }

                    }
                    free(voisinnm[i]);
                    voisinnm[i]=NULL;
                }

                free(voisinnm);
                voisinnm=NULL;
                barycentre[localcolor].x=barycentre[localcolor].x+n*(image[n][m].r+image[n][m].g+image[n][m].b);
                barycentre[localcolor].y=barycentre[localcolor].y+m*(image[n][m].r+image[n][m].g+image[n][m].b);
                masse[localcolor-1]=masse[localcolor-1]+(image[n][m].r+image[n][m].g+image[n][m].b);
                count[localcolor-1]=count[localcolor-1]+1;
                
                }
            }
        
        }
    
    
    for (int n = 0; n < l; n++)
    {free(couleur[n]);
    couleur[n]=NULL;
    }
    
    free(couleur);
    couleur=NULL;
    free(dicof);
    dicof=NULL;
    couleur=NULL;

    for (int k = 1; k < prime[0][0]+1; k++)
    {if(masse[k-1]!=0){
        barycentre[k].x=barycentre[k].x/masse[k-1];
        barycentre[k].y=barycentre[k].y/masse[k-1];
        barycentre[k].m=masse[k-1];
    }
    if(count[k-1]<seuille){
        barycentre[k].x=2143;
        contour[k][0][0]=0;
    }
    }

    barycentre[0].x=prime[0][0];
    barycentre[0].y=143;
    barycentre[0].m=3812155;
    free(masse);
    free(count);
    masse=NULL;
    free(prime[0]);
    free(prime);
    prime=NULL;
    free(barycentre);

    return contour;
}


