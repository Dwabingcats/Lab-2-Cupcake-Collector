import pygame
import asyncio  # 1. Import asyncio
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Load your image here (use lowercase relative path)
player_image = pygame.image.load("assets/verity.png")
player_image = pygame.transform.scale(player_image, (50, 50))  # Scale the image to 50x50 pixels
cupcake_image = pygame.image.load("assets/cupcake.jpeg")
cupcake_image = pygame.transform.scale(cupcake_image, (30, 30))  # Scale the image to 30x30 pixels

# Starting position, rotation, and gravity variables
cupcakes_collected = 0
x = 350
y = 250
velocity_y = 0
gravity = 0.67
speed = 5
jump = 15
angle = 0  # Track continuous rotation angle




on_ground = False
clock = pygame.time.Clock()

# Create a platform rect (x, y, width, height)
platform = pygame.Rect(200, 450, 200, 20)
platform2 = pygame.Rect(400, 300, 200, 20)

def respawn_cupcake():
    spawn_surfaces = [
        (50, 720, 520),
        (platform.left, platform.right - 30, platform.top - 30),   # platform 1
        (platform2.left, platform2.right - 30, platform2.top - 30) # platform 2
    ]
    x_min, x_max, y_pos = random.choice(spawn_surfaces)
    x_pos = random.randint(x_min, x_max)
    return x_pos, y_pos

# NEW: a list holding 10 cupcakes at random positions
cupcakes = []
for _ in range(10):
    cupcakex, cupcakey = respawn_cupcake()
    cupcakes.append(pygame.Rect(cupcakex, cupcakey, 30, 30))

# Place your game loop inside an async function
async def main():  # 2. Add 'async' before your main function definition
    global x, y, velocity_y, angle, on_ground, cupcakes_collected

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Controls & Movement ---
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= speed
            angle += 3  # Increase angle to roll continuously
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += speed
            angle -= 3  # Decrease angle to roll the other way

        player_rect = pygame.Rect(x, y, 50, 50)
        if player_rect.colliderect(platform):
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                x = platform.left - 50
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                x = platform.right

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if on_ground:
                velocity_y = -jump
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            velocity_y += 1

        if player_rect.colliderect(platform2):
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                x = platform2.left - 50
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                x = platform2.right

        # (removed the old cupcake check from here - it counted every cupcake twice)

        # --- Apply Gravity ---
        velocity_y += gravity
        y += velocity_y

        # Define player hitbox AFTER updating y position with gravity
        player_rect = pygame.Rect(x, y, 50, 50)

        on_ground = False
        if player_rect.colliderect(platform):
            if velocity_y > 0:
                y = platform.top - 50
                velocity_y = 0
                on_ground = True
            elif velocity_y < 0:
                y = platform.bottom
                velocity_y = 0

        if player_rect.colliderect(platform2):
                    if velocity_y > 0:
                        y = platform2.top - 50
                        velocity_y = 0
                        on_ground = True
                    elif velocity_y < 0:
                        y = platform2.bottom
                        velocity_y = 0


        if y >= 550:
            y = 550
            velocity_y = 0
            on_ground = True

        # NEW: loop through the list; [:] copy lets us remove while looping
        for cupcake in cupcakes[:]:
            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)
                cupcakes_collected += 1
                print(f"Cupcakes Collected: {cupcakes_collected}")

        # NEW: all 10 collected = you win
        if len(cupcakes) == 0:
            print("You collected all 10 cupcakes! You win!")
            running = False

        # --- Drawing Code ---
        screen.fill((0, 0, 0))

        # Draw platform
        pygame.draw.rect(screen, (255, 255, 255), platform)
        pygame.draw.rect(screen, (255, 255, 255), platform2)

        # Rotate player_image by current angle
        rotated_image = pygame.transform.rotate(player_image, angle)

        # Draw rotated_image on top of everything
        screen.blit(rotated_image, (x, y))
        # NEW: draw every cupcake left in the list
        for cupcake in cupcakes:
            screen.blit(cupcake_image, cupcake)
        clock.tick(60)  # Limit to 60 FPS

        pygame.display.flip()

        await asyncio.sleep(0)  # 3. CRITICAL: Add this at the VERY END of your while loop

# Run the game using asyncio
asyncio.run(main())  # 4. Initialize the loop