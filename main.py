import pygame, sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")      
    # set up font and create variables
    font = pygame.font.Font(None, 36)
    score = 0
    lives = 3
    # create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x,y)
    asteroid_field = AsteroidField()
    # Create a clock object
    clock = pygame.time.Clock()
    dt = 0
    #create infinite game loop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                lives -= 1
                log_event("player_hit")
                if lives <= 0:
                    print(f"Game over! Final Score: {score}")
                    sys.exit()
                else:
                    # Player survived, but lost a life. Reset player to the center of the screen
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    
                    # so the player doesn't instantly die upon respawning
                    for a in asteroids:
                        a.kill()
                    break
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score += 10

        screen.fill("black")
        player.draw(screen)
        for obj in drawable:
            obj.draw(screen)
        # draw UI on top of everything else
        score_text = font.render(f"Score: {score}", True, "white")
        lives_text = font.render(f"Lives: {lives}", True, "white")
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 45))
        pygame.display.flip()
        clock.tick(60)
        dt = clock.tick(60) / 1000
        print(dt)

if __name__ == "__main__":
    main()
