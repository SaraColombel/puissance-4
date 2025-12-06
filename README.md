# Présentation

Ce projet est un bot de jeu Puissance 4 avec interface graphique, capable de battre n'importe quel humain.
L’objectif est d’offrir une IA capable d’analyser l’état du plateau, de prédire les coups dangereux et d’optimiser ses actions pour gagner ou empêcher l’adversaire de gagner.

# Fonctionnalités
  - Vérification des coups valides
  - Placement des jetons
  - Évaluation du plateau pour choisir le meilleur coup
  - Possibilité de jouer contre l’IA.

# Algorithme utilisé
Le bot s’appuie sur :
  - Minimax avec élagage alpha-bêta
  - Prise en compte de plusieurs tours d’avance
  - Simulation de coups sur un grille fictive
  - Optimisation du calcul grâce à l’élagage des branches inutiles
  - Fonction d’évaluation du plateau pour guider l’IA

# Installation & lancement
  1. Cloner le projet
    - git clone https://github.com/mon-projet/puissance4-bot.git
    - cd puissance4-bot

  2. Lancer une partie
    - python3 puissance4_gui.py

ou : Lancer puissance4.exe
