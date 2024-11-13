import customtkinter as ctk
import random
import webbrowser
import json
import os
from tkinter import messagebox 

# Bárki olvassa ezt, szeretnék elnézést kérni, nem szoktam kommenteket írni, leginkább tele szoktam trollkodni
# Ez csakis a gyakorlás céljából került megírásra. -HEKI


# Beállítások a következő indításhoz.
BEALLITASOK_FAJL = "random_biro_beallitasok.json" # Igen! Bárki is vagy, ez a fájlnév, ezt írd felül.

# Kedves kutakodó, nem tudom hol laksz vagy mit csinálsz, de ezek az ablak nevek.
ablaknevek_lista = ["Itt repül a repülő!", "Meg fogok bukni funkc progból xD", "Szia uram! Bojler eladó!", 
                    "Milfs in your area looking to have fun...", "Nem tudom mit írjak ide.", "bruh", "Help, meg fogok őrülni", 
                    "What if i can just *yoink*, i got your nose Voldemort!", "I hate League Of Legends", "Wanna play 5D Chess?",
                    "Hangin' out like Sayori does", "Chipi-chipi, chapa-chapa, Dubi-dubi, daba-daba"]

# Ezek a bíróban lévő feladat nevek 11/13/2024
nevek = [
    "1. Időjárás", "2. Emberek", "3. Lakás", "4. Utazás", "5. Bor", "6. Út", "7. Múzeum", "8. Munka",
    "9. Forgalom", "10. Nagyfal", "11. Születések", "12. Madarak", "13. Javító", "14. Utazás",
    "15. Raktár", "16. Rokonok", "17. Vállalat", "18. Röpzárthelyi", "19. Autóbérlés", "20. Ingatlanforgalmazó",
    "21. Kalapácsvető verseny", "22. Eső", "23. Terembeosztás", "24. Olimpiai kvalifikáció", "25. ÉvfolyamZH-Tanórák",
    "26. Szaloncukor", "27. Nyelvóra", "28. Sportnap", "29. Autókölcsönző", "30. Új Nemzeti Kiválóság Program",
    "31. Munkaközvetítő", "32. Állatkert", "33. Megrendelések", "34. Vonat", "35. Tőzsde", "36. Sportnap",
    "37. 2. MintaZH", "38. Bor - 2. gepes ZH 2019", "39. Hajók a kikötőben", "40. Tornádók", "41. Könyvtár", 
    "42. Vonatok szemben", "43. Lottó", "44. Foci", "45. Karácsonyi slágerek", "46. Sípályák", "47. Kézilabda"
]

class RandomNevValaszto(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ablak
        self.title(random.choice(ablaknevek_lista))
        self.geometry("1000x510")
        # Az én laptopomon ezek a méretek voltak jók, így pont belefér az összen feladatnév.
        # Nem vagyok benne biztos hogy másik kijelző méreten hogyan változik ez.

        # Alap Téma 
        self.tema_eppen = "dark"
        ctk.set_appearance_mode(self.tema_eppen)
        
        # betölti a kijelölt dobozokat
        self.allapot = self.beallitasok_betoltese()

        # doboz (csak a szép megjelenés miatt)
        gomb_keret = ctk.CTkFrame(self)
        gomb_keret.pack(fill="x", pady=10) 

        # alapszín változtatás
        self.tema_gomb = ctk.CTkButton(gomb_keret, text="világosra váltás", command=self.tema_csere)
        self.tema_gomb.grid(row=0, column=0, padx=10, pady=10, sticky="ew") 

        # GitHub gomb
        self.github_gomb = ctk.CTkButton(gomb_keret, text="GitHub", fg_color="grey", command=self.github_megnyitasa)
        self.github_gomb.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        gomb_keret.grid_columnconfigure(0, weight=1)
        gomb_keret.grid_columnconfigure(1, weight=1)

        # keret a dobozoknak
        self.doboz_keret = ctk.CTkFrame(self)
        self.doboz_keret.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.vatozo_lista = []  # ide mentem a végén a kijelölt feladatokat.
        for i, nev in enumerate(nevek): 
            var = ctk.BooleanVar(value=self.allapot.get(f"task{i}", False))
            doboz = ctk.CTkCheckBox(self.doboz_keret, text=nev, variable=var)
            doboz.grid(row=i//5, column=i%5, sticky="w", padx=5, pady=2)
            self.vatozo_lista.append((f"task{i}", var))

        # megnyitás gomb
        self.megnyitas = ctk.CTkButton(self, text="Kérek egy feladatot!", fg_color="green", command=self.feladat_kiiras)
        self.megnyitas.pack(pady=10)
        
        # biro gomb
        self.biro = ctk.CTkButton(self, text="Biro megnyitása", fg_color="purple", command=self.biro_megnyitasa)
        self.biro.pack(pady=10)
        
        # kilépés gomb
        self.kilepes_gomb = ctk.CTkButton(self, text="Kilépés", fg_color="red", command=self.mentes_kilepes)
        self.kilepes_gomb.pack(pady=10)

    def tema_csere(self):
        # Sötét / világos téma csere hogy este ne vakítson meg senkit xD
        if self.tema_eppen == "light":
            self.tema_eppen = "dark"
            self.tema_gomb.configure(text="világosra váltás")
        else:
            self.tema_eppen = "light"
            self.tema_gomb.configure(text="sötétre váltás")
        ctk.set_appearance_mode(self.tema_eppen)

    def github_megnyitasa(self):
        webbrowser.open("https://github.com/HKM0")

    def feladat_kiiras(self):
        # itt generálok a kijelölt dobozokból listát ami a randomhoz lentebb kell.
        bejelolt = [nev for nev, var in zip(nevek, [var for _, var in self.vatozo_lista]) if var.get()]
        if bejelolt:
            kivalasztott_random = random.choice(bejelolt)
            print(f"Kiválasztott feladat: {kivalasztott_random}")
            messagebox.showinfo(random.choice(ablaknevek_lista), f"Kiválasztott feladat: {kivalasztott_random}")
        else:
            messagebox.showinfo("Hiba!", "Nincs kijelölve feladat!")

    def biro_megnyitasa(self):
        webbrowser.open("http://biro.inf.elte.hu/faces/download.xhtml")

    def mentes_kilepes(self):
        # Elmentem a beállításokat a json-ba
        dobozok_jelolve = {name: var.get() for name, var in self.vatozo_lista}
        with open(BEALLITASOK_FAJL, "w") as f:
            json.dump(dobozok_jelolve, f)
        self.destroy() #arabok be like

    @staticmethod
    def beallitasok_betoltese():
        # kijelölt dobozok betöltése a jsonból ha létezik.
        if os.path.exists(BEALLITASOK_FAJL):
            with open(BEALLITASOK_FAJL, "r") as f:
                return json.load(f)
        return {}

if __name__ == "__main__":
    ctk.set_default_color_theme("dark-blue")
    app = RandomNevValaszto()
    app.mainloop()


# életemben nem írtam ilyen sok kommentet xd
# ha sikerülne valahogy az aktív jfwid-t megszereznem akkor automatikusan le tudnám tölteni a feladatlapot :(
# na mindegy, remélem segített a kód.

#   -HEKI