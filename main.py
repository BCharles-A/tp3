import tkinter as tk
import hud

class App:
    def __init__(self):
        self.default_path = "setting_default.json"
        self.main = None
    
    def file_not_found(self, e):
        tk.messagebox.showerror("Erreur", f"Fichier non trouvé: {e.filename}\nLe fichier est invalide ou manquant.\nVeuillez clicker sur OK pour changer le fichier de configuration initiale.")
        file_path = tk.filedialog.askopenfilename(title="Select a configuration file", filetypes=[("JSON files", "*.json")])
        if file_path != "":
            self.default_path = file_path
            self.run()

    def unexpected_error(self, e):
        tk.messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite pendant l'initialisation: {e}\nVeuillez vérifier la légibilité du programme.")

    def run(self):
        try:
            self.main = hud.HUD(self.default_path)
            self.main.launch()

        except FileNotFoundError as e:
            self.file_not_found(e)
        except Exception as e:
            self.unexpected_error(e)

if __name__ == "__main__":
    app = App()
    app.run()