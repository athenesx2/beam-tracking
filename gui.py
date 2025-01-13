import datetime
import signal
from tkinter import filedialog, ttk
import traceback

from numpy import sqrt
from sauvegarde import *
from sousframe import *
import tkinter as tk
from PIL import Image, ImageTk
from interface import *
from communication import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# whoo whoo (°v°)

# pyinstaller -add-data "/home/eytan/Bureau/python L1/stage/logo.png:." --add-data "/home/eytan/Bureau/python L1/stage/save2.png:." --add-data "/home/eytan/Bureau/python L1/stage/parametre.png:." --add-data "/home/eytan/Bureau/python L1/stage/excel-type.xlsx:." --add-data "/home/eytan/Bureau/python L1/stage/simulmc.bmp:." --add-data "/home/eytan/Bureau/python L1/stage/simulmc2.bmp:."  polypheme.py --hidden-import='PIL._tkinter_finder'
# pyinstaller --noconfirm --add-data "données.txt:." --add-data "memoire.txt:." --add-data "test1.png:." --add-binary "a.so:." --windowed gui.py --hidden-import='PIL._tkinter_finder'


class app(tk.Tk):

    def __init__(self):
        super().__init__()

        t1 = time.time()
        self.taille = self.winfo_screenheight()  # 1200
        self.geometry(f"{self.taille//3*4}x{self.taille//4*3}")  # 1600x900
        frame1, frame2, frame3 = (
            tk.Frame(self, background="royalblue1", width=self.taille // 3 * 4),
            tk.Frame(self, background="royalblue1", width=self.taille // 3 * 4),
            tk.Frame(self, background="royalblue1", width=self.taille // 3 * 4),
        )
        bar = tk.Canvas(
            self,
            bg="black",
            highlightthickness=0,
            height=4,
            width=self.winfo_screenwidth(),
        )
        a = tk.Canvas(
            frame1,
            background="royalblue1",
            height=self.taille // 30,
            width=self.taille // 30,
            highlightthickness=0,
        )
        a.grid(row=1, column=6)
        a.create_line(
            self.taille // 60, 0, self.taille // 60, self.taille // 24, width=4
        )
        a = tk.Canvas(
            frame3,
            background="royalblue1",
            height=self.taille // 30,
            width=self.taille // 30,
            highlightthickness=0,
        )
        a.grid(row=1, column=6)
        a.create_line(
            self.taille // 60, 0, self.taille // 60, self.taille // 24, width=4
        )
        a = tk.Canvas(
            frame3,
            background="royalblue1",
            height=self.taille // 30,
            width=self.taille // 30,
            highlightthickness=0,
        )
        a.grid(row=1, column=10)
        a.create_line(
            self.taille // 60, 0, self.taille // 60, self.taille // 24, width=4
        )
        self.canvaco = tk.Canvas(
            frame1,
            background="royalblue1",
            height=self.taille // 30,
            width=self.taille // 30,
            highlightthickness=0,
        )
        self.co = self.canvaco.create_oval(
            4, 4, self.taille // 30 - 4, self.taille // 30 - 4, width=4, fill="red"
        )

        def raiseexception(signum, frame):
            raise Exception

        signal.signal(signal.SIGALRM, raiseexception)
        signal.setitimer(signal.ITIMER_REAL, 0.1)

        try:
            update_image()
            self.canvaco.itemconfig(self.co, fill="light green")
        except Exception as e:
            serveur_co = 0
            print(type(e).__name__)

            traceback.print_exc()
            # ou
            print(traceback.format_exc())
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
        self.columnconfigure(0, weight=1)
        frame1.grid(row=0, column=0, sticky="ew")
        frame2.grid(row=1, column=0, sticky="ew")
        frame3.grid(row=2, column=0, sticky="ew")
        bar.grid(row=3, column=0)
        self.configure(background="sky blue")
        self.title("beam track")
        self.onoff = 0
        self.sauvegarde = tk.Button(
            frame3,
            text="sauvegarder des données",
            background="dark turquoise",
            activebackground="turquoise",
            command=self.save,
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.compare = tk.Button(
            frame3,
            text="comparer d'ancien résultat",
            background="dark turquoise",
            command=self.comparing,
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.listecomparaisonimage = {}
        self.acq = tk.Button(
            frame3,
            text="acquisition automatique",
            background="dark turquoise",
            activebackground="turquoise",
            command=self.automatical,
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.scan = tk.Button(
            frame3,
            text="scan faisceau",
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            command=self.scaning,
            font=f"helvetica {self.taille // 60} bold",
        )
        self.accesserveur = tk.Button(
            frame1,
            text="diagnostique serveur",
            command=self.demarre,
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.parametreserveur = tk.Button(
            frame1,
            text="parametre RP5",
            background="dark turquoise",
            command=self.parametre,
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.redemarrer = tk.Button(
            frame1,
            text="redemarrer l'appareil",
            command=lambda: [reboot(), self.canvaco.itemconfig(self.co, fill="red")],
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.eteindre = tk.Button(
            frame1,
            text="eteindre l'appareil",
            command=lambda: [shutdown(), self.canvaco.itemconfig(self.co, fill="red")],
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.barycentredico = {}
        self.contourdico = {}
        self.videobutton = tk.Button(
            frame1,
            text="video",
            command=self.streaming,
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.photobutton = tk.Button(
            frame1,
            text="photo",
            command=self.photoing,
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.analysebutton = tk.Button(
            frame2,
            text="detection de faisceau",
            command=lambda: [self.analyse(self.cbdata.get(), self.cbdata.get())],
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.multitrack = tk.IntVar()
        self.multitrackcb = tk.Checkbutton(
            frame2,
            onvalue=1,
            offvalue=0,
            variable=self.multitrack,
            text="multifaisceau",
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.nocturne = tk.IntVar()
        self.nocturnecb = tk.Checkbutton(
            frame2,
            onvalue=-1,
            offvalue=1,
            variable=self.nocturne,
            text="mode nuit",
            background="dark turquoise",
            activebackground="turquoise",
            highlightbackground="navy",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.nocturnecb.select()
        with open("memoire.txt", "r") as f:
            fond = f.readlines()[1]
        with open("memoire.txt", "r") as f:
            seuil = f.readlines()[2]

        self.fondscale = tk.Scale(
            frame2,
            label="fond",
            length=self.taille // 20 * 3,
            showvalue=False,
            orient="horizontal",
            command=self.modifie,
            to=255,
            background="royalblue1",
            highlightthickness=0,
            troughcolor="dark turquoise",
            font=f"helvetica {self.taille // 60} bold",
        )

        self.seuilscale = tk.Scale(
            frame2,
            label="taille faisceau",
            length=self.taille // 10 * 2,
            showvalue=False,
            orient="horizontal",
            command=self.modifie,
            from_=50,
            to=2500,
            background="royalblue1",
            highlightthickness=0,
            troughcolor="dark turquoise",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.fondscale.set(fond)
        self.seuilscale.set(seuil)
        self.multitrackcb.deselect()
        s = ttk.Style()
        s.theme_create(
            "combostyle",
            parent="alt",
            settings={
                "TCombobox": {
                    "configure": {
                        "selectbackground": "dark turquoise",
                        "fieldbackground": "light sky blue",
                        "background": "dark turquoise",
                    }
                },
                "TMenubutton": {"configure": {"background": "royalblue3"}},
                "TButton": {
                    "configure": {
                        "background": "royalblue3",
                    }
                },
                "TFrame": {"configure": {"background": "royalblue1"}},
                "TLabel": {"configure": {"background": "royalblue1"}},
                "TScrollbar": {"configure": {"background": "royalblue1"}},
            },
        )
        s.theme_use("combostyle")
        self.select_fenetre = tk.StringVar()
        self.cbdata = ttk.Combobox(
            frame2,
            textvariable=self.select_fenetre,
            style="TCombobox",
            font=f"helvetica {self.taille // 60} bold",
        )
        self.fenetrestr = [""]
        self.cbdata["values"] = self.fenetrestr
        self.cbdata["state"] = "readonly"
        self.canvaco.grid(row=1, column=1, padx=5, pady=5)
        self.accesserveur.grid(row=1, column=2, padx=5, pady=5)
        self.parametreserveur.grid(row=1, column=5, padx=5, pady=5)
        self.eteindre.grid(row=1, column=4, padx=5, pady=5)
        self.redemarrer.grid(row=1, column=3, padx=5, pady=5)
        self.videobutton.grid(row=1, column=8, padx=5)
        self.photobutton.grid(row=1, column=7, padx=5)
        self.fondscale.grid(column=6, row=2, padx=5)
        self.seuilscale.grid(column=7, row=2, padx=5)
        self.multitrackcb.grid(column=8, row=2, padx=5)
        self.nocturnecb.grid(column=9, row=2, padx=5)
        self.cbdata.grid(column=10, row=2, padx=5)
        self.analysebutton.grid(column=11, row=2, padx=5)
        self.sauvegarde.grid(column=0, row=1, padx=5, pady=5)
        self.compare.grid(column=1, row=1, padx=5, pady=5)
        self.acq.grid(column=8, row=1, padx=5, pady=5)
        self.scan.grid(column=11, row=1, padx=5, pady=5)
        self.fenetre = {"video": ""}
        self.photo = {"video": ""}
        self.image = {"video": ""}
        self.analyseonoff = 0
        self.update_frame()

    def modifie(self, a):
        with open("memoire.txt", "r") as f:
            ip = f.readlines()[0][0:12]
        with open("memoire.txt", "w") as f:
            f.writelines(
                [
                    ip + "\n",
                    str(self.fondscale.get()) + "\n",
                    str(self.seuilscale.get()),
                ]
            )

    def demarre(self):
        self.canvaco.itemconfig(self.co, fill="yellow")
        self.after(500, self.testing)

    def parametre(self):
        try:
            self.parframe.destroy()
        except Exception:
            pass
        self.parframe = tk.Toplevel()
        self.parframe.title(
            "parametre Raspberry Pi 5",
        )
        self.parframe.geometry("600x350")
        self.parframe.configure(background="royalblue1")
        label = tk.Label(
            self.parframe,
            text="IP raspberry Pi:",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        label.pack(pady=10)

        entree = tk.Entry(
            self.parframe,
            font=f"helvetica {self.taille // 60} bold",
            background="light sky blue",
        )
        entree.pack(pady=10)

        with open("memoire.txt", "r") as f:
            ip = f.readlines()[0][0:12]
            entree.insert(0, ip)

        def updateip():
            with open("memoire.txt", "w") as f:
                f.writelines(
                    [
                        entree.get() + "\n",
                        str(self.fondscale.get()) + "\n",
                        str(self.seuilscale.get()),
                    ]
                )

        bouton_update = tk.Button(
            self.parframe,
            text="Mettre à jour",
            font=f"helvetica {self.taille // 60} bold",
            bg="dark turquoise",
            activebackground="turquoise",
            highlightbackground="dark blue",
            command=updateip,
        )
        bouton_update.pack(pady=10)
        label2 = tk.Label(
            self.parframe,
            text="commande terminal unix:",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        label2.pack(pady=10)

        entree2 = tk.Entry(
            self.parframe,
            font=f"helvetica {self.taille // 60} bold",
            background="light sky blue",
            width=40,
        )
        entree2.pack(pady=10)

        def comand():
            commanderp5(entree2.get())
            entree2.delete(0, len(entree2.get()))

        bouton_update2 = tk.Button(
            self.parframe,
            text="envoyer",
            font=f"helvetica {self.taille // 60} bold",
            bg="dark turquoise",
            activebackground="turquoise",
            highlightbackground="dark blue",
            command=comand,
        )
        bouton_update2.pack(pady=10)

    def save(self):
        try:
            self.saveframe.destroy()
        except Exception:
            pass
        self.saveframe = tk.Toplevel()
        self.saveframe.title(
            "enregistrement d'image",
        )
        self.saveframe.geometry(f"{self.taille//12*7}x{self.taille//3}")
        self.saveframe.configure(background="royalblue1")
        frame1 = tk.Frame(self.saveframe, bg="royalblue1")
        frame2 = tk.Frame(self.saveframe, bg="royalblue1")
        frame3 = tk.Frame(self.saveframe, bg="royalblue1")
        frame4 = tk.Frame(self.saveframe, bg="royalblue1")
        canvaco = tk.Canvas(
            frame4,
            background="royalblue1",
            height=self.taille // 30,
            width=self.taille // 30,
            highlightthickness=0,
        )
        co = canvaco.create_oval(
            4, 4, self.taille // 30 - 4, self.taille // 30 - 4, width=4, fill="orange"
        )
        canvaco.pack(side="right")
        cb = ttk.Combobox(
            frame1,
            style="TCombobox",
            font=f"helvetica {self.taille // 60} bold",
        )

        def updatebary(string):
            string = cb.get()
            if string == "":
                canvaco.itemconfig(co, fill="orange")
            else:
                barycheck = self.fenetre[string].bary
                if barycheck == 0:
                    canvaco.itemconfig(co, fill="red")
                elif barycheck == 1:
                    canvaco.itemconfig(co, fill="light green")

        cb.bind("<<ComboboxSelected>>", updatebary)
        cb["values"] = self.fenetrestr
        label1 = tk.Label(
            frame1,
            text="Photo à sauvegarder: ",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        label2 = tk.Label(
            frame2,
            text="Nom :    ",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        label3 = tk.Label(
            frame3,
            text="Chemin : ",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        label4 = tk.Label(
            frame4,
            text="barycentre analysé : ",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        frame1.pack(pady=10)
        frame2.pack(pady=10)
        frame3.pack(pady=10)
        frame4.pack(pady=10)
        label1.pack(side="left")
        label2.pack(side="left")
        label3.pack(side="left")
        label4.pack(side="left")
        cb.pack()
        entree = tk.Entry(
            frame2,
            font=f"helvetica {self.taille // 60} bold",
            background="light sky blue",
        )
        entree2 = tk.Entry(
            frame3,
            font=f"helvetica {self.taille // 60} bold",
            background="light sky blue",
        )

        cherche = tk.Button(
            frame3,
            text="chercher",
            font=f"helvetica {self.taille // 60} bold",
            bg="dark turquoise",
            activebackground="turquoise",
            highlightbackground="dark blue",
        )

        def chemin():
            filename = filedialog.askdirectory(parent=self.saveframe)
            entree2.delete(0, tk.END)
            entree2.insert(tk.END, filename)

        cherche.config(
            command=chemin,
        )
        cherche.pack(side="right")
        entree.pack()
        entree2.pack(padx=10, pady=10)

        def sauve():
            today = datetime.date.today()
            barycentre = []
            contour = []
            if self.fenetre[cb.get()].bary == 1:
                barycentre = self.barycentredico[cb.get()]
                contour = self.contourdico[cb.get()]
            if importable(entree.get()):
                importe(
                    (today.day, today.month, today.year),
                    entree.get(),
                    barycentre,
                    contour,
                    entree2.get(),
                    self.image[cb.get()],
                )
                self.saveframe.destroy()
            else:
                labelcheck.config(text="le nom est déjà utilisé")

        bouton_update = tk.Button(
            self.saveframe,
            text="sauvegarder",
            font=f"helvetica {self.taille // 60} bold",
            bg="dark turquoise",
            command=sauve,
            activebackground="turquoise",
            highlightbackground="dark blue",
        )
        labelcheck = tk.Label(
            self.saveframe,
            text="",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        labelcheck.pack()
        bouton_update.pack(pady=10)

    def automatical(self):
        try:
            self.automaticalframe.destroy()
        except Exception:
            pass
        self.automaticalframe = tk.Toplevel()
        self.automaticalframe.title(
            "acquisition automatique",
        )
        self.automaticalframe.geometry(f"{self.taille //3}x{self.taille //6}")
        self.automaticalframe.configure(background="royalblue1")

        frame1 = tk.Scale(
            self.automaticalframe,
            label="délais",
            length=self.taille // 5,
            showvalue=True,
            orient="horizontal",
            command=self.modifie,
            to=100,
            from_=1,
            background="royalblue1",
            highlightthickness=0,
            troughcolor="dark turquoise",
            font=f"helvetica {self.taille // 60} bold",
        )

        frame1.pack(pady=10)
        bouton_update = tk.Button(
            self.automaticalframe,
            text="lancer l'acquisition",
            font=f"helvetica {self.taille // 60} bold",
            bg="dark turquoise",
            command=lambda: self.acquisition(frame1.get()),
            activebackground="turquoise",
            highlightbackground="dark blue",
        )

        bouton_update.pack(pady=10)

    def acquisition(self, delay):

        try:
            self.automaticalframe.destroy()
            self.acquisitionframe.destroy()
        except Exception:
            pass
        self.acquisitionframe = tk.Toplevel()
        self.acquisitionframe.title(
            "acquisition automatique",
        )
        self.acquisitionframe.geometry(f"{640}x{480+self.taille //10}")
        self.acquisitionframe.configure(background="light sky blue")

        self.videoacq = tk.Label(self.acquisitionframe)
        self.videoacq.pack()

        frame1 = tk.Frame(self.acquisitionframe, bg="royalblue1")
        scrollbar = tk.Scrollbar(
            frame1, orient=tk.VERTICAL, background="light sky blue"
        )
        self.sslistbox = tk.Listbox(
            frame1,
            yscrollcommand=scrollbar.set,
            height=10,
            font=f"helvetica {self.taille // 60} bold",
            width=40,
            background="light sky blue",
        )
        scrollbar.config(command=self.sslistbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.sslistbox.pack(side="left", fill="both", expand=True)
        frame1.pack()

        image = update_image()
        tuplebar = detecte_faisceau_c(
            self.fondscale.get(),
            image,
            self.multitrack.get(),
            self.seuilscale.get(),
            1,
            self.nocturne.get(),
        )
        barycentre = tuplebar[0]
        k = 0
        while barycentre[k][0] == 2143:
            k += 1
        self.actbary = (barycentre[k][0], barycentre[k][1])
        self.ssupdate_frame(delay)

    def comparing(self):
        try:
            self.compareframe.destroy()
        except Exception:
            pass
        self.compareframe = tk.Toplevel()
        self.compareframe.title(
            "comparaison d'image",
        )
        self.compareframe.geometry(f"{self.taille // 12*7}x{self.taille // 12*5}")
        self.compareframe.configure(background="royalblue1")
        dates, noms, barycentres, contours, chemin = exporte()
        frame1 = tk.Frame(self.compareframe, bg="royalblue1")
        scrollbar = tk.Scrollbar(
            frame1, orient=tk.VERTICAL, background="light sky blue"
        )
        listbox = tk.Listbox(
            frame1,
            yscrollcommand=scrollbar.set,
            selectmode="single",
            height=10,
            font=f"helvetica {self.taille // 60} bold",
            width=40,
            background="light sky blue",
        )
        label = tk.Label(
            self.compareframe,
            text="photo à comparer",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        labelcheck = tk.Label(
            self.compareframe,
            text="",
            font=f"helvetica {self.taille // 60} bold",
            background="royalblue1",
        )
        cb = ttk.Combobox(
            self.compareframe,
            style="TCombobox",
            font=f"helvetica {self.taille // 60} bold",
        )

        cb["values"] = self.fenetrestr

        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both", expand=True)

        for i in range(len(noms)):
            listbox.insert(
                tk.END, f"{noms[i]} - {dates[i][0]}/{dates[i][1]}/{dates[i][2]}"
            )

        frame1.pack(pady=10)
        label.pack(pady=10)
        cb.pack(pady=10)

        def compareencore():

            selection = listbox.curselection()
            if selection:
                index = selection[0]
                nom, date, barycentre, contour, image = (
                    noms[index],
                    dates[index],
                    barycentres[index],
                    contours[index],
                    Image.open(chemin[index] + "/" + noms[index] + ".png"),
                )

                pcom = cb.get()
                self.compareframe.destroy()
                n = nom + "/" + pcom
                a = len(self.fenetre)
                self.fenetre[n] = ssfenetre(self, a, n, 1)
                self.fenetrestr.append(n)
                self.cbdata["values"] = self.fenetrestr
                self.fenetre[n].place(
                    x=self.taille // 6 + 10 * len(self.fenetre),
                    y=self.taille // 6 + 10 * len(self.fenetre),
                )
                self.image[n] = image
                self.photo[n] = tk.Label(self.fenetre[n])
                if pcom != "video":
                    self.preanalyse(pcom, n, (0, 0, 255))
                else:
                    self.listecomparaisonimage[n] = (
                        chemin[index] + "/" + noms[index] + ".png"
                    )
                photo = ImageTk.PhotoImage(image)
                self.photo[n].config(image=photo)
                self.photo[n].image = photo
                self.photo[n].pack()
            else:
                labelcheck.config(text="selectionez des photos à comparer")

        bouton_update = tk.Button(
            self.compareframe,
            text="comparer",
            font=f"helvetica {self.taille // 60} bold",
            bg="dark turquoise",
            command=compareencore,
            activebackground="turquoise",
            highlightbackground="dark blue",
        )
        labelcheck.pack()
        bouton_update.pack(pady=10)

    def testing(self):
        def raiseexception(signum, frame):

            raise Exception

        signal.signal(signal.SIGALRM, raiseexception)
        signal.setitimer(signal.ITIMER_REAL, 1)

        try:
            update_image()
            self.canvaco.itemconfig(self.co, fill="light green")
        except Exception as e:
            print(type(e).__name__)

            traceback.print_exc()
            # ou
            print(traceback.format_exc())
            self.canvaco.itemconfig(self.co, fill="red")
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)

    def preanalyse(self, source, cible, couleur=(0, 255, 0)):
        tuplebar = detecte_faisceau_c(
            self.fondscale.get(),
            self.image[source],
            self.multitrack.get(),
            self.seuilscale.get(),
            1,
            self.nocturne.get(),
        )
        barycentre = tuplebar[0]
        contour = tuplebar[1]
        self.barycentredico[cible] = barycentre
        self.contourdico[cible] = contour
        for i, j in contour:
            self.image[cible].putpixel(
                (i, j),
                couleur,
            )

        for k in range(len(barycentre)):
            if barycentre[k][0] != 2143:
                for i in range(8):

                    self.image[cible].putpixel(
                        (barycentre[k][0] + i, barycentre[k][1] + 1),
                        couleur,
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] - i, barycentre[k][1] + 1),
                        couleur,
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] + 1, barycentre[k][1] + i),
                        couleur,
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] + 1, barycentre[k][1] - i),
                        couleur,
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] + i, barycentre[k][1]), couleur
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] - i, barycentre[k][1]), couleur
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0], barycentre[k][1] + i), couleur
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0], barycentre[k][1] - i), couleur
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] + i, barycentre[k][1] - 1),
                        couleur,
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] - i, barycentre[k][1] - 1),
                        couleur,
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] - 1, barycentre[k][1] + i),
                        couleur,
                    )
                    self.image[cible].putpixel(
                        (barycentre[k][0] - 1, barycentre[k][1] - i),
                        couleur,
                    )

        return self.image[cible]

    def analyse(self, source, cible):

        if self.analyseonoff == 1:
            self.analyseonoff = 0
            self.scan.grid_forget()
            self.fenetre["video"].bary = 0
            self.analysebutton.config(text="detection de faisceau")
            return
        if source == "":
            pass
        elif source == "video":
            self.analysebutton.config(text="arreter la detection  ")
            self.analyseonoff = 1
            self.scan.grid(column=11, row=1, padx=5, pady=5)
            self.fenetre["video"].bary = 1
        else:

            image = self.preanalyse(source, cible)
            n = cible + " track"
            a = len(self.fenetre)
            self.fenetre[n] = ssfenetre(self, a, n, 1)
            self.fenetrestr.append(n)
            self.cbdata["values"] = self.fenetrestr
            self.fenetre[n].place(
                x=self.taille // 6 + 10 * len(self.fenetre),
                y=self.taille // 6 + 10 * len(self.fenetre),
            )
            self.photo[n] = tk.Label(self.fenetre[n])
            photo = ImageTk.PhotoImage(image)
            self.photo[n].config(image=photo)
            self.photo[n].image = photo
            self.photo[n].pack()

    def streaming(self):
        if self.onoff == 0:
            self.onoff = 1
            self.fenetre["video"] = ssfenetre(self, 0, f"video")
            self.fenetre["video"].place(x=self.taille // 6, y=self.taille // 6)
            self.videolabel = tk.Label(self.fenetre["video"])
            self.videolabel.pack()
            self.videobutton.config(text="stop ")
            self.fenetrestr[0] = "video"
            self.cbdata["values"] = self.fenetrestr
        elif self.onoff == 1:
            self.onoff = 2
            self.videobutton.config(text="video ")
        elif self.onoff == 2:
            self.onoff = 1
            self.videobutton.config(text="stop ")
            self.fenetrestr[0] = "video"
            self.cbdata["values"] = self.fenetrestr

    def photoing(self):
        if self.canvaco.itemcget(self.co, "fill") == "light green":
            n = len(self.fenetre)
            self.fenetre[f"photo {n}"] = ssfenetre(self, n, f"photo {n}")
            self.fenetrestr.append(f"photo {n}")
            self.cbdata["values"] = self.fenetrestr
            self.fenetre[f"photo {n}"].place(
                x=self.taille // 6 + 10 * n, y=self.taille // 6 + 10 * n
            )
            self.photo[f"photo {n}"] = tk.Label(self.fenetre[f"photo {n}"])
            image = update_image()
            self.image[f"photo {n}"] = image
            photo = ImageTk.PhotoImage(self.image[f"photo {n}"])
            self.photo[f"photo {n}"].config(image=photo)
            self.photo[f"photo {n}"].image = photo
            self.photo[f"photo {n}"].pack()

    def scaning(self):
        try:
            self.scanframe.destroy()
        except Exception:
            pass
        image = update_image()
        self.scanframe = ssfenetre(self, -7, "scan", 1)

        k = 0
        while self.barycentredico["video"][k][0] == 2143:
            k += 1
        x0, y0, m = self.barycentredico["video"][k]
        max = self.fondscale.get()
        si = self.nocturne.get()
        axex = [image.getpixel((x0, y0))[0]]
        axey = [image.getpixel((x0, y0))[0]]
        x1, y1 = x0 + 1, y0
        while (
            si * image.getpixel((x1, y1))[0] < si * max
            or si * image.getpixel((x1, y1))[0] < si * max
            or si * image.getpixel((x1, y1))[0] < si * max
        ):
            axex.append((image.getpixel((x1, y1)))[0])
            x1 += 1
        for i in range(15):
            axex.append((image.getpixel((x1, y1)))[0])
            x1 += 1
        r1 = x1 - 1
        x1, y1 = x0 - 1, y0
        while (
            si * image.getpixel((x1, y1))[0] < si * max
            or si * image.getpixel((x1, y1))[0] < si * max
            or si * image.getpixel((x1, y1))[0] < si * max
        ):
            axex = [(image.getpixel((x1, y1)))[0]] + axex
            x1 -= 1
        for i in range(15):
            axex = [(image.getpixel((x1, y1)))[0]] + axex
            x1 -= 1
        r2 = x1 + 1

        x1, y1 = x0, y0 + 1
        while (
            si * image.getpixel((x1, y1))[0] < si * max
            or si * image.getpixel((x1, y1))[0] < si * max
            or si * image.getpixel((x1, y1))[0] < si * max
        ):
            axey.append((image.getpixel((x1, y1)))[0])
            y1 += 1
        for i in range(15):
            axey.append((image.getpixel((x1, y1)))[0])
            y1 += 1
        r3 = y1 - 1
        x1, y1 = x0, y0 - 1
        while (
            si * image.getpixel((x1, y1))[0] < si * max
            or si * image.getpixel((x1, y1))[0] < si * max
            or si * image.getpixel((x1, y1))[0] < si * max
        ):
            axey = [(image.getpixel((x1, y1)))[0]] + axey
            y1 -= 1
        for i in range(15):
            axey = [(image.getpixel((x1, y1)))[0]] + axey
            y1 -= 1
        r4 = y1 + 1
        figure = Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(1, 2, 1)
        ax.plot(
            list(range(r2, r1 + 1, 1)),
            axex,
            "-",
        )
        ax.set_title("axe horizontal")
        bx = figure.add_subplot(1, 2, 2)

        bx.set_title("axe vertical")
        bx.plot(
            list(range(r4, r3 + 1, 1)),
            axey,
            "-",
        )
        self.canvas = FigureCanvasTkAgg(figure, master=self.scanframe)
        self.canvas.draw()
        self.widget = self.canvas.get_tk_widget()
        self.widget.pack()
        self.scanframe.place(x=self.taille // 12 * 5, y=self.taille // 10 * 2)

    def atomise(self, number):
        if number == "video":
            self.onoff = 0
            self.videolabel = None
            self.videobutton.config(text="video")
            self.fenetrestr[0] = ""
            self.cbdata["values"] = self.fenetrestr
            try:
                self.scanframe.destroy()
            except Exception:
                pass
        elif number == "scan":
            pass
        else:
            if self.fenetre[number].bary == 0:
                self.fenetrestr.remove(number)
                self.cbdata["values"] = self.fenetrestr
            if number in self.listecomparaisonimage:
                del self.listecomparaisonimage[number]

    def ssupdate_frame(self, delay):

        try:
            if self.canvaco.itemcget(self.co, "fill") == "light green":
                image = update_image()
                tuplebar = detecte_faisceau_c(
                    self.fondscale.get(),
                    image,
                    self.multitrack.get(),
                    self.seuilscale.get(),
                    1,
                    self.nocturne.get(),
                )
                barycentre = tuplebar[0]
                k = 0
                while barycentre[k][0] == 2143:
                    k += 1
                self.sslistbox.insert(
                    0,
                    f"({barycentre[k][0]},{barycentre[k][1]})  ->   {round(9.8*sqrt((-self.actbary[0]+barycentre[k][0])**2+(-self.actbary[1]+barycentre[k][1])**2),1)}microm",
                )
                contour = tuplebar[1]
                listimage = [image]
                couleur = [(0, 255, 0)]
                kc = 0
                for imagex in listimage:

                    for i, j in contour:
                        imagex.putpixel(
                            (i, j),
                            couleur[kc],
                        )
                    for k in range(len(barycentre)):
                        if barycentre[k][0] != 2143:
                            for i in range(8):
                                try:
                                    imagex.putpixel(
                                        (barycentre[k][0] + i, barycentre[k][1] + 1),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - i, barycentre[k][1] + 1),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] + 1, barycentre[k][1] + i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] + 1, barycentre[k][1] - i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] + i, barycentre[k][1]),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - i, barycentre[k][1]),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0], barycentre[k][1] + i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0], barycentre[k][1] - i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] + i, barycentre[k][1] - 1),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - i, barycentre[k][1] - 1),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - 1, barycentre[k][1] + i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - 1, barycentre[k][1] - i),
                                        couleur[kc],
                                    )
                                except IndexError:
                                    pass
                    kc += 1
            photo = ImageTk.PhotoImage(image)

            self.videoacq.config(image=photo)
            self.videoacq.image = photo
        except Exception as e:
            print(type(e).__name__)

            traceback.print_exc()
            # ou
            print(traceback.format_exc())
        self.after(delay * 1000, lambda: self.ssupdate_frame(delay))

    def update_frame(self):

        try:
            if self.canvaco.itemcget(self.co, "fill") == "light green":
                image = update_image()
            self.image["video"] = image

            if self.analyseonoff == 1:
                t1 = time.time()
                tuplebar = detecte_faisceau_c(
                    self.fondscale.get(),
                    self.image["video"],
                    self.multitrack.get(),
                    self.seuilscale.get(),
                    1,
                    self.nocturne.get(),
                )
                t2 = time.time()
                barycentre = tuplebar[0]
                contour = tuplebar[1]
                self.barycentredico["video"] = barycentre
                self.contourdico["video"] = contour
                listimage = [image]
                couleur = [(0, 255, 0)]
                kc = 0
                listimage += [
                    Image.open(self.listecomparaisonimage[a])
                    for a in self.listecomparaisonimage
                ]
                couleur += [(0, 0, 255) for a in self.listecomparaisonimage]
                for imagex in listimage:

                    for i, j in contour:
                        imagex.putpixel(
                            (i, j),
                            couleur[kc],
                        )
                    for k in range(len(barycentre)):
                        if barycentre[k][0] != 2143:
                            for i in range(8):
                                try:
                                    imagex.putpixel(
                                        (barycentre[k][0] + i, barycentre[k][1] + 1),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - i, barycentre[k][1] + 1),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] + 1, barycentre[k][1] + i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] + 1, barycentre[k][1] - i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] + i, barycentre[k][1]),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - i, barycentre[k][1]),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0], barycentre[k][1] + i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0], barycentre[k][1] - i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] + i, barycentre[k][1] - 1),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - i, barycentre[k][1] - 1),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - 1, barycentre[k][1] + i),
                                        couleur[kc],
                                    )
                                    imagex.putpixel(
                                        (barycentre[k][0] - 1, barycentre[k][1] - i),
                                        couleur[kc],
                                    )
                                except IndexError:
                                    pass
                    kc += 1
            photo = ImageTk.PhotoImage(image)
            self.videolabel.config(image=photo)
            self.videolabel.image = photo
            k = 0
            for key in self.listecomparaisonimage:
                imagex = listimage[k + 1]

                n = self.listecomparaisonimage[key]
                photo = ImageTk.PhotoImage(imagex)
                self.photo[key].config(image=photo)
                self.photo[key].image = photo
                k += 1
        except Exception as e:
            print(type(e).__name__)

            traceback.print_exc()
            # ou
            print(traceback.format_exc())
        self.after(30, self.update_frame)


appli = app()
appli.mainloop()
#######################################
############################################################
