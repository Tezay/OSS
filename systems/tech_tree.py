import json
import os

class TechTree:
    """
    # Classe pour gérer l'arbre technologique et sauvegarder son état dans un fichier JSON.
    """
    def __init__(self, template_path, default_data_path, output_dir):
        """
        Initialise la classe avec le chemin du modèle JSON et le répertoire de sortie.
        """
        # Charge les données du modèle et les sauvegarde dans un fichier nommé "tech_tree_state.json"
        self.template_path = template_path
        self.default_data_path = default_data_path
        self.output_dir = output_dir
        # Charge les données du modèle de la session locale de l'arbre tech
        self.session_data = self.get_tech_tree_session()
        # Charge les données par défaut de l'arbre tech
        self.default_data = self.get_tech_tree_default_data()
        self._save_to_file()
        

    def get_tech_tree_session(self):
        """
        Charge le fichier JSON modèle et retourne son contenu sous forme de dictionnaire.
        """
        with open(self.template_path, 'r') as file:
            return json.load(file)
        
    def get_tech_tree_default_data(self):
        with open(self.default_data_path, 'r') as file:
            return json.load(file)
    
    


    def _save_to_file(self):
        """
        Sauvegarde les données dans un fichier json dans le répertoire de sortie.
        """
        filename = "tech_tree_session.json"
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w') as file:
            json.dump(self.session_data, file, indent=4)
        print(f"Tech tree saved to {output_path}")

    def upgrade_module(self, module_name, inventory):
        """
        Améliore un module en activant le prochain tier disponible si les ressources nécessaires sont présentes.
        Retourne True si l'amélioration a été effectuée, False sinon.
        """
        if module_name not in self.session_data["tech_tree"]:
            raise ValueError(f"Module '{module_name}' does not exist in the tech tree.")

        tiers = self.session_data["tech_tree"][module_name]["tiers"]
        for tier, properties in tiers.items():
            if not properties["unlocked"]:
                # Vérifie les ressources nécessaires pour ce tier
                required_resources = self.default_data["tech_tree"][module_name]["tiers"][tier].get("required_resources", [])
                # Retourne True si toutes les ressources nécessaires sont présentes dans l'inventaire
                if all(inventory.has_item(resource["name"], resource["quantity"]) for resource in required_resources):
                    # Retire les ressources nécessaires de l'inventaire
                    for resource in required_resources:
                        if not inventory.remove_item(resource["name"], resource["quantity"]):
                            print(f"Failed to remove required resource '{resource['name']}' from inventory.")
                            return False
                    # Débloque le tier
                    properties["unlocked"] = True
                    self._save_to_file()
                    print(f"Upgraded {module_name} to {tier}.")
                    return True
                else:
                    print(f"Not enough resources to upgrade {module_name} to {tier}.")
                    return False
        print(f"All tiers for module '{module_name}' are already unlocked.")
        return False

    def possible_upgrade_module(self, module_name,tier, inventory):
        tiers = self.session_data["tech_tree"][module_name]["tiers"]
        for properties in tiers.items():
            if not properties[1]["unlocked"]:
                # Vérifie les ressources nécessaires pour ce tier
                required_resources = self.default_data["tech_tree"][module_name]["tiers"][tier].get("required_resources", [])
                # Retourne True si toutes les ressources nécessaires sont présentes dans l'inventaire
                if all(inventory.has_item(resource["name"], resource["quantity"]) for resource in required_resources):
                    return True
    