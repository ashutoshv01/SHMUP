#SHMUP GAME
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
import pygame
import random

from os import path

img_dir = path.join(path.dirname(__file__),"images")  # this variable will hold address to the images folder
snd_dir = path.join(path.dirname(__file__),"snd")

WIDTH = 480
HEIGHT = 600
FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

pygame.init() 
pygame.mixer.init()  
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SHMUP")
clock = pygame.time.Clock()   

# code for highscore
def get_high_score():
    # Default high score
    high_score = 0
 
    # Try to read the high score from a file
    try:
        high_score_file = open("highscore.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        # print("The high score is", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")
 
    return high_score

def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("highscore.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")

font_name = pygame.font.match_font("arial")  #finds the best match to the font in the computer
font_name2 = pygame.font.match_font("copper black")
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text,True,WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface,text_rect)

def draw_message(surf, text, size, x, y):
	font = pygame.font.Font(font_name2,size)
	font.set_bold(True)
	text_surface = font.render(text,True,RED)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface,text_rect)

def draw_shieldbar(surf, x, y, pct):
	if pct<0:
		pct =0
	bar_length =100
	bar_height =10
	fill = (pct/100)*bar_length
	outline_rect = pygame.Rect(x,y,bar_length,bar_height)
	fill_rect = pygame.Rect(x,y,fill,bar_height)
	pygame.draw.rect(surf,GREEN, fill_rect)
	pygame.draw.rect(surf,WHITE, outline_rect, 2)

def show_over_screen():
	screen.blit(background, background_rect)
	draw_message(screen, "SHMUP!", 64, WIDTH/2, HEIGHT/4)
	draw_text(screen,"LEFT AND RIGHT ARROW KEY TO MOVE AND UP TO FIRE!", 16, WIDTH/2, HEIGHT/2)
	draw_text(screen,"Press SPACEBAR to begin",14,WIDTH/2,3*HEIGHT/4)
	pygame.display.flip()
	waiting = True
	while(waiting):
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					waiting = False

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) 
		self.image = pygame.transform.scale(player_img, (50, 38)) # to scale the size of image by artist
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #command to draw circle
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT-10
		self.speedx = 0
		self.shield = 100

	def update(self):
		self.speedx = 0
		keystate = pygame.key.get_pressed() #tells which keys have been pressed
		if keystate[pygame.K_LEFT]:
			self.speedx = -5
		if keystate[pygame.K_RIGHT]:
			self.speedx = 5
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.bottom)   # x and y were earlier for this
		all_sprites.add(bullet)
		bullets.add(bullet)
		shoot_sound.play()  # to play sound

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) 
		self.image = pygame.transform.scale(random.choice(enemy_images), (38,29)) #random.choice(enemy_images) 
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 15
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #command to draw circle
		self.rect.x = random.randrange(WIDTH-self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(6,9)
		self.speedx = random.randrange(-3,3)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT+10 or self.rect.left<-25 or self.rect.right>WIDTH+25:
			self.rect.x = random.randrange(WIDTH-self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(6,9)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()  # to delete that bullet

class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) 
		self.image_orig = random.choice(meteor_images) # randomly choosing from list
		self.image = self.image_orig.copy()  # using original image for rotation and copy for sprite
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		self.radius = (int)(self.rect.width *0.85/2)
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #command to draw circle
		self.rect.x = random.randrange(WIDTH-self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(5,7)
		self.speedx = random.randrange(-2,2)
		self.rot = 0
		self.rot_speed = random.randrange(-8,8)
		self.last_update = pygame.time.get_ticks()   # use of clock to measure time

	def rotate(self):
		now = pygame.time.get_ticks()
		if now-self.last_update>50:      # if present time minus last update time exceeds 50
			self.last_update=now
			self.rot = (self.rot + self.rot_speed)%360
			# we need to update the rectangle as well
			new_image = pygame.transform.rotate(self.image_orig,self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT+10 or self.rect.left<-25 or self.rect.right>WIDTH+25:
			self.rect.x = random.randrange(WIDTH-self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(3,5)			

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self) 
		self.size = size
		self.image = expl_anim[size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame =0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 75

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame+=1
			if self.frame == len(expl_anim[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = expl_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

# load all game graphics
#randomly selecting images from list
background = pygame.image.load(path.join(img_dir,"bHiPMju.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,"playerShip2_red.png")).convert()
# enemy_img = pygame.image.load(path.join(img_dir,"enemyRed5.png")).convert()
enemy_images = []
enemy_list=["enemyGreen4.png","enemyBlack1.png","enemyBlue2.png","enemyRed5.png"]

for img in enemy_list:
	enemy_images.append(pygame.image.load(path.join(img_dir,img)))

bullet_img = pygame.image.load(path.join(img_dir,"laserRed16.png")).convert()
meteor_images = []
meteor_list=["meteorBrown_med1.png","meteorBrown_med3.png","meteorBrown_small1.png","meteorBrown_small2.png","meteorBrown_tiny1.png","meteorBrown_tiny2.png"]

for img in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_dir,img)))

expl_anim = {} # dictionary for explosion
expl_anim["lg"] = []
expl_anim["sm"] = []

for i in range(9):
	filename = "regularExplosion0{}.png".format(i)
	img = pygame.image.load(path.join(img_dir, filename))
	img.set_colorkey(BLACK)
	img_lg = pygame.transform.scale(img,(75,75))
	expl_anim["lg"].append(img_lg)
	img_sm = pygame.transform.scale(img,(32,32))
	expl_anim["sm"].append(img_sm)
# load all game sounds

shoot_sound = pygame.mixer.Sound(path.join(snd_dir,"Laser_Shoot2.wav"))
shoot_sound.set_volume(0.4)
collide_sound = pygame.mixer.Sound(path.join(snd_dir,"Hit_Hurt5.wav"))
collide_sound.set_volume(0.4)
loss_snd = pygame.mixer.Sound(path.join(snd_dir,"sfx_shieldDown.ogg"))
# pygame.mixer.music.load('foo.mp3')
# loss_snd.play(loops = 5)
expl_snds = []
for snd in ["Explosion2.wav","Explosion3.wav"]:
	expl_snds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
expl_snds[0].set_volume(0.25)
expl_snds[1].set_volume(0.25)

pygame.mixer.music.load(path.join(snd_dir,"tgfcoder-FrozenJam-SeamlessLoop.ogg"))  # to play background music
pygame.mixer.music.set_volume(0.7) # set volume low


pygame.mixer.music.play(loops=-1) # -1 ensures that it loops each time music ends
displayhigh = "HIGHSCORE:"
displaymessage = "NEW HIGH SCORE!!!"

#game loop
running = True
game_over = True
while running:
	
	if game_over:
		show_over_screen()
		game_over = False
		all_sprites = pygame.sprite.Group() 
		mobs = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		meteors = pygame.sprite.Group()
		player = Player() 
		all_sprites.add(player)
		for i in range(7):
			m = Mob()
			s = Meteor()
			all_sprites.add(m)
			mobs.add(m)
			all_sprites.add(s)
			meteors.add(s)
			flaghigh=0
			score = 0

	clock.tick(FPS)
	
	high_score=get_high_score()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player.shoot()

	all_sprites.update()
	#CHECK TO SEE IF BULLET HITS OR NOT
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # for collission of groups
	for hit in hits:
		random.choice(expl_snds).play()  # randomly choose one explosion and play sound
		score += 50 - hit.radius
		expl = Explosion(hit.rect.center,"lg")
		all_sprites.add(expl)
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)
		
	hits2 = pygame.sprite.groupcollide(meteors, bullets,True, True)
	for hit in hits2:
		expl = Explosion(hit.rect.center,"lg")
		all_sprites.add(expl)
		s = Meteor()
		all_sprites.add(s)
		meteors.add(s)
		random.choice(expl_snds).play()
		score += 50 - hit.radius

	if score>high_score:
		save_high_score(score)
		flaghigh = 1
	#CHECK TO SEE IF MOB HITS PLAYER OR NOT
	# circular boundary collission
	hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
	if hits:
		for i in range(5):
			loss_snd.play()
		game_over = True
		
	hits = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
	for hit in hits:
		player.shield -= 2*hit.radius
		expl = Explosion(hit.rect.center,"sm")
		all_sprites.add(expl)
		collide_sound.play()
		s = Meteor()
		all_sprites.add(s)
		meteors.add(s)
		if player.shield<=0:
			for i in range(5):
				loss_snd.play()
			game_over = True


	#DRAW/RENDER
	screen.fill(BLACK)
	screen.blit(background, background_rect)                       #blitting the background on the screen
	all_sprites.draw(screen)
	draw_shieldbar(screen,5,5,player.shield)
	draw_text(screen,str(score),14,WIDTH/2,10)
	draw_text(screen,displayhigh,14,8.2*WIDTH/11,10)
	draw_text(screen,str(high_score),14,10*WIDTH/11,10)
	if flaghigh == 1:
		draw_message(screen,displaymessage,20,8.2*WIDTH/11,30)
	pygame.display.flip() 

