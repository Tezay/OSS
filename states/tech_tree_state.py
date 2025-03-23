import pygame

from gui.buttons import *
from .base_state import BaseState


# Classe enfant de BaseState
# Méthodes utilisées :
# - handles_event : surveille les événements (touches clavier)
# - update : update la logique relative à l'état en cours
# - draw : déssine l'état courant
class TechTreeState(BaseState):
    def __init__(self, state_manager,game):
        super().__init__()
        self.state_manager = state_manager
        self.game=game


    def handle_event(self, event, pos):
        if event.type == pygame.KEYDOWN:
            
            if event.key == KEY_BINDINGS["exit_current_menu"]:
                from .game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)

    def update(self, dt, actions, pos, mouse_clicked):
        
        # Récupération des coordonnées de la souris dans un tuple
        mouse_x, mouse_y = pos


        # Vérification du clique de la souris sur le bouton
        if mouse_clicked:
            if click_button("return",pos):
                from states.game_state import GameState
                # On passe existing_game=self.game pour réutiliser l’instance
                new_game_state = GameState(self.state_manager, existing_game=self.game)
                # Change l'état courant à GameState
                self.state_manager.set_state(new_game_state)
            
            if click_button("ship_engine_tier_1",pos):
                inventory = self.game.data_manager.inventory
                self.game.data_manager.tech_tree.upgrade_module("ship_engine",inventory)
            
            ########### TEST ############
            # Exemple de bouton pour tester l'upgrade d'un module du tech tree
            if click_button('test_upgrade_tech_tree_module',pos):
                inventory = self.game.data_manager.inventory
                self.game.data_manager.tech_tree.upgrade_module("terraforming",inventory)
            #############################

    def draw(self, screen,pos):

        # Dessiner le jeu "en fond"
        self.game.draw(screen)
        # Dessiner l'overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))


        grille(True)


        unlocked_tiers = self.game.data_manager.tech_tree.get_tech_tree_session()
        
        data=self.game.data_manager.tech_tree.get_tech_tree_default_data()
        tech_tree_data={}

        #extraire les modules
        for module in data["tech_tree"]:
            #extraire les tiers
            tech_tree_data[module]={}
            for tier in data["tech_tree"][module]["tiers"]:
                tech_tree_data[module][tier]={}
                txt=""
                #extraire la description
                for description in data["tech_tree"][module]["tiers"][tier]["description"]:
                    txt+=description
                #extraire le booleen qui sert a savoir si la technologie est debloquer ou pas
                unlocked=unlocked_tiers["tech_tree"][module]["tiers"][tier]["unlocked"]
                #mettre la description et le booleen pour savoir si la technologie est debloquer ou pas
                tech_tree_data[module][tier]={"description":txt,"unlocked":unlocked}

        
            
        #print("tech_tree_data",tech_tree_data)


        


        # Dessin des boutons relatifs à l'état tech_tree_state (avec la méthode .draw() de la classe Button)

        mouse=pygame.mouse.get_pos()


        draw_buttons("return")
        #boutons qui n'existe aps encore dans le json arbre de technologie
        draw_buttons("defenses_T0")
        draw_buttons("defenses_T1")
        draw_buttons("defenses_T2")
    
        tech_tree_data_button={}
        #extraire le module
        for module in tech_tree_data:
            #extraire les tiers
            for tier in tech_tree_data[module]:
                #txt deviens le nom du bouton a appeler pour dessiner le bouton (Classe Button)
                txt=module+"_"+tier
                draw_buttons(txt)
                tech_tree_data_button[txt]=[]
                txt_2=""
                #faire en sorte que les sauts de lignes soit bien pris en conte.
                for text in tech_tree_data[module][tier]["description"]:
                    for letre in text:
                        if letre=="\n":
                            txt_2+="\n"
                        else:
                            txt_2+=letre
                #remettre les bon textes avec les sauts de lignes
                tech_tree_data_button[txt]=txt_2
        
        #print("tech_tree_data",tech_tree_data["terraforming_tier_1"])
        #print("tech_tree_data_button",tech_tree_data_button)
        
        #extraire ce qui va etre afficher dans l'overlay
        for name in tech_tree_data_button:
            txt=""
            for tier in tech_tree_data_button[name]:
                txt+=tier
            #quand la souris touche les boutons, l'overlay aves les info sur la technologie s'affiche
            if colide_button(name,mouse):
                colide_draw(name,txt,mouse)
                #if click_button(name):


        ########### TEST ############
        # Exemple de bouton pour tester l'upgrade d'un module du tech tree
        #draw_buttons("test_upgrade_tech_tree_module")
        #############################