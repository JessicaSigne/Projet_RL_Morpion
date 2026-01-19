import random
import pickle # Pour sauvegarder et charger la mémoire de l'IA

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon_max=1.0, epsilon_min=0.01, decay=0.99995):
        self.q_table = {}  # Le dictionnaire Q 
        self.alpha = alpha  # Taux d'apprentissage (vitesse à laquelle on oublie l'ancien pour le nouveau) 
        self.gamma = gamma  # Facteur de remise (importance des récompenses futures) 
        # self.epsilon = epsilon  # Probabilité d'explorer (jouer au hasard) 

        # Gestion de l'exploration
        self.epsilon = epsilon_max
        self.epsilon_min = epsilon_min
        self.decay = decay

    def get_q(self, state, action):
        """Récupère la valeur Q. Retourne 0 si on ne connaît pas encore ce cas."""
        return self.q_table.get((state, action), 0.0)

    def act(self, state, legal_actions):
        """Choisit une action selon la politique epsilon-greedy."""
        # EXPLORATION : On joue au hasard 
        if random.random() < self.epsilon:
            return random.choice(legal_actions)
        
        # EXPLOITATION : On choisit le meilleur coup mémorisé 
        q_values = [self.get_q(state, a) for a in legal_actions]
        max_q = max(q_values)
        
        # S'il y a plusieurs meilleurs coups (ex: plusieurs 0), on en prend un au hasard parmi eux 
        best_actions = [a for a, q in zip(legal_actions, q_values) if q == max_q]
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, done, next_legal_actions):
        """Mise à jour de la Q-table après un coup."""
        q_old = self.get_q(state, action) 
        
        if done:
            # Si la partie est finie, il n'y a pas d'état futur 
            target = reward
        else:
            # Formule mathématique : Récompense immédiate + futur possible 
            max_future_q = max([self.get_q(next_state, a) for a in next_legal_actions]) if next_legal_actions else 0
            target = reward + self.gamma * max_future_q
        
        # On ajuste la valeur Q selon l'erreur entre ce qu'on prévoyait et la réalité 
        self.q_table[(state, action)] = q_old + self.alpha * (target - q_old)
        
    def decay_epsilon(self):
        """Réduit epsilon petit à petit jusqu'à atteindre le minimum."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.decay)
        
    def save(self, filename):
        """Sauvegarde l'intelligence de l'IA dans un fichier."""
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, filename):
        """Charge une intelligence précédemment apprise."""
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)