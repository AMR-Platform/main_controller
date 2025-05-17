#!/usr/bin/env python3
import pygame
import time
import math
import os

# Set environment variables to prevent D-Bus errors
os.environ['SDL_VIDEODRIVER'] = 'x11'

# Basic initialization with error handling
pygame.init()
pygame.font.init()  # Explicitly initialize font

# Create a simpler version that should be more compatible
try:
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
except:
    # Fallback to windowed mode if fullscreen fails
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))

# Colors
background_color = (0, 0, 0)
text_color = (255, 255, 255)
accent_color = (0, 120, 255)

# Clock for controlling framerate
clock = pygame.time.Clock()
FPS = 60

# Text setup
main_font = pygame.font.Font(None, 180)
subtitle_font = pygame.font.Font(None, 60)

# Animation duration
duration = 5.0  # seconds
start_time = time.time()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    
    # Calculate animation progress
    elapsed = time.time() - start_time
    if elapsed >= duration:
        running = False
        continue
    
    progress = elapsed / duration
    
    # Clear screen
    screen.fill(background_color)
    
    # Draw simplified animated background
    for i in range(5):  # Reduced number of circles
        radius = int(min(width, height) * 0.4 * (0.6 + 0.4 * math.sin(progress * math.pi * 2 + i * 0.5)))
        thickness = max(1, int(4 + 2 * math.sin(progress * math.pi * 3)))
        pygame.draw.circle(screen, accent_color, (width // 2, height // 2), radius, thickness)
    
    # Main text animation (simpler version)
    if progress < 0.2:
        # Fade in
        alpha = int(255 * (progress / 0.2))
        size = int(180 * (0.5 + 0.5 * (progress / 0.2)))
        main_font = pygame.font.Font(None, size)
    elif progress > 0.8:
        # Fade out
        alpha = int(255 * (1 - (progress - 0.8) / 0.2))
    else:
        # Full visibility with slight pulsing
        alpha = 255
        pulse = 1.0 + 0.05 * math.sin(progress * 20)
        main_font = pygame.font.Font(None, int(180 * pulse))
    
    # Render main text
    main_text = main_font.render("AMR TEAM 1", True, text_color)
    main_rect = main_text.get_rect(center=(width // 2, height // 2))
    
    # Create a temporary surface for alpha blending if needed
    if alpha < 255:
        temp_surface = pygame.Surface(main_text.get_size(), pygame.SRCALPHA)
        temp_surface.fill((255, 255, 255, 0))
        temp_surface.blit(main_text, (0, 0))
        temp_surface.set_alpha(alpha)
        screen.blit(temp_surface, main_rect)
    else:
        screen.blit(main_text, main_rect)
    
    # Subtitle text (appears after main text starts showing)
    if progress > 0.3:
        subtitle_alpha = int(255 * min((progress - 0.3) / 0.2, 1.0))
        if progress > 0.8:
            subtitle_alpha = int(subtitle_alpha * (1 - (progress - 0.8) / 0.2))
        
        subtitle_text = subtitle_font.render("Autonomous Mobile Robotics", True, text_color)
        subtitle_rect = subtitle_text.get_rect(center=(width // 2, height // 2 + 100))
        
        # Alpha blending for subtitle
        if subtitle_alpha < 255:
            sub_surface = pygame.Surface(subtitle_text.get_size(), pygame.SRCALPHA)
            sub_surface.fill((255, 255, 255, 0))
            sub_surface.blit(subtitle_text, (0, 0))
            sub_surface.set_alpha(subtitle_alpha)
            screen.blit(sub_surface, subtitle_rect)
        else:
            screen.blit(subtitle_text, subtitle_rect)
    
    # Simple particle effects (just a few to avoid performance issues)
    for i in range(10):  # Reduced number of particles
        angle = progress * 10 + i * (math.pi * 2 / 10)
        distance = 200 + 50 * math.sin(progress * 5 + i)
        x = width // 2 + int(math.cos(angle) * distance)
        y = height // 2 + int(math.sin(angle) * distance)
        size = int(3 + 2 * math.sin(progress * 8 + i))
        
        pygame.draw.circle(screen, text_color, (x, y), size)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Clean up
pygame.quit()
