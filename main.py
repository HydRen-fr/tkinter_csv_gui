# IMPORT ET CREATION DE L'INSTANCE TKINTER

import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

root = tk.Tk()
root.title("Application de traitement de fichiers CSV")


# FONCTIONS


csv_data = []


def charger_csv():
    global csv_data
    chemin = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if chemin:
        with open(chemin, 'r') as file:
            reader = csv.reader(file)
            csv_data = list(reader)
            csv_data = [ligne for ligne in csv_data if ligne] # Supprime les lignes vides
        
        create_table(csv_data)


def create_table(data):
    global table
    if 'table' in globals():
        table.destroy()  # Supprimer la Treeview existante
    
    table = ttk.Treeview(root)
    table["columns"] = data[0]
    table["show"] = "headings"
    
    for column in data[0]:
        table.heading(column, text=column)
    
    for ligne in data[1:]:
        table.insert("", "end", values=ligne)
    
    table.pack(pady=10)



def display_results(results):
    text_resultats.delete("1.0", tk.END)

    if type(results) == "str":
        if results:
            text_resultats.insert(tk.END, results)
        else:
            text_resultats.insert(tk.END, "Aucun résultat trouvé.")

    else:
        for ligne in results:
            text_resultats.insert(tk.END, ", ".join(ligne) + "\n")


def recherche(demande):
    global csv_data
    if demande:
        results = []
        for ligne in csv_data[1:]:
            for element in ligne:
                if demande.lower() in str(element).lower():
                    results.append(ligne)
                    break
        
        display_results(results)


def rechercher_valeurs_inferieures(descripteur, valeur):
    results = []
    index_descripteur = csv_data[0].index(descripteur)
    for ligne in csv_data[1:]:
        if ligne[index_descripteur] < valeur:
            results.append(ligne)
    display_results(results)

def rechercher_valeurs_superieures(descripteur, valeur):
    results = []
    index_descripteur = csv_data[0].index(descripteur)
    for ligne in csv_data[1:]:
        if ligne[index_descripteur] > valeur:
            results.append(ligne)
    display_results(results)



def recherche_doublons():
    global csv_data
    deja_vu = []
    doublons = []
    for ligne in csv_data[1:]:
        if ligne in deja_vu:
            doublons.append(ligne)
        else:
            deja_vu.append(ligne)

    display_results(doublons)


def supprimer_doublons():
    global csv_data
    deja_vu = []
    no_doublons = [csv_data[0]]  # Garder la première ligne (les descripteurs)
    for ligne in csv_data[1:]:
        if ligne not in deja_vu:
            deja_vu.append(ligne)
            no_doublons.append(ligne)
    create_table(no_doublons)


def fusion_csv():
    global csv_data
    chemins = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if chemins:
        fusion_data = []
        for chemin in chemins:
            with open(chemin, "r") as f:
                reader = csv.reader(f)
                fusion_data += list(reader)

        descripteurs = csv_data[0]
        fusion_descripteurs = fusion_data[0]

        if fusion_descripteurs == descripteurs:
            create_table(fusion_data)

        else:
            display_results("Les descripteurs ne correspondent pas.")

def exporter_csv():
    chemin = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if chemin:
        with open(chemin, "w", newline="") as file:
            writer = csv.writer(file)
            # Écrire les descripteurs de colonnes
            writer.writerow([table.heading(column)["text"] for column in table["columns"]])
            # Écrire les données de la table
            for ligne in table.get_children():
                writer.writerow([table.set(ligne, column) for column in table["columns"]])

def tri():
    global csv_data
    data = csv_data[1:]
    data.sort()
    data.insert(0, csv_data[0])
    create_table(data)






# WIDGETS POUR L'INTERFACE



# Widgets pour charger un fichier CSV
load_button = tk.Button(root, text="Charger un fichier CSV", command=charger_csv)
load_button.pack(fill="x", pady=10)

# Séparateur vertical
separator1 = ttk.Separator(root, orient="horizontal")
separator1.pack(fill="x")


# Widget pour la recherche de données
recherche_label = tk.Label(root, text="Rechercher:", font=("Arial", 12))
recherche_label.pack(pady=5)
recherche_entry = tk.Entry(root, font=("Arial", 12))
recherche_entry.pack(pady=5)
recherche_button = tk.Button(root, text="Rechercher", command=lambda: recherche(recherche_entry.get()), font=("Arial", 12), bg="lightblue", fg="black")
recherche_button.pack(pady=5)

# Séparateur vertical
separator7 = ttk.Separator(root, orient="horizontal")
separator7.pack(fill="x")

descripteur_label = tk.Label(root, text="Descripteur:", font=("Arial", 12))
descripteur_label.pack(pady=5)
descripteur_entry = tk.Entry(root, font=("Arial", 12))
descripteur_entry.pack()

valeur_label = tk.Label(root, text="Valeur:", font=("Arial", 12))
valeur_label.pack(pady=5)
valeur_entry = tk.Entry(root, font=("Arial", 12))
valeur_entry.pack()

inferieures_button = tk.Button(root, text="Rechercher les valeurs inférieures", command=lambda: rechercher_valeurs_inferieures(descripteur_entry.get(), valeur_entry.get()), font=("Arial", 12))
inferieures_button.pack(pady=5)

superieures_button = tk.Button(root, text="Rechercher les valeurs supérieures", command=lambda: rechercher_valeurs_superieures(descripteur_entry.get(), valeur_entry.get()), font=("Arial", 12))
superieures_button.pack(pady=5)

# Séparateur vertical
separator2 = ttk.Separator(root, orient="horizontal")
separator2.pack(fill="x")

# Widgets pour rechercher/supprimer les doublons
doublons_button = tk.Button(root, text="Rechercher les doublons", command=recherche_doublons, font=("Arial", 12), bg="lightblue", fg="black")
doublons_button.pack(pady=5)

supp_doublons_button = tk.Button(root, text="Supprimer les doublons", command=supprimer_doublons, font=("Arial", 12), bg="lightblue", fg="black")
supp_doublons_button.pack(pady=5)

# Séparateur vertical
separator3 = ttk.Separator(root, orient="horizontal")
separator3.pack(fill="x")

# Widget pour fusionner des fichiers CSV
fusion_button = tk.Button(root, text="Fusionner des fichiers CSV", command=fusion_csv, font=("Arial", 12), bg="lightblue", fg="black")
fusion_button.pack(pady=5)

# Séparateur vertical
separator4 = ttk.Separator(root, orient="horizontal")
separator4.pack(fill="x")

# Widget pour trier les lignes
tri_button = tk.Button(root, text="Trier les lignes", command=tri, font=("Arial", 12), bg="lightblue", fg="black")
tri_button.pack(pady=5)

# Séparateur vertical
separator5 = ttk.Separator(root, orient="horizontal")
separator5.pack(fill="x")

# Widget pour exporter le Treeview en fichier CSV
export_button = tk.Button(root, text="Exporter en CSV", command=exporter_csv, font=("Arial", 12), bg="lightblue", fg="black")
export_button.pack(pady=5)

# Séparateur vertical
separator6 = ttk.Separator(root, orient="horizontal")
separator6.pack(fill="x")

# Widget pour afficher les résultats de la recherche et des doublons
text_resultats = tk.Text(root, font=("Arial", 12), height=10, width=50)
text_resultats.pack(pady=10)




root.mainloop()