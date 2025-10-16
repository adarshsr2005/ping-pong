import pygame
from .paddle import Paddle
from .ball import Ball

pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 40)
        self.game_over = False
        self.target_score = 5

        # Load sounds
        self.sound_paddle = pygame.mixer.Sound("sounds/PingPongHit.wav")
        self.sound_wall = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")

        # Create ball with wall sound
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, sound_wall=self.sound_wall)


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Skip updates if game is already over
        if self.game_over:
            return

        # Move the ball
        self.ball.move()

        # Paddle collision
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.velocity_x = abs(self.ball.velocity_x)
            self.ball.x = self.player.x + self.paddle_width
            self.sound_paddle.play()

        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.velocity_x = -abs(self.ball.velocity_x)
            self.ball.x = self.ai.x - self.ball.size
            self.sound_paddle.play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.sound_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.sound_score.play()
            self.ball.reset()

        # AI follows the ball
        self.ai.auto_track(self.ball, self.height)

        # Check for game over
        self.check_game_over()


    def check_game_over(self):
        """Display winner message and open replay menu."""
        if self.player_score == self.target_score or self.ai_score == self.target_score:
            self.game_over = True
            winner_text = "Player Wins!" if self.player_score == self.target_score else "AI Wins!"

            # Display winner
            screen = pygame.display.get_surface()
            screen.fill(BLACK)
            text_surface = self.large_font.render(winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(1500)

            # Show replay menu
            self.show_replay_menu()

    def show_replay_menu(self):
        """Show replay options and handle user selection."""
        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        menu_lines = [
            "Select Match Type:",
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        y = self.height // 2 - 60
        for line in menu_lines:
            text_surface = self.font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, y))
            screen.blit(text_surface, text_rect)
            y += 40
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key in [pygame.K_3, pygame.K_5, pygame.K_7]:
                        self.target_score = int(event.unicode)
                        self.reset_game()
                        waiting = False

    def reset_game(self):
        """Reset scores and positions to start a new match."""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False

    def render(self, screen):
        if self.game_over:
            return  # Skip normal render when in game-over/replay menu

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))
