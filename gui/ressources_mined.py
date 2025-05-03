import pygame
import math
from states.game_state import GameState
from core.json_manager import *

from config import *


class RessourcesMined():
    def __init__(self,game):
        self.planets=game.planets
    
    def get_planet_with_mines(self):
        list_planets_with_mines = []
        for i in self.planets:
            if i.mines:
                list_planets_with_mines.append(i)
        return list_planets_with_mines                      #retourne une liste avec toutes les plantes avec des mines

    def update(self):
        planets_with_mines=self.get_planet_with_mines()
        ressources=[]
        if len(planets_with_mines)==0:
            # Test d'Edouard
            # print("aucune planette avec des mines")
            pass
        else:
            for planet in planets_with_mines:
                ressources=[]
                planet_info=planet.planet_type
                planet_data=get_planet_data(planet_info)
                for ressource in planet_data["available_ressources"]:
                    ressources.append(ressource)                            #donne les ressources de la planette et leur quantité
                    print(ressources)
            


        #print("ici",self.planets)


    def draw(self, screen, pos):
        # Dessiner le jeu "en fond"
        self.game.draw(screen)
