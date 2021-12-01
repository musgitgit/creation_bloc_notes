from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import ttk, messagebox
import os

savedFile = {1:""} # Cette ligne nous permettra de stocker les objets files qui ne tiennent pas dans une instance de classe

#====================================== 
# I - Classe de la fenêtre pricipale 
#====================================== 
#Pour la suite : fen ----> fenètre principale
#                zone_texte----> zone de texte

class creer_fen_prin:     
    def __init__(self,fen,zone_texte):
        # Fenêtre principale        
        self.fen = fen         
        # Main Text Widget
        self.zone_texte=zone_texte
    # Création de la fenêtre tkinter   
    def creer(self):         
        self.fen = Tk()                          #Création de la 1ère fenètre
        self.fen.title("Mon Bloc-notes") #Donner un titre à la fenètre       
        self.fen.geometry("500x400")             #Donner les dimensions de la fenètre initiale
        self.fen.minsize(400, 350)               #Impose des dimensions minimales à la fenètre d'affichage
        self.fen.iconbitmap(r'icone.ico')        #Changer l'icone de la fenètre 
    # Activer la zone d'écriteur                   
    def activer_zone_text(self):         
        self.zone_texte = Text(width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True)
        self.zone_texte.pack()
    # Génération de la fenêtre principale             
    def boucle_window_bloc_notes(self):         
        self.fen.mainloop()

    #========================================
    #  II - Définition des actions des menus 
    #========================================
    #------------------------------
    # II.1 - actions du menu Fichier 
    #-------------------------------     
    def quitter(self):         
        self.fen.destroy()
    def nouveau(self):
        os.popen("bloc_notes.py")   # sur ma version python c'est cette commande qui marche non os.popen("python bloc_notes.py")
    def fopen(self):
        try:
            file = self.fen.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select File",filetypes = (("Text Files","*.txt"),("all files","*.*")))     
            fp = open(file,"r")         
            r = fp.read()         
            self.zone_texte.insert(1.0,r)
        except:
            # si on annule l'ouverture
            pass
      # Menu Enregistrer sous  
    def saveAs(self):         
       # create save dialog         
        fichier=self.fen.filename=filedialog.asksaveasfilename(initialdir =  "/",title = "Enregistrer Sous\         ",filetypes = (("Fichier Texte","*.txt"),  ("Tous les fichiers","*.*")))         
        fichier = fichier + ".txt" 
       # Utilisation du dictionnaire pour stocker le fichier                
        savedFile[1] = fichier         
        f = open(fichier,"w")         
        s = self.zone_texte.get("1.0",END)         
        f.write(s)          
        f.close()
       # menu Enregistrer
    def save(self):
        if(savedFile[1] ==""):             
            self.saveAs()                     
        else:             
            f = open(savedFile[1],"w")
            s = self.zone_texte.get("1.0",END)             
            f.write(s)              
            f.close()
    #------------------------------ 
    # II.2 - actions du menu Edition 
    #------------------------------     
    def copy(self):      
        self.zone_texte.clipboard_clear()          
        self.zone_texte.clipboard_append(self.zone_texte.selection_get())          
    def past(self):         
        self.zone_texte.insert(INSERT, self.zone_texte.clipboard_get())         
    def cut(self):         
        self.copy()         
        self.zone_texte.delete("sel.first","sel.last")
    def annuler(self):
        self.zone_texte.edit_undo()
    def retablir(self):
        self.zone_texte.edit_redo()

    
    #------------------------------ 
    # II.3 - actions du menu Outils 
    #------------------------------
    def bold(self):
        bold_font = font.Font(self.zone_texte, self.zone_texte.cget("font"))
        bold_font.configure(weight="bold")
        self.zone_texte.tag_configure("bold", font=bold_font)
        current_tags = self.zone_texte.tag_names("sel.first")
        if "bold" in current_tags:
            self.zone_texte.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.zone_texte.tag_add("bold", "sel.first", "sel.last")
    def italics_it(self):
        italics_font = font.Font(self.zone_texte, self.zone_texte.cget("font"))
        italics_font.configure(slant="italic")
        self.zone_texte.tag_configure("italic", font=italics_font)
        current_tags = self.zone_texte.tag_names("sel.first")
        if "italic" in current_tags:
            self.zone_texte.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.zone_texte.tag_add("italic", "sel.first", "sel.last")
    def select_all(self):
        self.zone_texte.tag_add('sel', '1.0', 'end')
    def clear_all(self):
        self.zone_texte.delete(1.0, END)
    def text_color(self):  # Pour choisir la couleur du texte, faut d'abord selectioner le texte à l'aide de la souris puis on peut le mettre en couleur qu'on veut
        my_color = colorchooser.askcolor()[1]
        color_font = font.Font(self.zone_texte, self.zone_texte.cget("font"))
        self.zone_texte.tag_configure("colored", font=color_font, foreground=my_color)
        current_tags = self.zone_texte.tag_names("sel.first")
        if "colored" in current_tags:
            self.zone_texte.tag_remove("colored", "sel.first", "sel.last")
        else:
            self.zone_texte.tag_add("colored", "sel.first", "sel.last")
    def bg_color(self):
        my_color = colorchooser.askcolor()[1]
        if my_color:
            self.zone_texte.config(bg=my_color)
    
    
    #------------------------------ 
    # II.4 - actions du menu Aide 
    #------------------------------
    def a_propos(self):
        messagebox.showinfo("Créer vos documents texte           ") #Créer une fenêtre pop-up pour afficher le message
    #====================================== 
    #  III - Méthodes d'ajout des menus 
    #======================================
    def ajouter_menus(self):         
        # 1 - Création de la barre des menus         
        menuBar = Menu(self.fen)                  
        # 2 - Création du menu Fichier         
        menuFichier = Menu(menuBar,tearoff=0)                       #tearoff = 0 ou tearoff = False pour ne pas détacher le menu de la fenètre principale
        menuBar.add_cascade(label = "Fichier", menu=menuFichier)           
        # Création des sous menus du menu Fichier
        menuFichier.add_command(label="Nouveau", command = self.nouveau)         
        menuFichier.add_command(label="Ouvrir", command = self.fopen)         
        menuFichier.add_command(label="Enregistrer", command = self.save)         
        menuFichier.add_command(label="Enregistrer sous", command = self.saveAs)         
        menuFichier.add_command(label="Quitter", command = self.quitter)        
                          
        #3 - Création du Menu Edition         
        menuEdition= Menu(menuBar,tearoff=0)         
        menuBar.add_cascade(label = "Edition ", menu=menuEdition)
        # Création des sous menus du menu Edition
        menuEdition.add_command(label="Annuler", command = self.annuler)          
        menuEdition.add_command(label="Rétablir", command = self.retablir)                 
        menuEdition.add_command(label="Copier", command = self.copy)        
        menuEdition.add_command(label="Couper", command = self.cut)         
        menuEdition.add_command(label="Coller", command = self.past)                 
        #4 - Création du Menu Outils         
        menuOutils = Menu(menuBar,tearoff=0)         
        menuBar.add_cascade(label = "Outils", menu = menuOutils)
        # Création des sous menus du menu Outils
        menu1 = Menu(menuOutils, tearoff=0)
        menuOutils.add_cascade(label="Préférences", menu = menu1)
        menu1.add_command(label="Texte en gras", command = self.bold)
        menu1.add_command(label="Italic Texte", command = self.italics_it)
        menu1.add_command(label="Sélectionner la couleur de texte", command = self.text_color)
        menu1.add_command(label="Sélectionner la couleur de la zone d'écriteur", command = self.bg_color)
        menu1.add_command(label="Sélectionner Tout", command = self.select_all)
        menu1.add_command(label="Supprimer Tout", command = self.clear_all)
        # Création du Menu Aide
        menuAide = Menu(menuBar,tearoff=0)         
        menuBar.add_cascade(label = "Aide", menu = menuAide)
        # Création des sous menus du menu Aide
        menuAide.add_command(label="A propos", command = self.a_propos)

        # Configuration de la barre des menus
        self.fen.config (menu=menuBar)
       
# Création d'une instance sur la classe principale (l'objet)
window_bloc_notes = creer_fen_prin("fenetre","contenu")

# Appel des méthodes qui créent l'objet fenêtre avec tous ces composants
window_bloc_notes.creer()
window_bloc_notes.activer_zone_text() 
window_bloc_notes.ajouter_menus() 
window_bloc_notes.boucle_window_bloc_notes()
