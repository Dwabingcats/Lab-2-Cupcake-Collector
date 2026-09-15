import pygame
import asyncio  # 1. Import asyncio

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Load your image here (use lowercase relative path)
player_image = pygame.image.load("assets/verity.png")

# Place your game loop inside an async function
async def main():  # 2. Add 'async' before your main function definition
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # --- Your Game Logic & Drawing Code Here ---
        screen.fill((0, 0, 0)) 
        
        # Draw the image on screen at (x, y) coordinates
        screen.blit(player_image, (350, 250))
        
        pygame.display.flip()
        
        await asyncio.sleep(0)  # 3. CRITICAL: Add this at the VERY END of your while loop

# Run the game using asyncio
asyncio.run(main())  # 4. Initialize the loop