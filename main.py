import pygame
import random
import os

pygame.font.init()
pygame.init()

WIDTH, HEIGHT = 1200, 565
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie War")

IMAGE_WIDTH, IMAGE_HEIGHT = 50, 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128,128,128)

MAX_BULLET = 3

BULLET_SPEED = 2050, 30

BULLET_IMAGE = pygame.image.load(os.path.join('image', 'bullet.png'))
BULLET = pygame.transform.scale(BULLET_IMAGE, (50, 30))

BG = pygame.image.load(os.path.join('image','bg.png'))

BG_IMAGE = pygame.transform.scale(BG, (1200, 565))

PLAYER = pygame.image.load(os.path.join('image','player.png'))

SPEED = 5

ZOMBIE = pygame.image.load(os.path.join('image','zombie.png'))

PLAYER_IMAGE = pygame.transform.scale(PLAYER, (IMAGE_WIDTH, IMAGE_HEIGHT))

FPS = 60

TEXT_FONT = pygame.font.SysFont('comicsans', 40)

SCREEN_FONT = pygame.font.SysFont('comicsans', 100)


def user_movement(keys_pressed, user):
    if keys_pressed[pygame.K_a] and user.x - SPEED > 0:
        user.x -= SPEED
    if keys_pressed[pygame.K_d] and user.x + SPEED + user.width < WIDTH:
        user.x += SPEED
    if keys_pressed[pygame.K_w] and user.y - SPEED > 0 + 365:
        user.y -= SPEED
    if keys_pressed[pygame.K_s] and user.y + SPEED + user.height < HEIGHT:
        user.y += SPEED


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ZOMBIE
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.x = WIDTH
        self.rect.y = random.randint(350, max(HEIGHT - self.rect.height, 0))
        self.health = 5
        self.direction = "left"
    
    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.direction = "right"
    
        if self.health <= 0:
            self.kill()
            
    def hit(self):
        self.health -= 1


class StartScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.text = self.font.render("Press SPACE to start", True, WHITE)
        self.text_rect = self.text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 70))
        
        self.new_text = self.font.render("Use W, S, D, A to Move", True, WHITE)
        self.new_text_rect = self.new_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
        
        self.next_text = self.font.render("Press R to reload", True, WHITE)
        self.next_text_rect = self.next_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

        self.shoot_text = self.font.render("Tap Right CTRL To Shoot", True, WHITE)
        self.shoot_rect = self.shoot_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))


    def draw(self):
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(self.text, self.text_rect)
        SCREEN.blit(self.new_text, self.new_text_rect)
        SCREEN.blit(self.next_text, self.next_text_rect)
        SCREEN.blit(self.shoot_text, self.shoot_rect)


def draw_window(user, user_bullets, user_health, zombies, bullets_left, kills):
    SCREEN.blit(BG_IMAGE, (0,0))

    user_health_text = TEXT_FONT.render("Health: " + str(user_health), 1, WHITE)
    SCREEN.blit(user_health_text, (10, 10))

    bullets_left_text = TEXT_FONT.render("Bullets Left: " + str(bullets_left), 1, WHITE)
    SCREEN.blit(bullets_left_text, (10, 50))

    kills_text = TEXT_FONT.render("Kills: " + str(kills), 1, WHITE)
    SCREEN.blit(kills_text, (700, 10))

    SCREEN.blit(PLAYER_IMAGE, (user.x, user.y))

    for zombie in zombies:
        SCREEN.blit(zombie.image, zombie.rect)

    for bullet in user_bullets:
        SCREEN.blit(BULLET, bullet)

    pygame.display.update()


def screen_text(text):
    draw_text = SCREEN_FONT.render(text, 1, WHITE)
    SCREEN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)
    

def main():
    user = pygame.Rect(70, 470, IMAGE_WIDTH, IMAGE_HEIGHT)

    zombies = pygame.sprite.Group()
    
    start = StartScreen()

    kills = 0

    winner_text = ""

    bullets_left = 20

    user_bullets = []

    user_health = 10
    
    clock = pygame.time.Clock()
    run = True

    show_start_screen = True

    while show_start_screen:
        start.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_start_screen = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_start_screen = False

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
                
            if event.type == pygame.KEYDOWN:
            # user bullet add
                if event.key == pygame.K_RCTRL and len(user_bullets) < MAX_BULLET and bullets_left >= 1:
                    bullet = pygame.Rect(user.x + user.width, user.y + user.height // 2 - 20, 10, 5)
                    user_bullets.append(bullet)
                    bullets_left -= 1

                
                if event.key == pygame.K_r and bullets_left < 20:
                    bullets_left = 20
        
        


        for bullet in user_bullets:
            bullet.x += BULLET_SPEED
            for zombie in zombies:
                if zombie.rect.colliderect(bullet):
                    user_bullets.remove(bullet)
                    zombie.hit()
                    if zombie.health == 0:
                        zombies.remove(zombie)
                        kills += 1
                    break
                    
            if bullet.x > WIDTH:
                user_bullets.remove(bullet)

        for zombie in zombies:
            if zombie.rect.x < 0:
                user_health -= 1  
                zombies.remove(zombie)

        if random.randint(1, 100) == 1:
            zombies.add(Zombie())

        
        for zombie in zombies:
            zombie.update()
            SCREEN.blit(zombie.image, zombie.rect)
            if user.colliderect(zombie.rect):
                user_health -= 1
                zombies.remove(zombie)

        if user_health == 0:
            winner_text = f'You Have Died. Kills: {kills}'

        if winner_text != "":
            screen_text(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        user_movement(keys_pressed, user)

        draw_window(user, user_bullets, user_health, zombies, bullets_left, kills)

    pygame.quit()
    


if __name__ == "__main__":
    main()
