import pygame
import os
import time


class SoundManager:
    """
    Classe gérant les sons et la musique du jeu.
    """
    def __init__(self, sound_folder="assets/sounds"):
        pygame.mixer.init()
        self.sound_folder = sound_folder
        self.sounds = {}
        self.music_volume = 0.5
        self.effect_volume = 0.5
        self.playing_sounds = {}

    def load_sound(self, name, filename):
        """
        Charge un son dans la mémoire.
        """
        path = os.path.join(self.sound_folder, filename)
        self.sounds[name] = pygame.mixer.Sound(path)
        self.sounds[name].set_volume(self.effect_volume)

    def play_sound(self, name, filename=None):
        """
        Joue un son.
        """
        # Récupère le temps actuel
        current_time = time.time()

        # Charge le son si il n'est pas déjà chargé
        if name not in self.sounds and filename:
            self.load_sound(name, filename)

        # Joue le son si il est chargé
        if name in self.sounds:
            sound = self.sounds[name]
            sound.play()
            self.playing_sounds[name] = {
                'sound': sound,
                'end_time': current_time + sound.get_length()
            }
        # Sinon affiche un message d'erreur
        else:
            print(f"Warning: '{name}' sound has not been loaded and no filename provided.")

    def stop_sound(self, name):
        """
        Arrête un son en cours de lecture.
        """
        # Vérifie si le son est en cours de lecture
        if name in self.playing_sounds:
            # Arrête le son si il est en cours de lecture
            self.playing_sounds[name]['sound'].stop()
            del self.playing_sounds[name]
        # Sinon affiche un message d'erreur
        else:
            print(f"Warning: '{name}' sound is not currently playing.")

    # Autres méthodes qui servirons plus tard si on veut ajouter de la musique etc

    def play_music(self, filename, loop=-1):
        path = os.path.join(self.sound_folder, filename)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_effect_volume(self, volume):
        self.effect_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)
