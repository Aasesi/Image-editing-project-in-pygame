from InterfaceElement import ElementBase
import pygame


class NumericalBox(ElementBase):
    def __init__(self, screen, position: tuple, width: int, height: int, name: str, max_value, min_value,
                 starting_value: int = 0, color: tuple = (182, 214, 210), outline_color: tuple = (142, 165, 163)):
        super().__init__(screen, position, name)

        # Box data
        self.value_in_string: str = "0"
        self.value = starting_value
        self.max_value = max_value
        self.min_value = min_value
        self.max_number_of_letters = 5
        self.active = False

        # Rectangle data
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.color = color

        # Outline info
        self.outline_color = outline_color

        # Text data
        self.text_color = (255, 255, 255)
        self.text_descr_color = (255, 255, 255)
        self.value_text = self.font.render(self.value_in_string, False, self.text_color)
        self.value_text_rect = self.value_text.get_rect(
            center=(self.pos[0] + (self.width // 2), self.pos[1] + (self.height // 2)))
        self.descr_text = self.font.render(self.name, False, self.text_descr_color)
        self.descr_text_rect = self.descr_text.get_rect(center=(self.pos[0] + self.width/2, self.pos[1]-10))

    def draw(self):
        # Main rect
        pygame.draw.rect(self.screen, self.color, self.rect)

        # Outline rect
        pygame.draw.rect(self.screen, self.outline_color, self.rect, 3)

        value_text = self.font.render(self.value_in_string, False, self.text_color)
        value_text_rect = value_text.get_rect(
            center=(self.pos[0] + (self.width // 2), self.pos[1] + (self.height // 2)))
        descr_text = self.font.render(self.name, False, self.text_descr_color)
        descr_text_rect = descr_text.get_rect(center=(self.pos[0] + self.width / 2, self.pos[1] - 10))

        # Draw text
        self.screen.blit(value_text, value_text_rect)
        self.screen.blit(descr_text, descr_text_rect)

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def check_events(self, event, mouse_pos, *args, **kwargs):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(mouse_pos):
            if self.active:
                self.active = False
            else:
                self.active = True
                self.value_in_string = ""
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = False
        elif self.active and event.type == pygame.KEYDOWN:
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                self.value_in_string = self.value_in_string[:-1]
            # Check for a number
            elif pygame.K_0 <= event.key <= pygame.K_9:
                if len(self.value_in_string) < self.max_number_of_letters:
                    self.value_in_string += event.unicode
            elif event.key == pygame.K_RETURN:
                self.value = int(self.value_in_string)
                self.active = False
                self.selected = True
            else:
                pass


class Checkbox(ElementBase):
    def __init__(self, screen, position: tuple, name, width: int, height: int, value_name: str,
                 color: tuple = (182, 214, 210), outline_color: tuple = (142, 165, 163)):
        super().__init__(screen, position, name)

        # Box info
        self.value_name = value_name
        self.normal_color = color
        self.active_color = self.normal_color

        # Rect info
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

        # Outline info
        self.outline_color = outline_color

        # Text info
        self.text_descr_color = (71, 71, 71)
        self.descr_text = self.font.render(self.value_name, False, self.text_descr_color)
        self.descr_text_rect = self.descr_text.get_rect(center=(self.pos[0] + self.width / 2, self.pos[1] - 10))

    def check_events(self, event, mouse_pos,  *args, **kwargs):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(mouse_pos):
            if self.selected:
                self.selected = False
            else:
                self.selected = True
            self.change_color()

    def change_color(self):
        if self.selected:
            self.active_color = (0, 0, 0)
        else:
            self.active_color = self.normal_color

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def draw(self):
        # Main rect
        pygame.draw.rect(self.screen, self.active_color, self.rect)

        # Outline rect
        pygame.draw.rect(self.screen, self.outline_color, self.rect, 3)

        # Draw text
        self.screen.blit(self.descr_text, self.descr_text_rect)
