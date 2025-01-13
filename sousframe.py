import tkinter as tk


class ssfenetre(tk.Frame):
    def __init__(self, parent, number, nom, bary=0, **kwargs):
        super().__init__(
            parent,
            **kwargs,
            bg="grey",
            highlightbackground="black",
            highlightthickness=2,
        )
        self.bary = bary
        self.nom = nom
        self.click = {"x": 0, "y": 0}
        self.number = number
        self.root = parent
        self.taille = self.winfo_screenheight()
        self.config(width=640, height=self.taille // 40 + 480 + 40)
        self.propagate(0)
        self.titlebar = tk.Frame(
            self,
            bg="gray70",
            height=self.taille // 40,
            highlightbackground="black",
            highlightthickness=1,
        )
        self.titlebar.pack(fill="x", side="top")

        self.title = tk.Label(
            self.titlebar,
            text=nom,
            font=f"helvetica {self.taille//60} normal",
            bg="gray70",
        )
        self.closebutton = tk.Button(
            self.titlebar,
            highlightthickness=0,
            background="gray70",
            font=f"helvetica {self.taille//60} normal",
            text="X",
            command=self.close,
        )
        self.closebutton.pack(side="right")

        self.title.pack()
        self.resizer = tk.Canvas(
            self,
            bg="gray",
            highlightthickness=0,
            width=20,
            height=15,
            cursor="double_arrow",
        )
        self.resizer.create_line(1, 1, 19, 1, width=2)
        self.resizer.create_line(5, 6, 15, 6, width=2)
        self.resizer.create_line(9, 11, 11, 11, width=2)
        self.resizer.pack(side="bottom", anchor="se")

        self.titlebar.bind("<ButtonPress-1>", self.deplacestart)
        self.titlebar.bind("<B1-Motion>", self.deplacemotion)

        self.resizer.bind("<ButtonPress-1>", self.resizestart)
        self.resizer.bind("<B1-Motion>", self.resizemotion)

    def deplacestart(self, event):
        self.click["x"] = event.x
        self.click["y"] = event.y

    def deplacemotion(self, event):
        delta_x = event.x - self.click["x"]
        delta_y = event.y - self.click["y"]
        self.place(x=self.winfo_x() + delta_x, y=self.winfo_y() + delta_y)

    def resizestart(self, event):
        self.dicotaille = {
            "width": self.winfo_width(),
            "height": self.winfo_height(),
            "x": event.x,
            "y": event.y,
        }

    def resizemotion(self, event):
        delta_x = event.x - self.dicotaille["x"]
        delta_y = event.y - self.dicotaille["y"]

        self.config(
            width=max(self.winfo_width() + delta_x, self.taille // 6),
            height=max(self.winfo_height() + delta_y, self.taille // 6),
        )

    def close(self):
        self.root.atomise(self.nom)
        self.destroy()
