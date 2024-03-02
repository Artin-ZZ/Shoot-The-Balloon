import pygame
import random
import sys
import time

# Init Pygame
pygame.init()

# Set Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700  # Screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bob-Marley's Shoot The Balloon")

# Set Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load Background Image
background_image = pygame.image.load('bg.jpeg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
balloon_image = pygame.image.load('balloon.png')
cannon_image = pygame.image.load('crosshair.png')

# Set Game Variables
balloons = []
balloon_speed = 10  # Increase Balloon Speed Here
score = 0
missed_balloons = 0  # Track Missed Balloons
font = pygame.font.Font(None, 36)

# Set Level Variables
time_per_level = 2 * 60  # 2 Mins Per Match
start_time = time.time()

# Function To Create A New Balloon
def create_balloons(num_balloons):
    for _ in range(num_balloons):
        balloon_rect = balloon_image.get_rect()
        balloon_rect.x = random.randint(0, SCREEN_WIDTH - balloon_rect.width)
        balloon_rect.y = SCREEN_HEIGHT  # Start Balloons Below The Screen
        balloons.append(balloon_rect)

# Main Game Loop
clock = pygame.time.Clock()
running = True
while running:
    screen.blit(background_image, (0, 0))
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Update Crosshair Position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cannon_rect = cannon_image.get_rect(center=(mouse_x, mouse_y))
    
    # Check If The Player Clicks To Shoot Balloons
    if pygame.mouse.get_pressed()[0]:
        # Check If Cannon Hits Any Balloons
        for balloon in balloons[:]:
            if balloon.collidepoint((mouse_x, mouse_y)):
                balloons.remove(balloon)
                score += 1
    
    # Spawn Balloons At Random Intervals
    if time.time() - start_time >= 1:  # Change The Time Interval To 1
        num_balloons = random.randint(0, 3)  # Random Number Off Balloons Between 0 And 3
        create_balloons(num_balloons)
        start_time = time.time()
        
    # Move The Balloons
    for balloon in balloons[:]:
        balloon.y -= balloon_speed
        
        # Check If Balloon Is Off Screen
        if balloon.bottom < 0:
            balloons.remove(balloon)
            missed_balloons += 1  # Increment Missed Balloons
    
    # Draw Balloons
    for balloon in balloons:
        screen.blit(balloon_image, balloon)
        
    # Draw Cannon
    screen.blit(cannon_image, cannon_rect)
    
    # Display Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Display Time Left For The Current Level
    time_left = max(0, time_per_level - (time.time() - start_time))
    minutes = int(time_left) // 60
    seconds = int(time_left) % 60
    time_text = font.render(f"Time Left: {minutes:02} : {seconds:02}", True, BLACK)
    screen.blit(time_text, (10, 50))
    
    # Display Missed Balloons
    missed_text = font.render(f"Missed: {missed_balloons}/3", True, BLACK)
    screen.blit(missed_text, (10, 90))
    
    # Check If Game Over (3 Missed Balloons Or Time Runs Out)
    if missed_balloons >= 3 or time_left <= 0:
        game_over_text = font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        time.sleep(3)  # Display Game Over Message For 3 Seconds
        running = False
    
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
