#!/usr/bin/env python3
import pygame
import sys
import time
import math
import os

# Force hardware acceleration and disable problematic subsystems
os.environ['SDL_VIDEODRIVER'] = 'x11'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Hide pygame welcome message
os.environ['DBUS_FATAL_WARNINGS'] = '0'  # Prevent D-Bus warnings from being fatal

# Safest approach to initialize pygame for system services
pygame.display.init()
pygame.font.init()

# Get the display info safely
try:
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
except:
    # Fallback to common resolution if info can't be obtained
    WIDTH, HEIGHT = 1920, 1080

# Setup fullscreen display with error handling
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
except pygame.error:
    try:
        # Try again with just FULLSCREEN
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    except pygame.error:
        # Last resort - windowed mode at full resolution
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set window title (even though it won't be visible in fullscreen)
pygame.display.set_caption("AMR TEAM 1")

# Colors
BACKGROUND = (0, 0, 0)  # Black
TEXT_COLOR = (255, 255, 255)  # White
ACCENT_COLOR = (0, 120, 255)  # Blue

# Create a robust clock object for timing
clock = pygame.time.Clock()
FPS = 60

# Animation settings
start_time = time.time()
duration = 5.0  # seconds

# Font setup with fallbacks
try:
    main_font = pygame.font.Font(None, min(200, HEIGHT // 5))  # Scale font for different resolutions
    sub_font = pygame.font.Font(None, min(60, HEIGHT // 15))
except pygame.error:
    # Fallback to system fonts if pygame default font fails
    fonts = pygame.font.get_fonts()
    if fonts:
        try:
            main_font = pygame.font.SysFont(fonts[0], min(200, HEIGHT // 5))
            sub_font = pygame.font.SysFont(fonts[0], min(60, HEIGHT // 15))
        except:
            # If all else fails, exit gracefully
            print("Fatal error: Cannot initialize fonts")
            pygame.quit()
            sys.exit(1)

# Main animation loop with robust error handling
running = True
while running:
    try:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        # Calculate animation time and exit if duration exceeded
        current_time = time.time()
        elapsed = current_time - start_time
        if elapsed >= duration:
            running = False
            continue
        
        # Animation progress from 0 to 1
        progress = min(elapsed / duration, 1.0)
        
        # Clear screen
        screen.fill(BACKGROUND)
        
        # Draw animated background circles
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        for i in range(5):
            radius = int(min(WIDTH, HEIGHT) * 0.4 * (0.6 + 0.4 * math.sin(progress * math.pi * 2 + i * 0.5)))
            thickness = max(1, int(4 + 2 * math.sin(progress * math.pi * 3)))
            pygame.draw.circle(screen, ACCENT_COLOR, (center_x, center_y), radius, thickness)
        
        # Text animations
        text_scale = 1.0 + 0.05 * math.sin(progress * math.pi * 4)
        
        # Main title with animation
        if progress < 0.3:
            # Fade in effect
            alpha = int(255 * (progress / 0.3))
            main_text = main_font.render("AMR TEAM 1", True, TEXT_COLOR)
            main_rect = main_text.get_rect(center=(center_x, center_y))
            
            # Apply alpha
            temp = pygame.Surface(main_text.get_size(), pygame.SRCALPHA)
            temp.blit(main_text, (0, 0))
            temp.set_alpha(alpha)
            screen.blit(temp, main_rect)
            
        elif progress > 0.8:
            # Fade out effect
            alpha = int(255 * (1 - (progress - 0.8) / 0.2))
            main_text = main_font.render("AMR TEAM 1", True, TEXT_COLOR)
            main_rect = main_text.get_rect(center=(center_x, center_y))
            
            # Apply alpha
            temp = pygame.Surface(main_text.get_size(), pygame.SRCALPHA)
            temp.blit(main_text, (0, 0))
            temp.set_alpha(alpha)
            screen.blit(temp, main_rect)
            
        else:
            # Normal display with slight pulsing
            main_text = main_font.render("AMR TEAM 1", True, TEXT_COLOR)
            text_width, text_height = main_text.get_size()
            scaled_width, scaled_height = int(text_width * text_scale), int(text_height * text_scale)
            
            # Only scale if it makes sense
            if abs(text_scale - 1.0) > 0.01:
                try:
                    main_text = pygame.transform.smoothscale(main_text, (scaled_width, scaled_height))
                except:
                    # Skip scaling if it fails
                    pass
                    
            main_rect = main_text.get_rect(center=(center_x, center_y))
            screen.blit(main_text, main_rect)
        
        # Subtitle with separate fade timings
        if progress > 0.2 and progress < 0.9:
            subtitle_alpha = int(255 * min((progress - 0.2) / 0.2, 1.0))
            if progress > 0.7:
                subtitle_alpha = int(subtitle_alpha * (1 - (progress - 0.7) / 0.2))
                
            sub_text = sub_font.render("Autonomous Mobile Robotics", True, TEXT_COLOR)
            sub_rect = sub_text.get_rect(center=(center_x, center_y + 100))
            
            # Apply alpha
            temp = pygame.Surface(sub_text.get_size(), pygame.SRCALPHA)
            temp.blit(sub_text, (0, 0))
            temp.set_alpha(subtitle_alpha)
            screen.blit(temp, sub_rect)
        
        # Simple particle effects
        for i in range(15):
            angle = progress * 10 + i * (math.pi * 2 / 15)
            distance = 200 + 50 * math.sin(progress * 5 + i)
            x = center_x + int(math.cos(angle) * distance)
            y = center_y + int(math.sin(angle) * distance)
            size = int(3 + 2 * math.sin(progress * 8 + i))
            
            pygame.draw.circle(screen, TEXT_COLOR, (x, y), size)
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
        
    except Exception as e:
        print(f"Error in animation loop: {e}")
        # Try to continue despite errors
        time.sleep(0.1)

# Ensure pygame quits cleanly
pygame.quit()
sys.exit(0)
