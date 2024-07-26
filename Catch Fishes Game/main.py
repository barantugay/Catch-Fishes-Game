import pygame
import random

pygame.init()

screen = pygame.display.set_mode((720, 960))
clock = pygame.time.Clock()

fisher_image = pygame.image.load("fisher.png")
fisher_position = fisher_image.get_rect(center=(360, 920))
spear_image = pygame.image.load("spear.png")
spear_position = spear_image.get_rect(center=(fisher_position.centerx - 16, fisher_position.centery - 32))
fish_images = [pygame.image.load(f"fish{i}.png") for i in range(1, 4)]
shark_image = pygame.image.load("shark.png")
shot_voice = pygame.mixer.Sound("shot.mp3")
shotOK_voice = pygame.mixer.Sound("shot ok.mp3")
levelUp_voice = pygame.mixer.Sound("Level Up.mp3")
youWin_voice = pygame.mixer.Sound("you win.mp3")
gameOver_voice = pygame.mixer.Sound("game over.mp3")

background_image = pygame.image.load("background.jpg")

shooting = False
sharks = []
fishes = []
level = 1
score = 0

myFont = pygame.font.SysFont("arialblack", 32)
myFont2 = pygame.font.SysFont("arialblack", 64)
myLevel = myFont.render(f"Level {level}", True, (244, 244, 244))
myScore = myFont.render(f"Score: {score}", True, (244, 244, 244))
level_position = myLevel.get_rect(center=(100, 40))
score_position = myScore.get_rect(center=(500, 40))

def placeFish(type_index):
    fish_position = fish_images[type_index].get_rect(topleft=(random.randint(0, 656), random.randint(80, 736)))
    fishes.append({
        'image': fish_images[type_index],
        'position': fish_position,
        'direction1': random.choice([-4, -3, -2, 2, 3, 4]),
        'direction2': random.choice([-4, -3, -2, 2, 3, 4])
    })

def addShark():
    shark_position = shark_image.get_rect(topleft=(random.randint(0, 592), random.randint(80, 714)))
    sharks.append({
        'position': shark_position,
        'direction1': random.choice([-4, -3, -2, 2, 3, 4]),
        'direction2': random.choice([-4, -3, -2, 2, 3, 4])
    })

def shot():
    global spear_position, shooting
    shot_voice.play()
    if not shooting:
        spear_position = spear_image.get_rect(center=(fisher_position.centerx - 12, fisher_position.centery - 64))
        shooting = True

def gameOver():
    global running
    if score != 100:
        myText = myFont2.render("GAME OVER", True, (255, 0, 0))
        myText_position = myText.get_rect(center=(360, 440))
        screen.blit(myText, myText_position)
        gameOver_voice.play()
        pygame.display.update()
        pygame.time.wait(3500)
        running = False
    else:
        myText = myFont2.render("YOU WIN", True, (0, 255, 0))
        myText_position = myText.get_rect(center=(360, 440))
        screen.blit(myText, myText_position)
        youWin_voice.play()
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

# Initialize game objects
for i in range(3):
    placeFish(i)
addShark()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shot()

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and fisher_position.x > 0:
        fisher_position.x -= 7
    elif key[pygame.K_RIGHT] and fisher_position.x < 656:
        fisher_position.x += 7

    if shooting:
        spear_position.y -= 20
        if spear_position.y < 0:
            shooting = False

    for fish in fishes:
        if spear_position.colliderect(fish['position']):
            score += 1
            shotOK_voice.play()
            myScore = myFont.render(f"Score: {score}", True, (244, 244, 244))
            fishes.remove(fish)

    if any(spear_position.colliderect(shark['position']) for shark in sharks):
        spear_position = spear_image.get_rect(center=(spear_position.x, spear_position.y - 64))
        screen.blit(background_image, (0, 0))
        pygame.draw.line(screen, (255, 0, 0), (0, 80), (720, 80), 5)
        pygame.draw.line(screen, (255, 0, 0), (0, 800), (720, 800), 5)
        pygame.draw.line(screen, (255, 0, 0), (0, 80), (0, 800), 5)
        pygame.draw.line(screen, (255, 0, 0), (720, 800), (720, 80), 5)
        screen.blit(fisher_image, fisher_position)
        if shooting:
            screen.blit(spear_image, spear_position)
        for fish in fishes:
            screen.blit(fish['image'], fish['position'])
        for shark in sharks:
            screen.blit(shark_image, shark['position'])
        screen.blit(myLevel, level_position)
        screen.blit(myScore, score_position)
        pygame.display.update()
        pygame.display.update()
        gameOver()


    if score == 3:
        addShark()
        for i in range(3):
            placeFish(i)
            placeFish(i)
        levelUp_voice.play()
        level += 1
        score = 6
        myScore = myFont.render(f"Score: {score}", True, (244, 244, 244))
        myLevel = myFont.render(f"Level {level}", True, (244, 244, 244))
    elif score == 12:
        addShark()
        for i in range(3):
            placeFish(i)
            placeFish(i)
            placeFish(i)
        levelUp_voice.play()
        level += 1
        score = 24
        myScore = myFont.render(f"Score: {score}", True, (244, 244, 244))
        myLevel = myFont.render(f"Level {level}", True, (244, 244, 244))
    elif score == 33:
        score = 100
        gameOver()

    for fish in fishes:
        fish['position'].y -= fish['direction1']
        fish['position'].x -= fish['direction2']
        if fish['position'].y <= 80 or fish['position'].y >= 720:
            fish['direction1'] = -fish['direction1']
        if fish['position'].x <= 0 or fish['position'].x >= 656:
            fish['direction2'] = -fish['direction2']

    for shark in sharks:
        shark['position'].y -= shark['direction1']
        shark['position'].x -= shark['direction2']
        if shark['position'].y <= 80 or shark['position'].y >= 714:
            shark['direction1'] = -shark['direction1']
        if shark['position'].x <= 0 or shark['position'].x >= 592:
            shark['direction2'] = -shark['direction2']

    screen.blit(background_image, (0, 0))
    pygame.draw.line(screen, (255, 0, 0), (0, 80), (720, 80), 5)
    pygame.draw.line(screen, (255, 0, 0), (0, 800), (720, 800), 5)
    pygame.draw.line(screen, (255, 0, 0), (0, 80), (0, 800), 5)
    pygame.draw.line(screen, (255, 0, 0), (720, 800), (720, 80), 5)
    screen.blit(fisher_image, fisher_position)
    if shooting:
        screen.blit(spear_image, spear_position)
    for fish in fishes:
        screen.blit(fish['image'], fish['position'])
    for shark in sharks:
        screen.blit(shark_image, shark['position'])
    screen.blit(myLevel, level_position)
    screen.blit(myScore, score_position)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
