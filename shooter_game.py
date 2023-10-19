#Створи власний Шутер!
from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

clock = time.Clock()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play()

game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, move_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = move_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.y, 10, 15, 20)
        bullets.add(bullet)


lost = 0#кількість пропущених монстрів
class Monster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 650)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    monster = Monster("ufo.png", randint(0, 650), -90, randint(1, 4), 80, 50)
    monsters.add(monster)



ship = Player("rocket.png", 350, 400, 5, 60, 80)

font.init()
text = font.SysFont("algerian", 30)

text1 = font.SysFont("chicago", 100, )
win_text = text1.render("YOU WIN", True, (20, 250, 20))
lose_text = text1.render("YOU LOSE", True, (180, 23, 20))

score_h = 0

life = 3

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                ship.fire()
    if finish != True:
        window.blit(background, (0, 0))

        score = text.render("Score: " + str(score_h), True, (250, 250, 137))
        window.blit(score, (10, 10))
        score_1 = text.render("Skip: " + str(lost), True, (250, 250, 137))
        window.blit(score_1, (10, 40))

        collide = sprite.groupcollide(bullets, monsters, True, True)
        for b in collide:
            score_h += 1
            monster = Monster("ufo.png", randint(0, 650), -90, randint(1, 4), 80, 50)
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, True):
            life -= 1
            monster = Monster("ufo.png", randint(0, 650), -90, randint(1, 4), 80, 50)
            monsters.add(monster)
        
        if life == 0 or lost >= 10:
            finish = True
            window.blit(lose_text, (350, 250))
        if score_h >= 15:
            finish = True
            window.blit(win_text, (350, 250))


        ship.reset()
        ship.update()
        monsters.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)

    display.update()
    clock.tick(60)
    