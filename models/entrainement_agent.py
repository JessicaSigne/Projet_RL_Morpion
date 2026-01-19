import matplotlib.pyplot as plt
import random
from src.environnement import TicTacToeEnv
from src.agent import QLearningAgent

def train():
    env = TicTacToeEnv()
    agent = QLearningAgent(alpha=0.2, gamma=0.95, epsilon_max=1.0, epsilon_min=0.01, decay=0.99992)
    
    num_episodes = 70000 
    
    # Listes pour le suivi
    epsilon_history = []
    win_history = []  # Contiendra des victoires, défaites et nuls
    
    print("Entraînement en cours...")

    # --- PARAMÈTRES OPTIMAUX POUR LE NUL ---
    # Récompense Victoire : +1
    # Récompense Défaite : -5 (Punition très forte pour forcer la défense)
    # Récompense Nul : +0.5 (On encourage l'IA à préférer le nul à la prise de risque)

    for episode in range(num_episodes):
        state = env.reset()
        done = False
        won = 0 # <--- ON INITIALISE À 0
        history = [] # Pour se souvenir du coup précédent et le punir si besoin
        
        while not done:
            legal_actions = env.legal_actions()
            action = agent.act(state, legal_actions)
            
            # On sauvegarde l'état actuel avant de jouer
            current_state = state
            state, reward, done = env.step(action)
            
            if done:
                if reward == 1: # Quelqu'un a gagné (X ou O)
                    won = 1 # <--- ON ENREGISTRE LA VICTOIRE POUR LE GRAPH
                    # 1. On donne +1 au vainqueur
                    agent.learn(current_state, action, 1, state, True, [])
                    
                    # 2. ON PUNIT LE PERDANT (C'est le secret du 100% nul)
                    if history:
                        prev_s, prev_a = history[-1]
                        agent.learn(prev_s, prev_a, -5, current_state, True, [])
                else:
                    # MATCH NUL : On donne un petit bonus pour encourager la sécurité
                    agent.learn(current_state, action, 0.5, state, True, [])
            else:
                # On enregistre le coup pour pouvoir le punir si l'adversaire gagne au tour d'après
                history.append((current_state, action))
                # Apprentissage neutre pendant la partie
                agent.learn(current_state, action, 0, state, False, env.legal_actions())



        # On enregistre les données
        epsilon_history.append(agent.epsilon)
        win_history.append(won)
        
        agent.decay_epsilon()

        if (episode + 1) % 5000 == 0:
            print(f"Épisode {episode + 1}/{num_episodes} terminé. Epsilon: {agent.epsilon:.2f}")

    # --- CALCUL DE LA PERFORMANCE (MOYENNE GLISSANTE) ---
    # On calcule le taux de victoire tous les 500 épisodes pour lisser la courbe
    window = 500
    win_rate_history = []
    for i in range(window, len(win_history)):
        rate = sum(win_history[i-window:i]) / window
        win_rate_history.append(rate)

    # --- GÉNÉRATION DES GRAPHIQUES ---

    # 1. Courbe d'Epsilon
    plt.figure(figsize=(10, 5))
    plt.plot(epsilon_history, color='blue', label='Epsilon (Curiosité)')
    plt.title("Décroissance de l'Epsilon")
    plt.xlabel("Épisodes")
    plt.ylabel("Valeur")
    plt.legend()
    plt.savefig("epsilon_decay.png")
    plt.close()

    # 2. Courbe de Performance (Taux de Victoire)
    plt.figure(figsize=(10, 5))
    plt.plot(win_rate_history, color='green', label='Taux de Victoire (Moyenne glissante)')
    plt.title(f"Évolution des performances (Fenêtre de {window} parties)")
    plt.xlabel("Épisodes")
    plt.ylabel("Taux de Victoire (%)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.savefig("performance_win_rate.png")
    plt.close()

    agent.save("morpion_qtable.pkl")
    print("\nEntraînement terminé !")
    print("- Graphique de performance sauvegardé : performance_win_rate.png")

if __name__ == "__main__":
    train()