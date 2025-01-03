import ctypes
from PIL import Image, ImageFile
import time

###########################################
# ce fichier permet de comuniquer avec les fonctions codé en C
###########################################


lib = ctypes.CDLL("./a.so")


class Pixel(ctypes.Structure):
    _fields_ = [
        ("r", ctypes.c_int),  # Composante rouge
        ("g", ctypes.c_int),  # Composante verte
        ("b", ctypes.c_int),  # Composante bleue
    ]


class Barycentre(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),  # Coordonnée x
        ("y", ctypes.c_long),  # Coordonnée y
        ("m", ctypes.c_long),  # Coordonnée m
    ]


lib.detecte_faisceau.argtypes = [
    ctypes.c_int,  # max
    ctypes.c_int,  # largeur
    ctypes.c_int,  # hauteur
    ctypes.POINTER(ctypes.POINTER(Pixel)),  # matrice des pixels
    ctypes.c_int,  # multitrack
    ctypes.c_int,  # seuil
    ctypes.c_int,  # nuit
]
lib.detecte_faisceau.restype = ctypes.POINTER(Barycentre)

lib.contour.argtypes = [
    ctypes.c_int,  # max
    ctypes.c_int,  # largeur
    ctypes.c_int,  # hauteur
    ctypes.POINTER(ctypes.POINTER(Pixel)),  # matrice des pixels
    ctypes.c_int,  # multitrack
    ctypes.c_int,  # seuil
    ctypes.c_int,  # nuit
]

lib.contour.restype = ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_int)))



def image_to_matrix(image: ImageFile):
    image.save("test.jpeg")
    image = Image.open("test.jpeg").convert("RGB")
    l, L = image.size
    matrice = (ctypes.POINTER(Pixel) * l)()
    pixels = list(image.getdata())
    
    for y in range(l):
        row = (Pixel * L)()
        for x in range(L):
            r, g, b = pixels[x*l+y]
            row[x] = Pixel(r, g, b)
        matrice[y] = ctypes.cast(row, ctypes.POINTER(Pixel))
    
    return matrice, l, L


def detecte_faisceau_c(max, image, multitrack=0, seuil=100, contour=0, nuit=1):
    
    matrice, largeur, hauteur = image_to_matrix(image)

    if contour == 0:
        val = []
    else:
        val = C_contour(max, matrice, largeur, hauteur, multitrack, seuil, nuit)

    
    return (C_barycentre(max, matrice, largeur, hauteur, multitrack, seuil, nuit), val)


def C_barycentre(max, matrice, l, L, multitrack=0, seuil=100, nuit=1):
    barycentres = lib.detecte_faisceau(max, l, L, matrice, multitrack, seuil, nuit)
    barycentres_list = []
    for i in range(barycentres[0].x):
        b = barycentres[i + 1]
        barycentres_list.append((b.x, b.y, b.m))
    t3 = time.time()
    return barycentres_list


def C_contour(max, matrice, l, L, multitrack=0, seuil=100, nuit=1):
    contour_liste = lib.contour(max, l, L, matrice, multitrack, seuil, nuit)
    contourlist = []
    for i in range(contour_liste[0][0][0]):
        for j in range(contour_liste[i + 1][0][0]):
            contourlist.append(
                (contour_liste[i + 1][j + 1][0], contour_liste[i + 1][j + 1][1])
            )

    return contourlist
