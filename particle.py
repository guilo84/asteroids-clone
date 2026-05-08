# particle.py
import pygame
from circleshape import CircleShape
from constants import PARTICLE_RADIUS, PARTICLE_LIFETIME

class Particle(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, PARTICLE_RADIUS)
        self.velocity = velocity
        self.time_to_live = PARTICLE_LIFETIME

    def draw(self, screen):
        # Let's draw them without a line width so they are solid little dots
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        self.time_to_live -= dt
        
        # If the timer runs out, remove the particle from the game
        if self.time_to_live <= 0:
            self.kill()
