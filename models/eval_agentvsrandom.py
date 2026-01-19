from src.environnement import TicTacToeEnv
from src.agent import QLearningAgent
import matplotlib.pyplot as plt
import random

def plot_results(stats, title, filename):
    """Crée un graphique en barres pour visualiser les performances."""
    names = list(stats.keys())
    values = list(stats.values())
    
    # Choix des couleurs : Vert pour Victoire, Rouge pour Défaite, Gris pour Nul
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']
    
    plt.bar(names, values, color=colors)
    plt.title(title)
    plt.ylabel('Nombre de parties')
    
    # On ajoute le nombre exact au-dessus de chaque barre
    for i, v in enumerate(values):
        plt.text(i, v + 1, str(v), ha='center', fontweight='bold')
    
    plt.savefig(filename)
    print(f"Graphique sauvegardé sous : {filename}")
    plt.close() # Ferme le graphique pour libérer la mémoire

def evaluate():
    env = TicTacToeEnv()
    agent = QLearningAgent()
    
    try:
        agent.load("morpion_qtable.pkl")
    except FileNotFoundError:
        print("Erreur : Entraînez l'IA d'abord !")
        return

    agent.epsilon = 0 
    num_games = 200
    stats = {"Victoires": 0, "Défaites": 0, "Nuls": 0}

    for _ in range(num_games):
        state = env.reset()
        done = False
        while not done:
            # Tour IA
            action = agent.act(state, env.legal_actions())
            state, reward, done = env.step(action)
            if done:
                if reward == 1: stats["Victoires"] += 1
                else: stats["Nuls"] += 1
                break
            
            # Tour Aléatoire
            opp_action = random.choice(env.legal_actions())
            state, opp_reward, done = env.step(opp_action)
            if done:
                if opp_reward == 1: stats["Défaites"] += 1
                else: stats["Nuls"] += 1

    # Affichage texte et graphique
    print(stats)
    plot_results(stats, "Performance de l'IA contre un joueur Aléatoire", "eval_aleatoire.png")

if __name__ == "__main__":
    evaluate()