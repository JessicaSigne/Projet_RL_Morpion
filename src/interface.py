import pygame
import sys
from src.environnement import TicTacToeEnv
from src.agent import QLearningAgent

# --- CONFIGURATION ET COULEURS ---
WIDTH, HEIGHT = 600, 700 # Augmenté pour laisser de la place aux boutons en bas
BG_COLOR = (46, 2, 73)      # Violet très foncé
BTN_COLOR = (87, 10, 87)     # Violet médium
TEXT_COLOR = (248, 6, 204)   # Rose néon
WHITE = (255, 255, 255)
LINE_COLOR = (169, 16, 121)  # Rose/Violet clair

class TicTacToeGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Morpion par Jessica")
        self.font_main = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 25, bold=True)
        
        self.env = TicTacToeEnv()
        self.agent = QLearningAgent()
        
        # Chargement de l'IA
        try:
            self.agent.load("morpion_qtable.pkl")
            self.agent.epsilon = 0
        except:
            print("IA non chargée.")

        self.state = "MENU" # États possibles : MENU, GAME
        self.mode = 1       # 1:HvsH, 2:HvsA, 3:AvsA

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y))
        self.screen.blit(img, rect)

    def draw_menu(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("MORPION PAR JESSICA", self.font_main, TEXT_COLOR, WIDTH//2, 100)

        # Définition des boutons
        self.btn_hvh = pygame.Rect(150, 200, 300, 60)
        self.btn_hva = pygame.Rect(150, 300, 300, 60)
        self.btn_ava = pygame.Rect(150, 400, 300, 60)
        self.btn_quit = pygame.Rect(150, 500, 300, 60)

        buttons = [
            (self.btn_hvh, "Humain vs Humain"),
            (self.btn_hva, "Humain vs Agent"),
            (self.btn_ava, "Agent vs Agent"),
            (self.btn_quit, "Quitter")
        ]

        for rect, label in buttons:
            pygame.draw.rect(self.screen, BTN_COLOR, rect, border_radius=12)
            pygame.draw.rect(self.screen, TEXT_COLOR, rect, 3, border_radius=12)
            self.draw_text(label, self.font_button, WHITE, rect.centerx, rect.centery)

    def draw_game_board(self):
        self.screen.fill(BG_COLOR)
        # Grille
        for i in range(1, 3):
            pygame.draw.line(self.screen, LINE_COLOR, (0, i*200), (600, i*200), 7)
            pygame.draw.line(self.screen, LINE_COLOR, (i*200, 0), (i*200, 600), 7)

        # Dessin des formes 
        for i, cell in enumerate(self.env.board):
            row, col = i // 3, i % 3
            center = (col * 200 + 100, row * 200 + 100)
            if cell == 1: # X
                pygame.draw.line(self.screen, TEXT_COLOR, (center[0]-50, center[1]-50), (center[0]+50, center[1]+50), 10)
                pygame.draw.line(self.screen, TEXT_COLOR, (center[0]+50, center[1]-50), (center[0]-50, center[1]+50), 10)
            elif cell == 2: # O
                pygame.draw.circle(self.screen, WHITE, center, 60, 10)

        # Zone d'information en bas
        self.btn_back = pygame.Rect(50, 620, 150, 50)
        self.btn_reset = pygame.Rect(400, 620, 150, 50)
        
        pygame.draw.rect(self.screen, BTN_COLOR, self.btn_back, border_radius=8)
        self.draw_text("Menu", self.font_button, WHITE, self.btn_back.centerx, self.btn_back.centery)
        
        pygame.draw.rect(self.screen, BTN_COLOR, self.btn_reset, border_radius=8)
        self.draw_text("Rejouer", self.font_button, WHITE, self.btn_reset.centerx, self.btn_reset.centery)

        # Messages de fin 
        if self.env.done:
            # On vérifie si X a gagné, sinon si O a gagné, sinon c'est un nul 
            if self.env._check_winner(1):
                msg = "JOUEUR X A GAGNÉ !"
            elif self.env._check_winner(2):
                msg = "JOUEUR O A GAGNÉ !"
            else:
                msg = "MATCH NUL !"
            
            self.draw_text(msg, self.font_button, WHITE, WIDTH//2, 645)

    def run(self):
        while True:
            if self.state == "MENU":
                self.draw_menu()
            else:
                self.draw_game_board()
                # Tour IA 
                if not self.env.done:
                    if (self.mode == 2 and self.env.current_player == 2) or (self.mode == 3):
                        pygame.time.delay(500)
                        action = self.agent.act(self.env.get_state(), self.env.legal_actions())
                        self.env.step(action)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.state == "MENU":
                        if self.btn_hvh.collidepoint(pos): self.mode=1; self.state="GAME"; self.env.reset()
                        if self.btn_hva.collidepoint(pos): self.mode=2; self.state="GAME"; self.env.reset()
                        if self.btn_ava.collidepoint(pos): self.mode=3; self.state="GAME"; self.env.reset()
                        if self.btn_quit.collidepoint(pos): pygame.quit(); sys.exit()
                    
                    elif self.state == "GAME":
                        if self.btn_back.collidepoint(pos): self.state = "MENU"
                        if self.btn_reset.collidepoint(pos): self.env.reset()
                        
                        # Clic sur la grille 
                        if not self.env.done and pos[1] < 600:
                            row, col = pos[1]//200, pos[0]//200
                            action = row * 3 + col
                            if action in self.env.legal_actions():
                                self.env.step(action)

            pygame.display.update()
