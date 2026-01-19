class TicTacToeEnv:
    def __init__(self):
        # Le plateau est une liste de 9 cases. 0 = vide, 1 = X, 2 = O 
        self.board = [0] * 9
        self.current_player = 1  # Le joueur 1 commence 
        self.done = False

    def get_state(self):
        """Retourne une version 'figée' du plateau pour que l'IA puisse s'en souvenir."""
        # On inclut le joueur actuel pour éviter toute ambiguïté 
        return (tuple(self.board), self.current_player)

    def legal_actions(self):
        """Retourne la liste des indices des cases vides."""
        return [i for i, x in enumerate(self.board) if x == 0]

    def reset(self):
        """Remet le jeu à zéro pour une nouvelle partie."""
        self.board = [0] * 9
        self.current_player = 1
        self.done = False
        return self.get_state()

    def step(self, action):
        self.board[action] = self.current_player
        
        # On vérifie si le joueur actuel vient de gagner
        if self._check_winner(self.current_player):
            self.done = True
            return self.get_state(), 1, True # Récompense positive pour le gagnant
        
        # Match nul : plus de cases vides 
        if 0 not in self.board:
            self.done = True
            return self.get_state(), 0, True
        
        # La partie continue : on change de joueur
        self.current_player = 3 - self.current_player
        return self.get_state(), 0, False 

    def _check_winner(self, p):
        """Vérifie les 8 combinaisons gagnantes (lignes, colonnes, diagonales)."""
        win_conf = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_conf:
            if self.board[a] == self.board[b] == self.board[c] == p:
                return True
        return False