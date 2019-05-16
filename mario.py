import pygame
import random
random.seed(a=None)
pygame.init()
screenleftright=852
screenup=480
win = pygame.display.set_mode((screenleftright, screenup))
k = 6
print(k)

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]

walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

zombie_right = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                  pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                  pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png')]

zombie_left = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                  pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                  pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png')]
bg = pygame.image.load('1.jpg')
char = pygame.image.load('standing.png')


clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('rifle.wav')
#music = pygame.mixer.music.load('mymusic.mp3')
#pygame.mixer.music.play(-1)


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = True
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox=(self.x+20,self.y+10,28,60)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y+2 + 10, 28, 53)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)
class zombie(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 6
        self.left = False
        self.right = True
        self.walkCount = 0
        self.hp = 60
        self.hitbox = (self.x+24, self.y + 2, 30, 60)
    def walker(self, win):

        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
             win.blit(zombie_left[self.walkCount // 3], (self.x, self.y))
             self.walkCount += 1
        elif self.right:
            win.blit(zombie_right[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:

            if self.right:
                win.blit(zombie_right[0], (self.x, self.y))
            else:
                win.blit(zombie_left[0], (self.x, self.y))
        pygame.draw.rect(win, (0, 255, 0), (self.x+5, self.y-15, 60, 12), 1)
        pygame.draw.rect(win, (0, 255, 0), (self.x+5, self.y-12, self.hp, 6), 5)
        self.hitbox = (self.x+22, self.y + 2, 30, 60)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)



class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 13 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow(bullets):
    win.blit(bg, (0, 0))
    man.draw(win)
    for enemy in zombies:
        enemy.walker(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()
man = player(200, 410, 64, 64)
zombies = [zombie(random.randint(60,screenleftright-50),410,64,64)]
bullets =[]


run = True
shootcounter = 0
level=1
while run:
    clock.tick(27)

    if shootcounter > 0:
        shootcounter += 1
    if shootcounter == 4:
        shootcounter = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



   # for walker in zombies:
      #  if man.x > walker.hitbox[0] - walker.hitbox[2] and man.x < walker.hitbox[0] + walker.hitbox[2] and man.y > walker.hitbox[1] - walker.hitbox[3] and man.y < walker.hitbox[1] + walker.hitbox[3]:
        #    run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootcounter==0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 7:
            bulletSound.play()
        if len(bullets) <7:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (255, 255, 0), facing))
        shootcounter=1
    for bullet in bullets:
        flag = 1
        if bullet.x < screenleftright and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        for walker in zombies:

            if bullet.x > walker.hitbox[0]-walker.hitbox[2] and bullet.x < walker.hitbox[0]+walker.hitbox[2]and bullet.y > walker.hitbox[1]-walker.hitbox[3] and bullet.y < walker.hitbox[1]+walker.hitbox[3]:
                walker.hp -=20
                bullets.pop(bullets.index(bullet))
                flag=0
                if walker.hp <=0:
                    zombies.pop(zombies.index(walker))
                    flag=0
            if flag ==0:
                break


    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screenleftright - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True

            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    for enemy in zombies:
        if enemy.x > screenleftright-52:
            enemy.vel *= -1
            enemy.right = False
            enemy.left = True
        if enemy.x < 10:
            enemy.vel *= -1
            enemy.right = True
            enemy.left = False
        enemy.x = enemy.x + enemy.vel
    if zombies == []:
        bullets.pop
        level +=1
        for enemy in  range(level):
            zombies.append(zombie(random.randint(60, screenleftright-50), 410, 64, 64))
            if random.randint(0,1):
                zombies[enemy].left = True
                zombies[enemy].right = False
                zombies[enemy].vel *= -1


    redrawGameWindow(bullets)

pygame.quit()