import pygame

from gui.buttons import *
from .base_state import BaseState
import json

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
            
        
                        


            unlocked_tiers=self.game.data_manager.tech_tree.session_data
            #print("unlocked_tiers",unlocked_tiers["tech_tree"])

            
            for module in unlocked_tiers["tech_tree"]:
                #print("module",module)
                for tier in unlocked_tiers["tech_tree"][module]["tiers"]:
                    #print("tier",tier)
                    txt=module+"_"+tier
                    if click_button(txt,pos):
                        if int(tier[5])!=0:
                            verif_tier=tier[:4]+"_"+str(int(tier[5])-1)
                        else:
                            verif_tier=tier

                        print("click",txt)
                        print("avant",verif_tier)
                        #print("verif_tier",verif_tier)
                        #print("verif_tier[5]",verif_tier[5])
                        if int(verif_tier[5])==int(tier[5])-1:
                            if unlocked_tiers["tech_tree"][module]["tiers"][tier]["unlocked"]==False and unlocked_tiers["tech_tree"][module]["tiers"][verif_tier]["unlocked"]==True:
                                inventory = self.game.data_manager.inventory
                                self.game.data_manager.tech_tree.upgrade_module(module,inventory)
                    txt=""


            
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

        unlocked_tiers=self.game.data_manager.tech_tree.session_data

        #print(unlocked_tiers)

        #print("unlocked_tiers",unlocked_tiers["tech_tree"]["ship_engine"])

        
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

        size=custom_size(10,2)

        draw_buttons("return")
        #boutons qui n'existe aps encore dans le json arbre de technologie
        """draw_buttons("defenses_T0")
        draw_buttons("defenses_T1")
        draw_buttons("defenses_T2")"""

        draw_size_buttons("defenses_T0",5,15,size)
        draw_size_buttons("defenses_T1",5,18,size)
        draw_size_buttons("defenses_T2",5,21,size)

        
        tech_tree_data_button={}
        #extraire le module
        for module in tech_tree_data:
            #extraire les tiers
            for tier in tech_tree_data[module]:
                #txt deviens le nom du bouton a appeler pour dessiner le bouton (Classe Button)
                txt=module+"_"+tier
                if int(tier[5])!=0:
                    save_tier=tier[:4]+"_"+str(int(tier[5])-1)
                else:
                    save_tier=tier
                #print("save_tier",save_tier)
                inventory = self.game.data_manager.inventory
                if unlocked_tiers["tech_tree"][module]["tiers"][tier]["unlocked"]==True:
                    draw_size_buttons(txt,buttons[txt]["x"],buttons[txt]["y"],size,color=(0,255,0))
                    #print("moduleeeeeeeeee",module)
                elif tech_tree_data[module][tier]["unlocked"]==False and tech_tree_data[module][save_tier]["unlocked"]==True and self.game.data_manager.tech_tree.possible_upgrade_module(module,tier,inventory):
                    draw_size_buttons(txt,buttons[txt]["x"],buttons[txt]["y"],size,color=(255,255,0))
                    #sinon on dessine le bouton en rouge
                else:
                    draw_size_buttons(txt,buttons[txt]["x"],buttons[txt]["y"],size,color=(255,0,0))
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
            colide_draw(name,txt,mouse,size)
            #if click_button(name):





        ########### TEST ############
        # Exemple de bouton pour tester l'upgrade d'un module du tech tree
        #draw_buttons("test_upgrade_tech_tree_module")
        #############################