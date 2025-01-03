from PIL import Image, ImageFile


def exporte():
    with open("données.txt", "r") as f:
        données = f.readlines()
        dates = []
        noms = []
        barycentres = []
        contours = []
        chemin = []
        n = 5
        for k in range((len(données) - 1) // n):
            dates.append(
                tuple(int(date) for date in données[n * k + 1][:-1].split("/"))
            )
            noms.append(données[n * k + 2][:-1])
            contours.append(
                [
                    tuple(int(coord) for coord in chaine.split(","))
                    for chaine in données[n * k + 4][:-1].split("|")[1:]
                ]
            )
            chemin.append(données[n * k + 5][:-1])
            barycentres.append(
                [
                    tuple(int(coord) for coord in chaine.split(","))
                    for chaine in données[n * k + 3][:-1].split("|")[1:]
                ]
            )

        return dates, noms, barycentres, contours, chemin


def importable(nom):
    with open("données.txt", "r") as f:
        données = f.readlines()
        
        n = 5
        for k in range((len(données) - 1) // n):
            if nom == données[n * k + 2][:-1]:
                return False
        return True


def importe(
    date: tuple[int, int, int],
    nom: str,
    barycentres: list[tuple],
    contour: list[tuple],
    chemin: str,
    image: ImageFile,
):
    with open("données.txt", "r") as f:
        données = f.read()
    with open("données.txt", "w") as f:
        inscrit = données + f"{date[0]}/{date[1]}/{date[2]}" + "\n" + nom + "\n"
        for couple in barycentres:
            inscrit += f"|{couple[0]},{couple[1]}"
        inscrit += "\n"
        for couple in contour:
            inscrit += f"|{couple[0]},{couple[1]}"
        inscrit += "\n"
        inscrit += f"{chemin}\n"
        f.write(inscrit)
        print(f"{chemin}/{nom}.png")
        image.save(f"{chemin}/{nom}.png")


def supprime(nom):
    with open("données.txt", "r") as f:
        données = f.readlines()
        n = 5
        for k in range((len(données) - 1) // n):
            if nom == données[n * k + 2][:-1]:
                données.pop(n * k + 5)
                données.pop(n * k + 4)
                données.pop(n * k + 3)
                données.pop(n * k + 2)
                données.pop(n * k + 1)
                break
    with open("données.txt", "w") as f:
        f.writelines(données)
