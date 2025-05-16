#!/usr/bin/env python3
import pygame
import time
import math

# Initialize pygame
pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode(
    (info.current_w, info.current_h),
    pygame.FULLSCREEN | pygame.NOFRAME
)
pygame.display.set_caption("AMR TEAM 1")

# Colors
background_color = (0, 0, 0)
text_color = (255, 255, 255)
accent_color = (0, 120, 255)  # Blue accent color

# Create a clock object to control frame rate
clock = pygame.time.Clock()
FPS = 60

# Main text setup
font_size = 200
font = pygame.font.Font(None, font_size)
text = "AMR TEAM 1"

# Animation parameters
animation_duration = 5  # seconds
start_time = time.time()
running = True

# Main animation loop
while running:
    current_time = time.time()
    elapsed = current_time - start_time
    
    # Exit if animation is complete or if there's a quit event
    if elapsed >= animation_duration:
        running = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    
    # Clear screen
    screen.fill(background_color)
    
    # Animation progress from 0 to 1
    progress = min(elapsed / animation_duration, 1.0)
    
    # Draw fancy background effects
    for i in range(10):
        radius = int(min(info.current_w, info.current_h) * (0.5 + 0.4 * math.sin(progress * math.pi * 2 + i * 0.2)))
        thickness = int(5 + 3 * math.sin(progress * math.pi * 3))
        alpha = int(80 + 30 * math.sin(progress * math.pi * 2))
        
        # Create a surface for the circle with alpha
        circle_surface = pygame.Surface((info.current_w, info.current_h), pygame.SRCALPHA)
        circle_color = (*accent_color, alpha)
        pygame.draw.circle(circle_surface, circle_color, (info.current_w // 2, info.current_h // 2), radius, thickness)
        screen.blit(circle_surface, (0, 0))
    
    # Text animation
    if progress < 0.3:
        # Fade in and zoom in
        alpha = int(255 * (progress / 0.3))
        scale = 0.5 + 1.5 * (progress / 0.3)
        text_surf = font.render(text, True, text_color)
        text_surf.set_alpha(alpha)
        text_rect = text_surf.get_rect()
        scaled_width = int(text_rect.width * scale)
        scaled_height = int(text_rect.height * scale)
        text_scaled = pygame.transform.smoothscale(text_surf, (scaled_width, scaled_height))
        text_rect = text_scaled.get_rect(center=(info.current_w // 2, info.current_h // 2))
        screen.blit(text_scaled, text_rect)
    
    elif progress < 0.8:
        # Pulsing effect
        pulse = 1.0 + 0.05 * math.sin((progress - 0.3) * 20)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect()
        scaled_width = int(text_rect.width * pulse)
        scaled_height = int(text_rect.height * pulse)
        text_scaled = pygame.transform.smoothscale(text_surf, (scaled_width, scaled_height))
        text_rect = text_scaled.get_rect(center=(info.current_w // 2, info.current_h // 2))
        screen.blit(text_scaled, text_rect)
        
        # Draw additional text elements
        subtitle_font = pygame.font.Font(None, 60)
        subtitle_text = "Autonomous Mobile Robotics"
        subtitle_surf = subtitle_font.render(subtitle_text, True, text_color)
        subtitle_alpha = int(255 * min((progress - 0.3) / 0.2, 1.0))
        subtitle_surf.set_alpha(subtitle_alpha)
        subtitle_rect = subtitle_surf.get_rect(center=(info.current_w // 2, info.current_h // 2 + 120))
        screen.blit(subtitle_surf, subtitle_rect)
    
    else:
        # Fade out
        alpha = int(255 * (1 - (progress - 0.8) / 0.2))
        text_surf = font.render(text, True, text_color)
        text_surf.set_alpha(alpha)
        text_rect = text_surf.get_rect(center=(info.current_w // 2, info.current_h // 2))
        screen.blit(text_surf, text_rect)
        
        subtitle_font = pygame.font.Font(None, 60)
        subtitle_text = "Autonomous Mobile Robotics"
        subtitle_surf = subtitle_font.render(subtitle_text, True, text_color)
        subtitle_surf.set_alpha(alpha)
        subtitle_rect = subtitle_surf.get_rect(center=(info.current_w // 2, info.current_h // 2 + 120))
        screen.blit(subtitle_surf, subtitle_rect)
    
    # Draw animated particles for visual effect
    for i in range(30):
        particle_x = info.current_w // 2 + int(math.cos(progress * 10 + i) * info.current_w * 0.4)
        particle_y = info.current_h // 2 + int(math.sin(progress * 8 + i) * info.current_h * 0.3)
        particle_size = int(5 + 3 * math.sin(progress * 5 + i))
        particle_alpha = int(150 + 100 * math.sin(progress * 3 + i * 0.5))
        
        particle_surface = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
        particle_color = (255, 255, 255, particle_alpha)
        pygame.draw.circle(particle_surface, particle_color, (particle_size, particle_size), particle_size)
        screen.blit(particle_surface, (particle_x - particle_size, particle_y - particle_size))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Clean up
pygame.quit()
