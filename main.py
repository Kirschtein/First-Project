import pygame
import os
import random

pygame.init()
pygame.display.set_caption("Chimera")

# Global Constants
SCREEN_HEIGHT = 576
SCREEN_WIDTH = 936
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.transform.scale(pygame.image.load("images/Main1_side_right.png"), (64, 64)),
		   pygame.transform.scale(pygame.image.load("images/Main1_side_right_1.png"), (64, 64)),
		   pygame.transform.scale(pygame.image.load("images/Main1_side_right_2.png"), (64, 64)),
		   pygame.transform.scale(pygame.image.load("images/Main1_side_right_3.png"), (64, 64)),
		   pygame.transform.scale(pygame.image.load("images/Main1_side_right_4.png"), (64, 64)),
		   pygame.transform.scale(pygame.image.load("images/Main1_side_right_5.png"), (64, 64)),
		   pygame.transform.scale(pygame.image.load("images/Main1_side_right_6.png"), (64, 64)),
		   pygame.transform.scale(pygame.image.load("images/Main1_side_right_7.png"), (64, 64))]

JUMPING = pygame.transform.scale(pygame.image.load("images/Main1_jump_right.png"), (64, 64))

SITTING = [pygame.transform.scale(pygame.image.load("images/sit.png"), (64, 64)),
		   pygame.transform.scale(pygame.image.load("images/sit.png"), (64, 64))]

HYDRANT = [pygame.transform.scale(pygame.image.load("images/Hydrant.png"), (35,50)),
		   pygame.transform.scale(pygame.image.load("images/Hydrant.png"), (35,50)),
		   pygame.transform.scale(pygame.image.load("images/Hydrant.png"), (35,50))]

TREE = [pygame.transform.scale(pygame.image.load("images/Tree_1.png"), (64, 140)),
		pygame.transform.scale(pygame.image.load("images/Tree_1.png"), (64, 140)),
		pygame.transform.scale(pygame.image.load("images/Tree_2.png"), (64, 140))]

BOX = [pygame.transform.scale(pygame.image.load("images/box1.png"), (110, 90)),
	   pygame.transform.scale(pygame.image.load("images/box2.png"), (110, 90)),
	   pygame.transform.scale(pygame.image.load("images/box3.png"), (110, 90))]

SHADOW = [pygame.transform.scale(pygame.image.load("images/Enemy_1.png"), (64, 64)),
		  pygame.transform.scale(pygame.image.load("images/Enemy_2.png"), (64, 64))]

PORTAL = [pygame.transform.scale(pygame.image.load("images/portal_real.png"), (64, 128)),
		  pygame.transform.scale(pygame.image.load("images/portal_real.png"), (64, 128)),
		  pygame.transform.scale(pygame.image.load("images/portal_real.png"), (64, 128))]

STANDING = pygame.transform.scale(pygame.image.load("images/Main1_front.png"), (70, 110))
GIRL = pygame.transform.scale(pygame.image.load("images/Girl.png"), (64, 64))

RESETA = [pygame.transform.scale(pygame.image.load("images/reseta_real.png"), (45, 120)),
		  pygame.transform.scale(pygame.image.load("images/reseta_real.png"), (45, 120)),
		  pygame.transform.scale(pygame.image.load("images/reseta_real.png"), (45, 120))]

DRUG = [pygame.transform.scale(pygame.image.load("images/Drug.png"), (45, 90)),
		pygame.transform.scale(pygame.image.load("images/Drug.png"), (45, 90)),
		pygame.transform.scale(pygame.image.load("images/Drug.png"), (45, 90))]

music = pygame.mixer.music.load("music/Coldplay Something Just Like This Instrumental Official.mp3")

BG = pygame.image.load(os.path.join("images", "Background_2.jpg"))


class Boy:
	X_POS = 80
	Y_POS = 390
	Y_POS_SIT = 430
	JUMP_VEL = 8.5

	def __init__(self):
		self.sit_img = SITTING
		self.run_img = RUNNING
		self.jump_img = JUMPING

		self.boy_sit = False
		self.boy_run = True
		self.boy_jump = False

		self.step_index = 0
		self.jump_vel = self.JUMP_VEL
		self.image = self.run_img[0]
		self.boy_rect = self.image.get_rect()
		self.boy_rect.x = self.X_POS
		self.boy_rect.y = self.Y_POS

	def update(self, userInput):
		if self.boy_sit:
			self.sit()
		if self.boy_run:
			self.run()
		if self.boy_jump:
			self.jump()

		if self.step_index >= 10:
			self.step_index = 0

		if (userInput[pygame.K_UP] or userInput[pygame.K_w] or userInput[pygame.K_SPACE]) and not self.boy_jump:
			self.boy_sit = False
			self.boy_run = False
			self.boy_jump = True
		elif (userInput[pygame.K_DOWN] or userInput[pygame.K_s]) and not self.boy_jump:
			self.boy_sit = True
			self.boy_run = False
			self.boy_jump = False
		elif not (self.boy_jump or userInput[pygame.K_DOWN]):
			self.boy_sit = False
			self.boy_run = True
			self.boy_jump = False

	def sit(self):
		self.image = self.sit_img[self.step_index // 5]
		self.boy_rect = self.image.get_rect()
		self.boy_rect.x = self.X_POS
		self.boy_rect.y = self.Y_POS_SIT
		self.step_index += 1

	def run(self):
		self.image = self.run_img[self.step_index // 5]
		self.boy_rect = self.image.get_rect()
		self.boy_rect.x = self.X_POS
		self.boy_rect.y = self.Y_POS
		self.step_index += 1

	def jump(self):
		self.image = self.jump_img
		if self.boy_jump:
			self.boy_rect.y -= self.jump_vel * 4
			self.jump_vel -= 0.8
		if self.jump_vel < - self.JUMP_VEL:
			self.boy_jump = False
			self.jump_vel = self.JUMP_VEL

	def draw(self, SCREEN):
		SCREEN.blit(self.image, (self.boy_rect.x, self.boy_rect.y))


class Obstacle:
	def __init__(self, image, type):
		self.image = image
		self.type = type
		self.rect = self.image[self.type].get_rect()
		self.rect.x = SCREEN_WIDTH

	def update(self):
		self.rect.x -= game_speed
		if self.rect.x < -self.rect.width:
			obstacles.pop()

	def draw(self, SCREEN):
		SCREEN.blit(self.image[self.type], self.rect)


class Box(Obstacle):
	def __init__(self, image):
		self.type = random.randint(0, 2)
		super().__init__(image, self.type)
		self.rect.y = 380


class Tree(Obstacle):
	def __init__(self, image):
		self.type = random.randint(0, 2)
		super().__init__(image, self.type)
		self.rect.y = 325

class Hydrant(Obstacle):
	def __init__(self, image):
		self.type = random.randint(0, 2)
		super().__init__(image, self.type)
		self.rect.y = 405


class Shadow(Obstacle):
	def __init__(self, image):
		self.type = 0
		super().__init__(image, self.type)
		self.rect.y = 390
		self.index = 0

	def draw(self, SCREEN):
		if self.index >= 9:
			self.index = 0
		SCREEN.blit(self.image[self.index // 5], self.rect)
		self.index += 1


class Drug(Obstacle):
	def __init__(self, image):
		self.type = random.randint(0, 2)
		super().__init__(image, self.type)
		self.rect.y = 325


class Portal(Obstacle):
	def __init__(self, image):
		self.type = random.randint(0, 2)
		super().__init__(image, self.type)
		self.rect.y = 300


class Reseta(Obstacle):
	def __init__(self, image):
		self.type = random.randint(0, 2)
		super().__init__(image, self.type)
		self.rect.y = 350


def main():
	global game_speed, x_pos_bg, y_pos_bg, points, obstacles
	run = True
	clock = pygame.time.Clock()
	player = Boy()
	game_speed = 10
	x_pos_bg = 0
	y_pos_bg = 0
	points = 0
	font = pygame.font.Font('freesansbold.ttf', 20)
	hints = ["Delusions",
			 "Hallucinations",
			 "Disorganized thinking (speech)",
			 "Extremely disorganized or abnormal motor behavior.",
			 "Negative symptoms",
			 "Aripiprazole (Abilify)",
			 "Asenapine (Saphris)",
			 "Brexpiprazole (Rexulti)",
			 "Cariprazine (Vraylar)",
			 "Clozapine (Clozaril, Versacloz)",
			 "Individual therapy",
			 "Social skills training",
			 "Family therapy",
			 "Vocational rehabilitation and supported employment"]

	obstacles = []
	death_count = 0
	pygame.mixer.music.play(-1)

	def score():
		global points, game_speed
		points += 1
		if points % 500 == 0:
			game_speed += 1


		text = font.render("Points: " + str(points), True, (0, 0, 0))
		textRect = text.get_rect()
		textRect.center = (850, 30)
		SCREEN.blit(text, textRect)

	def background():
		global x_pos_bg, y_pos_bg
		image_width = BG.get_width()
		SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
		SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
		if x_pos_bg <= -image_width:
			SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
			x_pos_bg = 0
		x_pos_bg -= game_speed

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		userInput = pygame.key.get_pressed()

		background()
		score()
		player.draw(SCREEN)
		player.update(userInput)

		def hintPrint():
			text = font.render(hints[random.randint(0,13)], True, (250, 245, 225))
			textRect = text.get_rect()
			textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
			SCREEN.blit(text, textRect)
			pygame.display.update()
			pygame.time.delay(300)

		if len(obstacles) == 0:
			if random.randint(0, 2) == 0:
				obstacles.append(Box(BOX))
				# a for object identifier
				a = "Box"
			elif random.randint(0, 2) == 0:
				obstacles.append(Reseta(RESETA))
				a = "Reseta"
			elif random.randint(0, 2) == 0:
				obstacles.append(Drug(DRUG))
				a = "Drug"
			elif random.randint(0, 2) == 2:
				obstacles.append(Shadow(SHADOW))
				a = "Shadow"
			elif random.randint(0, 2) == 0:
				obstacles.append(Portal(PORTAL))
				a = "Portal"
			elif random.randint(0, 2) == 1:
				obstacles.append(Tree(TREE))
				a = "Tree"
			elif random.randint(0, 2) == 0:
				obstacles.append(Hydrant(HYDRANT))
				a = "Hydrant"

		for obstacle in obstacles:
			obstacle.draw(SCREEN)
			obstacle.update()
			if points == 3000:
				win(points)
			elif player.boy_rect.colliderect(obstacle.rect):
				# add or remove function depending on object's role
				if a == "Box":
					pygame.time.delay(1000)
					death_count += 1
					menu(death_count)
				elif a == "Tree":
					pygame.time.delay(1000)
					death_count += 1
					menu(death_count)
				elif a == "Shadow":
					pygame.time.delay(1000)
					death_count += 1
					menu(death_count)
				elif a == "Portal":
					pygame.time.delay(1000)
					death_count += 1
					menu(death_count)
				elif a == "Reseta":
					hintPrint()
				elif a == "Drug":
					pygame.time.delay(1000)
					death_count += 1
					menu(death_count)
				elif a == "Hydrant":
					pygame.time.delay(1000)
					death_count += 1
					menu(death_count)

		clock.tick(30)
		pygame.display.update()


def win(points):

	run = True
	while run:
		SCREEN.blit(BG, (0, 0))
		font = pygame.font.Font('freesansbold.ttf', 30)

		if points == 3000:
			text = font.render("Congratulations!", True, (250, 245, 225))
			kidnap = font.render("You have successfully abducted Fleur!", True, (250, 245, 225))
			kidnapRect = kidnap.get_rect()
			kidnapRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
			SCREEN.blit(kidnap, kidnapRect)
		textRect = text.get_rect()
		textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
		SCREEN.blit(text, textRect)
		SCREEN.blit(STANDING, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 75))
		SCREEN.blit(GIRL, (SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 + 120))
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				main()


def menu(death_count):
	global points
	run = True
	while run:

		SCREEN.blit(BG, (0, 0))
		font = pygame.font.Font('freesansbold.ttf', 30)

		if death_count == 0:
			text = font.render("Press any Key to Start", True, (250, 245, 225))
			save = font.render("Score 3000 to save Fleur", True, (250, 245, 225))
			saveRect = save.get_rect()
			saveRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
			SCREEN.blit(save, saveRect)
		elif death_count > 0:
			text = font.render("Press any Key to Restart", True, (250, 245, 225))
			score = font.render("Your Score: " + str(points), True, (250, 245, 225))
			scoreRect = score.get_rect()
			scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
			SCREEN.blit(score, scoreRect)

		textRect = text.get_rect()
		textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
		SCREEN.blit(text, textRect)

		SCREEN.blit(STANDING, (SCREEN_WIDTH // 2 - 33, SCREEN_HEIGHT // 2 + 75))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				main()


menu(death_count=0)
win(points=0)

