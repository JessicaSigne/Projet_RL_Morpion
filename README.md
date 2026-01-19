# Projet_Morpion_Complet

=======
# 🎮 Morpion avec Apprentissage par Renforcement (Q-Learning)

## 👤 Auteur
**Jessica SIGNE**  
📧 Email : jessicasigne44@gmail.com  
📅 Date : Janvier 2026 
GitHub : https://github.com/JessicaSigne/Projet_RL_Morpion.git
---

## 📋 Description du Projet

Ce projet implémente un jeu de **Morpion (Tic-Tac-Toe)** avec trois modes de jeu différents, incluant un agent intelligent entraîné par **apprentissage par renforcement** (Q-Learning). L'objectif est de construire une architecture propre séparant le jeu de l'agent pour permettre un apprentissage efficace, créer des agents capables de jouer de manière optimale en utilisant des techniques d'IA avancées.


### 🎯 Objectifs Pédagogiques

1. **Comprendre l'apprentissage par renforcement** : Implémentation de l'algorithme Q-Learning
2. **Optimisation des hyperparamètres** : Alpha, gamma, epsilon, reward shaping
3. **Architecture logicielle** : Séparation Environnement / Agent / Evaluation /Interface
4. **Évaluation rigoureuse** : Métriques de performance et convergence

### 🎯 Architecture du Code

```src/environnement.py``` : Gère les règles du plateau 3x3, les coups légaux et la détection de victoire/nul.
```src/agent.py``` : Contient la logique du Q-learning, la table $Q(s,a)$ et la politique $\epsilon$-greedy.
```models/entrainement_agent.py``` : Gère la boucle d'épisodes et la décroissance de l'epsilon. 
```models/eval_agentvsrandom.py``` : Gère l'évaluation agent vs un agent aléatoire
```models/eval_agentvsagent.py``` : Gère l'évaluation agent vs agent (Self-Play) 
```src/interface.py``` : Interface graphique Pygame (Thème Violet) pour le jeu interactif.

---

## 🏗️ Architecture du Projet

Le projet est structuré en **3 programmes indépendants** :

```
PROJET_MORPION_COMPLET/
├── models/
│   ├── entrainement_agent.py   # Boucle d'entraînement + plots
│   ├── eval_agentvsagent.py    # Évaluation Self-Play
│   └── eval_agentvsrandom.py   # Évaluation vs Aléatoire
├── src/
│   ├── agent.py                # Classe QLearningAgent
│   ├── environnement.py        # Logique TicTacToeEnv
│   └── interface.py            # GUI Pygame (Violet Theme)
├── main.py                     # Point d'entrée principal
├── requirements.txt            # Liste des librairies
└── README.md                   # Documentation
```

---
### Création
```python -m venv venv```

#### Activation
##### Windows :
```venv\Scripts\activate```

##### Mac/Linux :
```source venv/bin/activate```

## ⚙️ Installation

### Prérequis
- **Python 3.8+**
- **Système d'exploitation** : Windows, macOS, Linux

### Installer les Dépendances
```bash
pip install -r requirements.txt
```

## 🎮 Utilisation 📈 Entraînement

Pour entraîner l'agent et générer les graphiques de performance :```python -m models.entrainement_agent```

```Paramètres optimaux :``` 70 000 épisodes, $\alpha=0.1$, $\gamma=0.95$. 9Résultat : Génère le fichier ```morpion_qtable.pkl``` et les courbes d'apprentissage.

## 📊 Évaluation (Modes automatiques)

*VS Aléatoire :* ```python -m models.eval_agentvsrandom``` (Vérifie le taux de victoire). 

*VS Agent (Self-Play) :* ```python -m models.eval_agentvsagent``` (Vérifie l'équilibre de Nash).

## 🎮 Interface Pygame
Pour lancer le jeu avec le menu interactif : ```python main.py```


### **Mode 1 : Humain vs Humain**

### **Mode 2 : Humain vs Agent IA**

### **Mode 3 : Agent vs Agent (Self-Play), Visualisation accélérée**


## 📈 Résultats

*Apprentissage :* L'agent atteint une convergence vers un taux de victoire de ```~82%``` contre un joueur aléatoire.


*Défense :* En utilisant une punition de défaite forte ```(-5)```, l'agent a atteint ```100%``` de matchs nuls en mode Self-Play. 


*Exploration :* La décroissance progressive d'Epsilon a permis une couverture optimale des états du plateau.


## 📈 Visualisations et Analyse des Performances

Le projet génère automatiquement une série de graphiques permettant de valider l'apprentissage de l'IA.

### 🧠 Suivi de l'Entraînement
*Progression de l'IA :* Le graphique ```performance_win_rate.png``` montre l'augmentation du taux de victoire au fil des épisodes.

*Stabilité du modèle :* On observe sur ```performance_win_rate.png``` que la courbe atteint un plateau, signe que l'agent a fini d'apprendre.

*Transition stratégique :* Le fichier ```epsilon_decay.png``` illustre le passage d'une phase de pure exploration à une phase d'expertise (exploitation).

*Gestion de la curiosité :* La courbe ```epsilon_decay.png``` confirme que l'agent ne joue plus au hasard à la fin de l'entraînement.

### 📊 Évaluation contre un joueur Aléatoire
*Domination tactique :* L'histogramme ```eval_aleatoire.png``` affiche le nombre massif de victoires de l'IA face à des coups imprévisibles.

*Robustesse défensive :* Le graphique ```eval_aleatoire.png``` permet de visualiser le très faible nombre de défaites subies par l'agent.

*Gestion des erreurs :* On voit sur ```eval_aleatoire.png``` que l'IA sait punir les erreurs adverses tout en évitant les pièges simples.

### ⚔️ Évaluation en Self-Play (Agent vs Agent)
*Atteinte de l'optimum :* Le graphique ```eval_agentvsagent.png``` montre que 100% des parties se terminent désormais par un match nul.

*Équilibre de Nash :* L'image ```eval_agentvsagent.png```  prouve qu'aucun des deux agents (X ou O) ne peut plus prendre l'avantage sur l'autre.

*Symétrie des forces :* On constate sur ```eval_agentvsagent.png``` l'absence totale de victoires pour X ou O, confirmant une défense parfaite.
---

## 🚀 Améliorations Futures

### 🛠️ Court terme

*Niveaux de difficulté :* Intégrer un sélecteur permettant de jouer contre une IA "Débutante" (Epsilon élevé) ou "Experte" (Epsilon = 0).

*Historique local :* Sauvegarder les statistiques des sessions de jeu (victoires/défaites de l'utilisateur) dans un fichier JSON ou CSV.

*Animations Pygame :* Ajouter des effets de transition fluides lors de l'apparition des X et des O sur la grille.

### 🧠 Long terme (IA Avancée)Deep Q-Learning (DQN) 

Remplacer la Q-Table par un réseau de neurones avec PyTorch ou TensorFlow pour gérer des jeux plus complexes.Généralisation au ```Puissance 4``` : Adapter l'environnement pour une grille de $7 \times 6$, nécessitant une gestion plus fine de l'espace des états.AlphaZero-style : Implémenter un algorithme de recherche arborescente ```Monte Carlo (MCTS)``` combiné à un réseau de neurones pour une IA imbattable sur n'importe quelle taille de grille.

---

## 📄 Licence

Ce projet est réalisé dans un cadre pédagogique.  
Tous droits réservés © 2026 Jessica SIGNE

---

## 📞 Contact

**Jessica SIGNE**  
📧 jessicasigne44@gmail.com

Pour toute question sur le projet, l'implémentation ou les résultats, n'hésitez pas à me contacter !

---

## 🙏 Remerciements

- **Professeur** : Pour l'encadrement et les conseils
- **Anthropic** : Pour Claude AI (assistance au développement)
- **Communauté Python** : Pygame, NumPy, Matplotlib

---
>>>>>>> 8674ba8 (Initial commit)
