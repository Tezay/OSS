import json
import os
from config import DEFAULT_INVENTORY, ITEMS_LIST_PATH

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
        return DEFAULT_INVENTORY

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
        # Parcours les items de l'inventaire
        for item in self.data["items"]:
            # Si l'item existe déjà
            if item["name"] == item_name:
                # Incrémente la quantité
                item["quantity"] += quantity
                # Sauvegarde les modifications
                self._save_to_file()
                return
        # Si l'item n'existe pas, l'ajoute à l'inventaire
        self.data["items"].append({"name": item_name, "quantity": quantity})
        self._save_to_file()
    
    def debug_add_item(self, item_name):
        """
        Ajoute un item à l'inventaire ou incrémente sa quantité si l'item existe déjà.
        """
        # Parcours les items de l'inventaire
        for item in self.data["items"]:
            # Si l'item existe déjà
            if item["name"] == item_name:
                # Incrémente la quantité
                item["quantity"] += 999999
                # Sauvegarde les modifications
                self._save_to_file()
                return
        # Si l'item n'existe pas, l'ajoute à l'inventaire
        self.data["items"].append({"name": item_name, "quantity": 999999})
        self._save_to_file()

    def remove_item(self, item_name, quantity):
        """
        Retire une quantité d'un item de l'inventaire. Si la quantité devient 0 ou négative, l'item est supprimé.
        """
        # Parcours les item de l'inventaire
        for item in self.data["items"]:
            # Si le nom de l'item correspond
            if item["name"] == item_name:
                # Vérifie si la quantité est suffisante pour être retirée
                if item["quantity"] >= quantity:
                    # Retire la quantité de l'item
                    item["quantity"] -= quantity
                    # Si la quantité est devenue 0 ou négative, supprime l'item de l'inventaire
                    if item["quantity"] <= 0:
                        self.data["items"].remove(item)
                    # Sauvegarde les modifications
                    self._save_to_file()
                    print(f"Removed {quantity} of '{item_name}' from inventory.")
                    return True
                else:
                    print(f"Not enough '{item_name}' in inventory to remove {quantity}.")
                    return False
        print(f"Item '{item_name}' not found in inventory.")
        return False

    def get_inventory(self):
        """
        Renvoie l'entièreté de l'inventaire sous forme de liste.
        """
        return self.data["items"]

    def has_item(self, item_name, quantity):
        """
        Vérifie si l'inventaire contient un item avec une quantité suffisante.
        """
        # Parcours les items de l'inventaire
        for item in self.data["items"]:
            # Si le nom de l'item correspond ET quantité suffisante : renvoie True
            if item["name"] == item_name and item["quantity"] >= quantity:
                return True
        return False
    
    def get_items_data(self):
        """
        Renvoie un dictionnaire contenant les données des items possédés par le joueur.
        """
        # Charge les données complètes des items depuis le fichier ITEMS_LIST_PATH
        # Ajout de encoding='utf-8' pour assurer la lecture correcte des caractères spéciaux.
        with open(ITEMS_LIST_PATH, 'r', encoding='utf-8') as file:
            all_items_data = json.load(file)

        # Crée un dictionnaire pour stocker les données des items possédés
        items_data = {}

        # Parcours les items possédés par le joueur
        for owned_item in self.data["items"]:
            item_name = owned_item["name"]
            quantity = owned_item["quantity"]

            # Récupère les données complètes de l'item depuis le fichier
            if item_name in all_items_data:
                item_data = all_items_data[item_name]
                # Ajoute la quantité possédée à l'item
                item_data["quantity"] = quantity
                # Ajoute l'item au dictionnaire des items possédés
                items_data[item_name] = item_data

        return items_data


