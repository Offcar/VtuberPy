import os
import sys
import pygame
import sounddevice as sd
import numpy as np
micInput = 0

def audio_callback(indata,frames,time,status):
    global micInput 
    micInput = (int)(np.linalg.norm(indata) * 10)

def create_mask(surface,alpha):
    mask = pygame.mask.from_surface(surface)
    mask_surface = mask.to_surface()
    mask_surface.set_colorkey((0,0,0))
    a,b = mask_surface.get_size()
    for x in range(a):
        for y in range(b):
            if mask_surface.get_at((x,y))[0] != 0:
                mask_surface.set_at((x,y),(1,1,1,alpha))
    return mask_surface

def main():
    #VARS
    x = y = 50
    max_y = 40
    min_y = 50

    #ALPHA
    alpha = alpha_max = 180
    alpha_scaling = (int)(alpha_max/6)
    alpha_min = 0
    aux_timer = alpha_timer = 3
    min_speaking = 20

    #CHAR SCALE
    scale = 0.5

    #PYGAME
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800,800))
    screen.fill((0,0,255))
    pygame.display.flip()

    #CHAR
    selected = dir1 = './src/template/idle.png'
    char = pygame.image.load(dir1)
    char = pygame.transform.scale(char, (char.get_width()*scale, char.get_height()*scale))
    screen.blit(char,(x,y))
    char_mask = create_mask(char,alpha)
    screen.blit(char_mask,(x,y))
    pygame.display.flip()
    char_mask = create_mask(char,alpha)

    #SOUND STREAM
    stream = sd.InputStream(callback=audio_callback)
    with stream:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 0
            key = pygame.key.get_pressed()
            if(key[pygame.K_ESCAPE]):
                return 0
            if(micInput > min_speaking):
                aux_timer = alpha_timer
                if alpha > alpha_min:
                    alpha = alpha - alpha_scaling
                    char_mask.set_alpha(alpha)
                if y > max_y:
                    y = y - 2
            else:
                aux_timer = aux_timer - 1
                if alpha < alpha_max and aux_timer <= 0:
                    alpha = alpha + alpha_scaling
                    char_mask.set_alpha(alpha)
                if y < min_y:
                    y = y + 2
            screen.fill((0,0,255))
            screen.blit(char,(x,y))
            screen.blit(char_mask,(x,y))
            pygame.display.update()
            clock.tick(30)

if __name__ =="__main__":
    if not sys.argv:
        print(sys.argv)
    val = main()
    print('Exiting main() with value %s'%val)
    pygame.quit()

