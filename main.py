import tkinter as tk
import hud
import personalized_exception as pe

class App:
    def __init__(self):
        self.default_path = "setting_default.json"
        self.main = None
    
    def redefine_path(self):
        file_path = tk.filedialog.askopenfilename(title="Select a configuration file", filetypes=[("JSON files", "*.json")])
        if file_path != "":
            self.default_path = file_path
            self.run()

    def run(self):
        try:
            self.main = hud.HUD(self.default_path)
            self.main.launch()

        except FileNotFoundError as e:
            tk.messagebox.showerror("Erreur", f"Fichier non trouvé: {self.default_path}\nLe fichier est invalide ou manquant.\nVeuillez sélectionner une autre fichier de configuration initial")
            self.redefine_path()

        except pe.FrictionNotInRange as e:
            tk.messagebox.showerror("Erreur de fichier de configuration initial",f"{e}\nVeuillez vérifier si la valeur du coefficient de friction dans le fichier de configuration\ncorrespond à l'intervalle permise.\nou choisir un autre fichier de configuration.")
            self.redefine_path()
        
        except pe.RestitutionCoefNotInRange as e:
            tk.messagebox.showerror("Erreur de fichier de configuration initial",f"{e}\nVeuillez vérifier si la valeur du coefficient de restitution dans le fichier de configuration\ncorrespond à l'intervalle permise.\nou choisir un autre fichier de configuration.")
            self.redefine_path()

        except pe.NoMainObject as e:
            tk.messagebox.showerror("Erreur de fichier de configuration initial",f"{e}\nLe fichier de configuration doit contenir au moins la ball principale.\nVeuillez vérifier si votre fichier de configuration est correctement formé\nou choisir un autre fichier de configuration.")
            self.redefine_path()

        except pe.MissingKey as e:
            tk.messagebox.showerror("Erreur de fichier de configuration initial",f"{e}\nVeuillez vérifier si votre fichier de configuration est correctement formé\nou choisir un autre fichier de configuration.")
            self.redefine_path()

        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite pendant l'initialisation: {e}\nVeuillez vérifier la légibilité du programme.")
            self.redefine_path()

if __name__ == "__main__":
    app = App()
    app.run()