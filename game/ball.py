import pygame

class Ball:
    def __init__(self, x, y, velocity_x, velocity_y, screen_width, screen_height, size=15,
                 sound_wall=None):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.sound_wall = sound_wall  # Sound for wall bounce

    def move(self):
        # Move the ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Top and bottom wall collision
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            if self.sound_wall:
                self.sound_wall.play()
        elif self.y + self.size >= self.screen_height:
            self.y = self.screen_height - self.size
            self.velocity_y *= -1
            if self.sound_wall:
                self.sound_wall.play()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def reset(self):
        # Center the ball and reverse direction randomly
        self.x = self.screen_width // 2 - self.size // 2
        self.y = self.screen_height // 2 - self.size // 2
        self.velocity_x *= -1
        self.velocity_y *= -1
