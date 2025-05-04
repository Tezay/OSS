# OSS - Orbital Space Simulator

## Description

OSS (Orbital Space Simulator) est un jeu de simulation et d'exploration spatiale en 2D développé en Python avec la bibliothèque Pygame. Le joueur contrôle le dernier vaisseau spatial de l'humanité, chargé de trouver une nouvelle planète habitable après la destruction de la Terre. Le jeu propose une génération procédurale de carte, une physique newtonienne pour le mouvement du vaisseau, la collecte de ressources, un arbre technologique et un système d'inventaire.

## Guide d'installation

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/Tezay/OSS.git
    cd OSS
    ```
2.  **Créez un environnement virtuel (recommandé) :**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sous Windows, utilisez `venv\Scripts\activate`
    ```
3.  **Installez les dépendances :**
    Assurez-vous que Python et pip sont installés. Ensuite, exécutez la commande suivante à la racine du projet :
    ```bash
    pip install -r requirements.txt
    ```
    Cela installera Pygame, la seule dépendance externe.

## Comment lancer le jeu

Naviguez jusqu'au répertoire racine du projet dans votre terminal et exécutez :

```bash
python main.py
```

## Structure du Projet

```
OSS/
│
├── assets/             # Contient tous les assets du jeu (images, polices, sons)
│   ├── fonts/
│   ├── hud/
│   ├── planets/
│   ├── spaceships/
│   └── ... (autres types d'assets)
│
├── config.py           # Variables de configuration globales (taille écran, constantes physiques, raccourcis clavier, chemins, définitions des boutons)
│
├── core/               # Logique principale du jeu et gestionnaires
│   ├── game.py         # Classe principale du jeu gérant les entités, la caméra, les mises à jour du monde et le dessin
│   ├── input_manager.py # Gère les entrées utilisateur et les actions
│   ├── json_manager.py # Fonctions utilitaires pour lire les données des fichiers JSON (planètes, dialogues)
│   ├── session_data_manager.py # Gère la persistance des données pour une session de jeu (inventaire, état de l'arbre technologique)
│   └── sound_manager.py # Gère le chargement et la lecture des sons/musiques
│
├── data/               # Fichiers de données du jeu (format JSON)
│   ├── dialogues.json  # Séquences de dialogues pour les tutoriels, etc.
│   ├── items_list.json # Définitions et propriétés de tous les objets du jeu
│   ├── planets.json    # Définitions et propriétés des différents types de planètes
│   ├── tech_tree_data.json # Données par défaut et structure de l'arbre technologique
│   └── tech_tree_session_template.json # Modèle pour la progression du joueur dans l'arbre technologique
│
├── entities/           # Entités du jeu
│   └── spaceship.py    # Classe définissant le vaisseau du joueur (physique, carburant, textures)
│
├── gui/                # Éléments de l'interface utilisateur graphique
│   ├── buttons.py      # Fonctions et logique pour créer et gérer les boutons
│   ├── hud.py          # Classe de l'affichage HUD (affiche vitesse, carburant, mini-carte, dialogues, infos atterrissage)
│   └── ressources_mined.py
│
├── local_data/         # Répertoire créé à l'exécution pour stocker les données spécifiques à la session (inventaire, état de l'arbre technologique)
│
├── states/             # Différents états du jeu (menus, jeu, paramètres, etc.)
│   ├── base_state.py   # Classe de base abstraite pour tous les états
│   ├── game_state.py   # État principal du jeu
│   ├── menu_state.py   # État du menu principal
│   ├── inventory_state.py # État de l'écran d'inventaire
│   ├── tech_tree_state.py # État de l'écran de l'arbre technologique
│   ├── settings_state/ # Sous-répertoire pour les états du menu des paramètres
│   │   ├── settings_menu_state.py
│   │   └── ... (autres sous-états des paramètres)
│   └── ... (autres états comme game_over, credits, etc.)
│
├── systems/            # Systèmes du jeu comme l'inventaire, l'arbre technologique, la gestion des ressources
│   ├── inventory.py    # Classe de gestion de l'inventaire
│   ├── planet_resources.py # Fonctions liées aux ressources des planètes (collecte, chargement d'images)
│   └── tech_tree.py    # Classe de gestion de l'arbre technologique
│
├── world/              # Génération du monde et logique de la caméra
│   ├── camera.py       # Classe de la caméra pour gérer la vue du jeu (suivi, zoom, panoramique)
│   └── map_generator.py # Génération procédurale de la carte du jeu (étoiles, planètes)
│
├── main.py             # Point d'entrée principal de l'application, gère la boucle de jeu et les transitions d'état
├── requirements.txt    # Liste les dépendances des packages Python
└── README.md
```

## Fonctionnalités Clés

*   **Génération Procédurale de Carte :** Le monde du jeu (étoiles et planètes) est généré de manière procédurale basé sur une graine (seed), assurant une expérience unique à chaque fois (ou répétable avec une graine fixe).
*   **Physique Newtonienne :** Le mouvement du vaisseau spatial est régi par une physique newtonienne simplifiée, incluant les forces gravitationnelles des planètes, la poussée et la rotation. La prédiction de trajectoire est également implémentée.
*   **Gestion des États :** Le jeu utilise un `StateManager` pour gérer différents écrans comme le menu principal, le jeu, l'inventaire, l'arbre technologique et les paramètres, permettant une interface utilisateur et un flux de jeu modulaires.
*   **Arbre Technologique :** Les joueurs peuvent débloquer des améliorations pour leur vaisseau et leurs capacités via un arbre technologique, nécessitant des ressources spécifiques trouvées dans le monde du jeu. La progression est sauvegardée par session.
*   **Système d'Inventaire :** Les joueurs collectent des ressources sur les planètes, qui sont stockées dans un inventaire. Ces ressources sont utilisées pour l'artisanat ou le déblocage de technologies. L'état de l'inventaire est sauvegardé par session.
*   **Gestion des Ressources :** Les planètes possèdent des ressources spécifiques qui se régénèrent avec le temps, à la fois lorsque le joueur est posé et lorsqu'il est absent (calcul de la progression hors ligne au retour).
*   **Système de craft :** Les joueurs peuvent assembler les items de leur inventaire afin d'en créer de nouveaux, avec un système de craft intégré. La liste des crafts disponible est stockée dans un fichier JSON.
*   **HUD Dynamique :** L'HUD fournit des informations en temps réel sur l'état du vaisseau (position, vitesse, niveaux de carburant), une mini-carte, des indicateurs de force directionnelle et des informations contextuelles (messages d'atterrissage, invites de collecte de ressources, dialogues).
*   **Persistance de Session :** La progression clé du joueur, comme le contenu de l'inventaire et les technologies débloquées, est sauvegardée dans un dossier unique dans `local_data/` pour chaque session de jeu.

## Touches Clavier (Par Défaut)

*   **Déplacer Vaisseau (Poussée) :** `ESPACE`
*   **Rotation Gauche :** `Q`
*   **Rotation Droite :** `D`
*   **Décélérer (Debug) :** `Maj Droite`
*   **Arrêt instantané (Debug) :** `0` (Pavé numérique)
*   **Inventaire :** `I`
*   **Carte :** `M`
*   **Arbre Technologique :** (Bouton sur l'HUD)
*   **Paramètres (En Jeu) :** `Échap` ou Bouton Paramètres sur l'HUD
*   **Quitter Menu Actuel :** `Échap`
*   **Confirmer Dialogue :** `Entrée`
*   **Déplacer caméra dans la map :** Touches Fléchées
*   **Zoom (Debug) :** `Z` (Zoom Avant), `X` (Zoom Arrière)

*(Note : Vérifiez `config.py` pour les raccourcis les plus à jour)*
