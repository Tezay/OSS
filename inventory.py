import json
import os

class Inventory:
    """
    Classe pour gérer l'inventaire et sauvegarder son état dans un fichier JSON.
    """
    def __init__(self, output_dir):
        """
        Initialise la classe avec le répertoire de sortie
        """
        # Crée un fichier nommé "inventory.json" avec une structure par défaut
        self.output_dir = output_dir
        self.data = self._initialize_inventory()
        self._save_to_file()

    def _initialize_inventory(self):
        """
        # Initialise l'inventaire avec un item par défaut (pour le test)
        """
        return {"items": [{"name": "water", "quantity": 5}]}

    def _save_to_file(self):
        """
        Sauvegarde les données dans un fichier dans le répertoire de sortie
        """
        filename = "inventory.json"
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w') as file:
            json.dump(self.data, file, indent=4)
        print(f"Inventory saved to {output_path}")

    def add_item(self, item_name, quantity):
        """
        Ajoute un item à l'inventaire ou incrémente sa quantité si l'item existe déjà.
        """
        for item in self.data["items"]:
            if item["name"] == item_name:
                item["quantity"] += quantity
                self._save_to_file()
                return
        self.data["items"].append({"name": item_name, "quantity": quantity})
        self._save_to_file()

    def remove_item(self, item_name, quantity):
        """
        Retire une quantité d'un item de l'inventaire. Si la quantité devient 0 ou négative, l'item est supprimé.
        """
        for item in self.data["items"]:
            if item["name"] == item_name:
                item["quantity"] -= quantity
                if item["quantity"] <= 0:
                    self.data["items"].remove(item)
                self._save_to_file()
                return
        print(f"Item '{item_name}' not found in inventory.")

    def get_inventory(self):
        """
        Renvoie l'entièreté de l'inventaire.
        """
        return self.data["items"]
