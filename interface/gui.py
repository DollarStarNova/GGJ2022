import pygame
from pygame._sdl2 import Window


DEFAULT_WINDOW_SCALE = .75

pygame.display.init()


class window():
    def __init__(self,
                 window_title: str = "GGJ2022",
                 window_width: int = pygame.display.get_desktop_sizes()[0][0] * DEFAULT_WINDOW_SCALE, window_height: int = pygame.display.get_desktop_sizes()[0][1] * DEFAULT_WINDOW_SCALE  # type: ignore -- Stop pylance nagging about get_desktop_sizes
                 ):
        self.window_width = window_width
        self.window_height = window_height
        self.window_title = window_title
        self.title_bar_font_colour = pygame.Color("#FFFFFF")

        self.main_window = self.create_parent_window()
        self.draw()
        pygame.display.update()

    def create_parent_window(self) -> pygame.surface.Surface:
        pw = pygame.display.set_mode([int(self.window_width), int(self.window_height)], flags=pygame.NOFRAME)
        pygame.display.set_caption(self.window_title)
        self.sdl2_pw = Window.from_display_module()  # Create an SDL2 window reference so we can move the window later  ------  HAHA NO... it doesn't move smoothly :/
        return pw

    def draw(self):
        if not hasattr(self, "window_bar"):
            self.draw_window_frame()
        self.main_window.blit(self.window_frame, (0, 0))

        if not hasattr(self, "title_bar"):
            self.draw_custom_title_bar()
        self.main_window.blit(self.title_bar, (0, 0))

    def draw_custom_title_bar(self) -> None:
        x = self.main_window.get_width()
        left = pygame.image.load("graphics\\menu_bar_left.png").convert_alpha()
        left_w = left.get_width()
        middle = pygame.image.load("graphics\\menu_bar_middle.png").convert_alpha()
        middle_w = middle.get_width()
        h = middle.get_height()
        right = pygame.image.load("graphics\\menu_bar_right.png").convert_alpha()
        right_w = right.get_width()

        blit_list = [(left, (int(0), int(0)))]
        i = left_w
        while i < (x - right_w):
            blit_list.append((middle, (int(i), int(0))))
            i += middle_w
        blit_list.append((right, (int(x - right_w), int(0))))

        final_image = pygame.Surface([x, h], pygame.SRCALPHA)
        final_image.blits(blit_list)

        self.title_bar = final_image
        self.title_bar_area = pygame.Rect((int(0), int(0), x, h))
        self.close_button_area = pygame.Rect((x - right_w + 39, 7, 54, 22))  # coordinates from ms paint !

    def draw_window_frame(self) -> None:
        x = self.main_window.get_width()
        y = self.main_window.get_height()
        left_edge = pygame.image.load("graphics\\window_edge_left.png").convert_alpha()

        right_edge = pygame.image.load("graphics\\window_edge_right.png").convert_alpha()
        right_edge_w = right_edge.get_width()
        edge_h = right_edge.get_height()

        left_bottom_edge = pygame.image.load("graphics\\window_edge_bottom_left.png").convert_alpha()
        left_bottom_edge_w = left_bottom_edge.get_width()

        right_bottom_edge = pygame.image.load("graphics\\window_edge_bottom_right.png").convert_alpha()
        right_bottom_edge_w = right_bottom_edge.get_width()

        middle_bottom_edge = pygame.image.load("graphics\\window_edge_bottom_middle.png").convert_alpha()
        middle_bottom_edge_w = middle_bottom_edge.get_width()
        bottom_edge_h = middle_bottom_edge.get_height()

        blit_list = [
            (left_bottom_edge, (int(0), int(y - bottom_edge_h))),
            (right_bottom_edge, (int(x - right_bottom_edge_w), int(y - bottom_edge_h))),
        ]
        i = left_bottom_edge_w
        while i < (x - right_bottom_edge_w):
            blit_list.append((middle_bottom_edge, (int(i), int(y - bottom_edge_h))))
            i += middle_bottom_edge_w

        i = 0
        while i < y - bottom_edge_h:
            blit_list.append((left_edge, (0, i)))
            blit_list.append((right_edge, (x - right_edge_w, i)))
            i += edge_h

        final_image = pygame.Surface([x, y], pygame.SRCALPHA)  # gives us a transparent surface by default, so we can draw our window frame over the content
        final_image.blits(blit_list)

        self.window_frame = final_image

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            collision_list = [self.close_button_area, self.title_bar_area]
            collision = pygame.Rect(event.pos, (1, 1)).collidelist(collision_list)

            if collision == 0:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            # elif collision == 1:
                # self.dragging_window = True
                # self.mouse_relative_to_window = pygame.mouse.get_pos()

                # if event.type == pygame.MOUSEBUTTONUP:
                #     if hasattr(self, "dragging_window") and self.dragging_window:
                #         x, y = self.sdl2_pw.position  # type: ignore
                #         mouse_x, mouse_y = pygame.mouse.get_pos()
                #         prev_mouse_x, prev_mouse_y = self.mouse_relative_to_window
                #         if mouse_x > prev_mouse_x:
                #             x = x + mouse_x - prev_mouse_x
                #         else:
                #             x = x - prev_mouse_x + mouse_x
                #         if mouse_y > prev_mouse_y:
                #             y = y + mouse_y - prev_mouse_y
                #         else:
                #             y = y - prev_mouse_y - mouse_y
                #         self.sdl2_pw.position = (x, y)

                # If you are reading this and know how to make dragging windows work smoothly, please tell me!

        # if event.type == pygame.MOUSEMOTION:
        #     x, y = self.sdl2_pw.position  # type: ignore
        #     # if event.buttons[0] and self.title_bar_area.collidepoint(event.pos):
        #     if not hasattr(self, "mouse_relative_to_window"):
        #         self.mouse_relative_to_window = pygame.mouse.get_pos()
        #     mouse_x, mouse_y = pygame.mouse.get_pos()
        #     prev_mouse_x, prev_mouse_y = self.mouse_relative_to_window
        #     if mouse_x > prev_mouse_x:
        #         x = x + mouse_x - prev_mouse_x
        #     else:
        #         x = x - prev_mouse_x + mouse_x
        #     if mouse_y > prev_mouse_y:
        #         y = y + mouse_y - prev_mouse_y
        #     else:
        #         y = y - prev_mouse_y - mouse_y
            # self.sdl2_pw.position = (x, y)

            #     if not hasattr(self, "last_move"):
            #         self.last_move = (0, 0)
            #     x, y = self.sdl2_pw.position  # type: ignore
            #     self.sdl2_pw.position = [x + self.last_move[0], y + self.last_move[1]]
            #     print(self.sdl2_pw.position)
            #     self.last_move = event.rel
            # pygame.event.post(pygame.event.Event(pygame.WINDOWMOVED, {"x": x + z, "y": y + a}))
