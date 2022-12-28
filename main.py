import os
import sys
import pygame
import sounddevice
import numpy as np
micInput = 0


def audio_callback(indata, frames, time, status):
    global micInput
    micInput = (int)(np.linalg.norm(indata) * 10)


def create_mask(surface, alpha):
    mask = pygame.mask.from_surface(surface)
    mask_surface = mask.to_surface()
    mask_surface.set_colorkey((0, 0, 0))
    a, b = mask_surface.get_size()
    for x in range(a):
        for y in range(b):
            if mask_surface.get_at((x, y))[0] != 0:
                mask_surface.set_at((x, y), (1, 1, 1, alpha))
    return mask_surface


def main():
    # VARS
    x = y = 5
    max_y = 10
    min_y = 20

    # ALPHA
    alpha = alpha_max = 180
    alpha_scaling = (int)(alpha_max/6)
    alpha_min = 0
    aux_timer = alpha_timer = 0
    min_speaking = 20
    min_swap = 90
    aux_swap_timer = swap_timer = 15

    # CHAR SCALE
    scale = 0.35

    # PYGAME
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((700, 900))
    screen.fill((0, 0, 255))
    pygame.display.flip()

    # CHAR SETUP
    """
        IDEA A PROBAR
        Hacer un arreglo con las dos o mas poses
        La idea es que sea segun modo en que use el personaje (hablar, en bass, dibujando, etc)
        existen los punteros 0 (idle), 1,2,3 .. como alternos para cuando el mic pesque el volumen para hablar

        char = [
            'speak0' = [superficie,mask], 
            'speak1 = [superficie,mask],
        ]

    """

    # CARGA DE ARCHIVOS HARDCODEADA
    dir1 = './src/offcar/speak0.png'
    dir2 = './src/offcar/speak1.png'
    dir3 = './src/offcar/speak2.png'
    dir4 = './src/offcar/speak3.png'

    # diccionario en que guardar todo
    test = {}

    # SPEAK0
    char = pygame.image.load(dir1)
    char = pygame.transform.scale(
        char, (char.get_width()*scale, char.get_height()*scale))
    char_mask = create_mask(char, alpha)
    test['speak0'] = {'surface': char, 'mask': char_mask}

    # SPEAK0
    char = pygame.image.load(dir2)
    char = pygame.transform.scale(
        char, (char.get_width()*scale, char.get_height()*scale))
    char_mask = create_mask(char, alpha)
    test['speak1'] = {'surface': char, 'mask': char_mask}

    char = pygame.image.load(dir3)
    char = pygame.transform.scale(
        char, (char.get_width()*scale, char.get_height()*scale))
    char_mask = create_mask(char, alpha)
    test['speak2'] = {'surface': char, 'mask': char_mask}

    char = pygame.image.load(dir4)
    char = pygame.transform.scale(
        char, (char.get_width()*scale, char.get_height()*scale))
    char_mask = create_mask(char, alpha)
    test['speak3'] = {'surface': char, 'mask': char_mask}

    # selected char
    selected = 'speak0'
    pointer = 1
    speakFlag = False

    #
    speakTimer = speakTimerDefault = 40

    screen.blit(test[selected]['surface'], (x, y))
    screen.blit(test[selected]['mask'], (x, y))
    pygame.display.flip()

    # SOUND STREAM
    stream = sounddevice.InputStream(callback=audio_callback)
    with stream:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 0
            key = pygame.key.get_pressed()
            if (key[pygame.K_ESCAPE]):
                return 0
            # MINIMO PARA HABLAR
            if (micInput > min_speaking):
                aux_swap_timer = swap_timer
                if (micInput > min_swap):
                    selected = 'speak'+str(pointer)
                    speakFlag = True
                aux_timer = alpha_timer
                if alpha > alpha_min:
                    alpha = alpha - alpha_scaling
                    # test[selected]['mask'].set_alpha(alpha)
                if y > max_y:
                    y = y - 2
            # SILENCE
            else:
                aux_swap_timer = aux_swap_timer - 1
                if aux_swap_timer <= 0:
                    selected = 'speak0'
                    # ROTAR PUNTERO PARA PROXIMA POSE DE HABLAR
                    speakTimer = speakTimer - 1
                    if speakFlag == True:
                        if (speakTimer < 0):
                            print('timer agotado, rotar')
                            if pointer == 1:
                                pointer = 2
                            elif pointer == 2:
                                pointer = 3
                            elif pointer == 3:
                                pointer = 1
                            speakTimer = speakTimerDefault

                        # print('vuela a idle, rotar pointer')
                        # print('pointer: '+str(pointer))
                        # if pointer == 1:
                            # pointer = 2
                        # elif pointer == 2:
                            # pointer = 3
                        # elif pointer == 3:
                            # pointer = 1
                        # print('pointer post change: '+str(pointer))
                    speakFlag = False
                aux_timer = aux_timer - 1
                if alpha < alpha_max and aux_timer <= 0:
                    alpha = alpha + alpha_scaling
                    # test[selected]['mask'].set_alpha(alpha)
                if y < min_y:
                    y = y + 2
            print('Speaktimer %s' % (speakTimer))
            test[selected]['mask'].set_alpha(alpha)
            screen.fill((0, 0, 255))
            screen.blit(test[selected]['surface'], (x, y))
            screen.blit(test[selected]['mask'], (x, y))
            pygame.display.update()
            clock.tick(30)


if __name__ == "__main__":
    val = main()
    print('Exiting main() with value %s' % val)
    pygame.quit()
