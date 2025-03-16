import json
import os

class TechTree:
    """
    # Classe pour gérer l'arbre technologique et sauvegarder son état dans un fichier JSON.
    """
    def __init__(self, template_path, output_dir):
        """
        Initialise la classe avec le chemin du modèle JSON et le répertoire de sortie.
        """
        # Charge les données du modèle et les sauvegarde dans un fichier nommé "tech_tree_state.json"
        self.template_path = template_path
        self.output_dir = output_dir
        self.data = self.get_tech_tree_state()
        self._save_to_file()

    def get_tech_tree_state(self):
        """
        # Charge le fichier JSON modèle et retourne son contenu sous forme de dictionnaire.
        """
        with open(self.template_path, 'r') as file:
            return json.load(file)

    def _save_to_file(self):
        """
        Sauvegarde les données dans un fichier json dans le répertoire de sortie.
        """
        filename = "tech_tree_state.json"
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w') as file:
            json.dump(self.data, file, indent=4)
        print(f"Tech tree saved to {output_path}")
