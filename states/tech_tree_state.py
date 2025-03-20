import pygame
from buttons import*
from .base_state import BaseState
from session_data_manager import DataManager


data_manager = DataManager()
tech_tree_data = data_manager.tech_tree.get_tech_tree_tiers_data()
#print("tech_tree_data",tech_tree_data)

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
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
        screen.fill((0, 0, 0))
        grille(True)

        # Dessin des boutons relatifs à l'état tech_tree_state (avec la méthode .draw() de la classe Button)

        mouse=pygame.mouse.get_pos()


        draw_buttons("return")
        
        draw_buttons("defenses_T0")
        draw_buttons("defenses_T1")
        draw_buttons("defenses_T2")
    
        list={}
        for i in tech_tree_data:
            for j in tech_tree_data[i]:
                txt=i+"_"+j
                list[txt]=[]
                draw_buttons(txt)
                txt_2=""
                for k in tech_tree_data[i][j]:
                    for l in k:
                        if l=="\n":
                            txt_2+="\n"
                        else:
                            txt_2+=l
                    #print("txt_2",txt_2)
                list[txt]=txt_2
        
        #print("list",list["terraforming_tier_1"])
        #print("list",list)
        
        for i in list:
            txt=""
            for j in list[i]:
                txt+=j
            if colide_button(i,mouse):
                colide_draw(i,txt,mouse)

        ########### TEST ############
        # Exemple de bouton pour tester l'upgrade d'un module du tech tree
        #draw_buttons("test_upgrade_tech_tree_module")
        #############################