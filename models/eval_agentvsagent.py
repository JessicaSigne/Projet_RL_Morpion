import matplotlib.pyplot as plt
from src.environnement import TicTacToeEnv
from src.agent import QLearningAgent
import random

def evaluate_self_play():
    env = TicTacToeEnv()
    
    # On crée deux instances du même "cerveau"
    agent_x = QLearningAgent()
    agent_o = QLearningAgent()
    
    # On charge le même fichier de connaissances pour les deux
    try:
        agent_x.load("morpion_qtable.pkl")
        agent_o.load("morpion_qtable.pkl")
        print("Modèles chargés pour X et O.")
    except FileNotFoundError:
        print("Erreur : Fichier pkl introuvable.")
        return

    # Epsilon à 0 : on veut la performance maximale sans hasard [cite: 88]
    agent_x.epsilon = 0
    agent_o.epsilon = 0
    
    num_games = 200
    stats = {"Victoires X": 0, "Victoires O": 0, "Nuls": 0}

    for _ in range(num_games):
        state = env.reset()
        done = False
        
        while not done:
            # Choix de l'agent en fonction du joueur courant
            current_agent = agent_x if env.current_player == 1 else agent_o
            
            legal_actions = env.legal_actions()
            action = current_agent.act(state, legal_actions)
            
            state, reward, done = env.step(action)
            
            if done:
                if reward == 1:
                    # Le joueur qui vient de jouer a gagné
                    if env.current_player == 1: stats["Victoires X"] += 1
                    else: stats["Victoires O"] += 1
                else:
                    stats["Nuls"] += 1

    # --- AFFICHAGE DES RÉSULTATS ---
    print(f"\n--- Évaluation Self-Play ({num_games} parties) ---")
    for key, value in stats.items():
        print(f"{key}: {value} ({(value/num_games)*100:.1f}%)")

    # --- GÉNÉRATION DU DIAGRAMME ---
    names = list(stats.keys())
    values = list(stats.values())
    
    plt.figure(figsize=(8, 6))
    # Couleurs : Bleu pour X, Violet pour O, Gris pour Nul
    plt.bar(names, values, color=['#3498db', '#9b59b6', '#95a5a6'])
    
    plt.title(f"Résultats Self-Play : IA vs IA ({num_games} parties)")
    plt.ylabel("Nombre de parties")
    
    # Ajout des étiquettes de données sur les barres
    for i, v in enumerate(values):
        plt.text(i, v + 2, str(v), ha='center', fontweight='bold')

    plt.savefig("eval_self_play.png")
    print("\nGraphique sauvegardé sous 'eval_self_play.png'.")
    plt.show()

if __name__ == "__main__":
    evaluate_self_play()