import random
import math
import pygame
import tkinter as tr
from tkinter import messagebox


# Initialization of a pygame
pygame.init()

# Setting up game screen. remember to have always even multiplier for screen resolution
screen_size_x = 800
screen_size_y = 640
screen = pygame.display.set_mode((screen_size_x, screen_size_y))
background = pygame.image.load("graphics/background_2.jpg")


# Game title and icon
pygame.display.set_caption("graphics/Space Invaders")
icon = pygame.image.load("graphics/ufo.png")
pygame.display.set_icon(icon)


# Player image
player_img = pygame.image.load("graphics/player.png")
player_size = player_img.get_rect().size[0]
player_movement_range = 2
# Setting players starting position
player_x = screen_size_x/2 - player_size
player_y = screen_size_y/1.2 - player_size



def player(x,y):
	screen.blit(player_img, (x, y))

#multiple enemy

enemy_img = []
enemy_x = []
enemy_y = []
enemy_movement_x = []
enemy_movement_y = 10

num_of_enemies = 3

for i in range(num_of_enemies):
	enemy_img.append(pygame.image.load("graphics/enemy.png"))
	enemy_x.append(random.randint(0, screen_size_x))
	enemy_y.append(random.randint(0, screen_size_y/4))
	enemy_movement_x.append(0.2 * ((-1)**i))

def enemy(x, y, i):
	screen.blit(enemy_img[i], (x,y))


# Bullet image
bullet_img = pygame.image.load("graphics/bullet.png")
bullet_x = player_x 
bullet_y = player_y - player_img.get_rect().size[0]
bullet_movement_y = 6
bullet_state = "ready"

def bullet(x, y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bullet_img, (x,y))


# Colision

def colision(enemy_x, enemy_y, bullet_x, bullet_y):
	return math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2) < 16


# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

def render_score(text_x, text_y):
	player_score = font.render("Score: " + str(score), True, (255,255,255))
	screen.blit(player_score, (text_x, text_y))

over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over():
	screen.blit(over_font.render("GAME OVER!", True, (255,255,255)), (screen_size_x/4, screen_size_y/2))



running = True

while running:
	screen.fill((0,59,100))
	screen.blit(background, (0,0))

	player_position_change_x = 0
	player_position_change_y = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	

	#if keystroke was pressed check if it was right or left or up or down
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			player_position_change_x -= player_movement_range
		elif event.key == pygame.K_RIGHT:
			player_position_change_x += player_movement_range
		elif event.key == pygame.K_UP:
			player_position_change_y -= player_movement_range
		elif event.key == pygame.K_DOWN:
			player_position_change_y += player_movement_range

		if event.key == pygame.K_SPACE and bullet_state == "ready":
			bullet_x = player_x 
			bullet_y = player_y - player_img.get_rect().size[0]
			bullet(bullet_x, bullet_y)


	# Checking if our hero wont cross borders of a screen. 
	if player_x + player_position_change_x >= screen_size_x - player_size:
		player_x = screen_size_x - player_size
	elif player_x + player_position_change_x <= 0:
		player_x = 0
	else:
		player_x += player_position_change_x

	if player_y + player_position_change_y >= screen_size_y - player_size:
		player_y = screen_size_y - player_size
	elif player_y + player_position_change_y <= 0:
		player_y = 0	   
	else:
		player_y += player_position_change_y


	#Creating enemies
	for i in range(num_of_enemies):
	#enemy will be moving randomly		

		if enemy_x[i] + enemy_movement_x[i] >= screen_size_x - player_size:
			enemy_x[i] = screen_size_x - player_size
			enemy_movement_x[i] = enemy_movement_x[i] * -1
			enemy_y[i] += enemy_movement_y 
		elif enemy_x[i] <= 0:
			enemy_x[i] = 0
			enemy_movement_x[i] = enemy_movement_x[i] * -1
			enemy_y[i] += enemy_movement_y

		if enemy_y[i] >= player_y:
			game_over()			
			running = False			
			break

		enemy_x[i] += enemy_movement_x[i] 	

		# Check if colision happend
		shot_down = colision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
		if shot_down:
			bullet_y -= bullet_movement_y
			bullet(bullet_x, bullet_y)
			bullet_state = "ready"
			score += 100
			enemy_x[i] = random.randint(0, screen_size_x)
			enemy_y[i] = random.randint(0, screen_size_y/4)

			if score % 1000 == 0:
				enemy_movement_x[i] = abs(enemy_movement_x[i]) + 0.1
				num_of_enemies += 1
				enemy_img.append(pygame.image.load("graphics/enemy.png"))
				enemy_x.append(random.randint(0, screen_size_x))
				enemy_y.append(random.randint(0, screen_size_y/4))
				enemy_movement_x.append(0.2*(-1**i))

		enemy(enemy_x[i], enemy_y[i], i)


	#bullet
	if bullet_state == "fire":
		bullet_y -= bullet_movement_y
		bullet(bullet_x, bullet_y)

	if bullet_y <= 0:
		bullet_state = "ready"

	render_score(text_x, text_y)
	player(player_x, player_y)	
	pygame.display.update()