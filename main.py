import pygame
import sys
import time
from interface.gui import window


def main():

    pygame.display.init()
    my_window = window()

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
                my_window.handle_event(event)
        time.sleep(0.001)  # one ms sleep to reduce CPU usage

    pygame.quit()
    sys.exit(0)


main()
