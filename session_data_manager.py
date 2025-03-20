import os
from datetime import datetime
from config import LOCAL_DATA_PATH, TECH_TREE_DEFAULT_DATA_PATH, TECH_TREE_TEMPLATE_PATH
from tech_tree import TechTree
from inventory import Inventory

class DataManager:
    """
    Classe pour gérer les données du jeu et créer un dossier unique pour chaque session.
    """
    def __init__(self):
        """
        Initialise la classe avec le répertoire de base où les dossiers seront créés
        """
        # Crée un nouveau dossier pour la session de jeu
        self.base_dir = LOCAL_DATA_PATH
        self.folder_path = self._create_game_session_folder()
        # Créer l'objet tech_trees
        self.tech_tree = TechTree(TECH_TREE_TEMPLATE_PATH, TECH_TREE_DEFAULT_DATA_PATH, self.folder_path)
        # Créer l'objet inventory
        self.inventory = Inventory(self.folder_path)

    def _create_game_session_folder(self):
        """
        Crée un dossier unique basé sur la date et l'heure actuelles"
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_name = f"data_{timestamp}"
        folder_path = os.path.join(self.base_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created at {folder_path}")
        return folder_path
    
    def get_tech_tree_data(self):
        return self.tech_tree.get_tech_tree_tiers_data()
