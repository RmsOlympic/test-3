import pygame
pygame.init()
import random

'bagian variable'
lebar_scene = 1000
tinggi_scene = 600
judul_scene = 'Space Fighter'
Points = 0
Lewat = 0
jumlah_bullet = 5
waktu_reload = 5 

'bagian aset'
Background = 'galaxy.jpg'
fighter = 'stuff\playerShip1_blue.png'
enemy = 'stuff\meteorBrown_big1.png'
Background_music = 'sounds\Mice on Venus.mp3'
obstacles = 'stuff\scratch2.png'
bullet = 'stuff\laserBlue12.png'

'bagian scene'
scene = pygame.display.set_mode((lebar_scene, tinggi_scene))
back = pygame.transform.scale(pygame.image.load(Background), (lebar_scene, tinggi_scene))
fps = pygame.time.Clock()
pygame.display.set_caption(judul_scene)

'bagian music'
pygame.mixer.init()
pygame.mixer.music.load(Background_music)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play()

'bagian tulisan'
pygame.font.init()
font1 = pygame.font.SysFont("IMPACT", 40)

'bagian kelas'
class GameSprite(pygame.sprite.Sprite):
   def __init__(self, image, x, y, lebar, tinggi, speed):
       super().__init__()
       self.lebar = lebar
       self.tinggi = tinggi
       self.image = pygame.transform.scale(pygame.image.load(image),
                                           (self.lebar, self.tinggi))   
       self.speed = speed
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
   def reset(self):
       scene.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
            tombol = pygame.key.get_pressed()
            if tombol[pygame.K_a] and self.rect.x > 0:
                self.rect.x -= self.speed
            if tombol[pygame.K_d] and self.rect.x < lebar_scene - self.lebar:
                self.rect.x += self.speed       
            if tombol[pygame.K_w] and self.rect.y > 0:
                self.rect.y -= self.tinggi
            if tombol[pygame.K_s] and self.rect.y < tinggi_scene - self.tinggi:
                self.rect.y += self.tinggi     

    def shoot(self): #metode untuk mengeluarkan peluru
       global jumlah_bullet
       if jumlah_bullet > 0:
           bullet1 = Bullet(bullet, self.rect.x + 26, self.rect.top, 20, 20, 2)
           grup_peluru.add(bullet1)
           jumlah_bullet -= 1

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > tinggi_scene:
            self.rect.y = -100
            self.rect.x = random.randint(100, lebar_scene-100)
            global Lewat
            Lewat += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 100:
            self.kill()            

'bagian object'
player1 = Player(fighter, 50,tinggi_scene -50, 50, 50, 10)

grup_musuh = pygame.sprite.Group()
jumlah_musuh = 3
for a in range(jumlah_musuh):
    musuh1 = Enemy(enemy,
                   random.randint(50, lebar_scene-100), 
                   random.randint(-50, 100),
                   50, 50, 10
                  )   
    grup_musuh.add(musuh1) 

grup_peluru = pygame.sprite.Group()                     

grup_obstacles = pygame.sprite.Group()
jumlah_obstacles = 5
for a in range(jumlah_obstacles):
    obstacles1 = Enemy(obstacles,
                   random.randint(50, lebar_scene-100), 
                   random.randint(-50, 100),
                   50, 50, 10
                  )   
    grup_obstacles.add(obstacles1) 
               
    
'bagian loop'
GAME_RUN = True
while GAME_RUN:
    'bagian tampilan'
    scene.blit(back, (0, 0))
    player1.reset()
    player1.update()
    grup_musuh.draw(scene)
    grup_musuh.update()
    grup_peluru.draw(scene)
    grup_peluru.update()
    grup_obstacles.draw(scene)
    grup_obstacles.update()


    'bagian tampilan tulisan'
    score = font1.render("SCORE :"+ str(Points), True, (250 ,250 ,250))
    missed = font1.render("MISSED :"+ str(Lewat), True, (250 ,250 ,250))
    scene.blit(score, (10, 10))
    scene.blit(missed, (10, 100))
    
    'event handler'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player1.shoot()

    'bagian tabrakan dan win loss'
    if pygame.sprite.spritecollide(player1, grup_musuh, False):
        print("You Have Been Hit")    

    Hit = pygame.sprite.groupcollide(grup_peluru, grup_musuh, True, True) 
    for a in Hit:
        musuh1 = Enemy(enemy,
                   random.randint(50, lebar_scene-100), 
                   random.randint(-50, 100),
                   50, 50, 10
                  )   
        grup_musuh.add(musuh1) 
        Points += 1

    pygame.sprite.groupcollide(grup_peluru, grup_obstacles  , True, True)    
    #syarat menang
    if Points >= 5:
        print("You Win")
    #syarat kalah
    if Lewat >= 5:
        print("You Lose")    

    'Bagian Reload'    
    if jumlah_bullet <= 0:
        waktu_reload -= 0.1
        if waktu_reload <= 0:
            jumlah_bullet = 5
            waktu_reload = 5

    'bagian penting'
    fps.tick(60)
    pygame.display.update()