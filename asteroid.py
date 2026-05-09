import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS, ASTEROID_SPAWN_RATE_SECONDS, ASTEROID_MAX_RADIUS, LINE_WIDTH
from particle import Particle

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen,"white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        num_particles = random.randint(5, 10)
        for _ in range(num_particles):
            # Pick a completely random direction (0 to 360 degrees)
            random_angle = random.uniform(0, 360)
            # Pick a random speed (adjust these numbers if you want faster/slower sparks)
            random_speed = random.uniform(50, 200)
            
            # Create a velocity vector pointing up, then rotate it to the random angle
            particle_velocity = pygame.Vector2(0, 1).rotate(random_angle) * random_speed
            
            # Instantiate the particle (it automatically joins the groups!)
            Particle(self.position.x, self.position.y, particle_velocity)
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        
        vec1 = self.velocity.rotate(random_angle)
        vec2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid1.velocity = vec1 * 1.2
        asteroid2.velocity = vec2 * 1.2

