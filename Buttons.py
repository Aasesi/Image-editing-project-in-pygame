import tkinter as tk
import pygame
from tkinter import filedialog
from InterfaceElement import ElementBase, TypeOfInteraction
from custom_exceptions import NoFileSelectedError


class NormalButton(ElementBase):
    """
    A class representing a normal button element.

    Attributes:
    - Inherits attributes from ElementBase.
    """
    def __init__(self, screen, position: tuple, name: str, button_image="Resources/button.png"):
        super().__init__(screen, position, name)

        # Rect info
        self.image = pygame.image.load(button_image)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def check_events(self, event, pos, *args, **kwargs):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(pos):
            self.selected = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class LoadButton(ElementBase):
    """
    A class representing a load button element.

    Attributes:
    - Inherits attributes from ElementBase.
    """
    def __init__(self, screen, position: tuple, name="Load", path_to_image=None, button_image="Resources/button.png"):
        super().__init__(screen, position, name)
        self.path_to_image = path_to_image
        self.type_name = TypeOfInteraction.LOAD

        # Rect info
        self.image = pygame.image.load(button_image)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def check_events(self, event, pos, *args, **kwargs):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(pos):
            window = tk.Tk()
            window.withdraw()
            path_to_file = filedialog.askopenfilename(title="Select an image",
                                                      filetypes=[
                                                          ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")])
            self.path_to_image = path_to_file
            self.selected = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def load_image(self):
        """
        Loads an image and returns its file path.

        Raises:
        - NoFileSelectedError: If no file path is selected.

        Returns:
        - The path to the loaded image file.
        """
        if self.path_to_image == "":
            raise NoFileSelectedError("File was not selected.")
        self.selected = False
        return self.path_to_image


class SaveButton(ElementBase):
    """
    A class representing a save button element.

    Attributes:
    - Inherits attributes from ElementBase.
    """
    def __init__(self, screen, position: tuple, name="Save", button_image="Resources/button.png"):
        super().__init__(screen, position, name)
        self.path_save_file: str = ""
        self.type_name = TypeOfInteraction.SAVE

        # Rect info
        self.image = pygame.image.load(button_image)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def check_events(self, event, pos, *args, **kwargs):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(pos):
            window = tk.Tk()
            window.withdraw()
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            self.path_save_file = file_path
            self.selected = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def save_image(self, image):
        """
        Saves the image to the specified file path.

        Args:
        - image: An image object.

        Raises:
        - NoFileSelectedError: If no file path is selected.

        """
        if self.path_save_file == "":
            raise NoFileSelectedError("File was not selected.")
        self.selected = False
        image.save_image(self.path_save_file)


class InstantActionButton(ElementBase):
    """
    A class representing an instant action button element.

    Attributes:
    - Inherits attributes from ElementBase.
    """
    def __init__(self, screen, position: tuple, command, name, button_image="Resources/button.png"):
        super().__init__(screen, position, name)
        self.command = command
        self.type_name = TypeOfInteraction.INSTANT_ACTION

        # Rect info
        self.image = pygame.image.load(button_image)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def check_events(self, event, pos, *args, **kwargs):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(pos):
            self.selected = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def do_command(self, image):
        """Executes command assigned to the class

        Args:
        - image: An image object of IEPImage.

        """
        self.selected = False
        image.execute_command(self.command)


class UndoButton(ElementBase):
    """
    A class representing an undo button element.

    Attributes:
    - Inherits attributes from ElementBase.
    """
    def __init__(self, screen, position: tuple, name, button_image="Resources/undo_button.png"):
        super().__init__(screen, position, name)
        self.type_name = TypeOfInteraction.UNDO_REDO

        # Rect info
        self.image = pygame.image.load(button_image)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def check_events(self, event, pos, *args, **kwargs):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(pos):
            self.selected = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def do_action(self, image):
        """
        Performs the action to undo the last image change.

        Args:
        - image: An image object.

        """
        image.undo_image()
        self.selected = False


class RedoButton(ElementBase):
    """
    A class representing a redo button element.

    Attributes:
    - Inherits attributes from ElementBase.
    """
    def __init__(self, screen, position: tuple, name, button_image="Resources/redo_button.png"):
        super().__init__(screen, position, name)
        self.type_name = TypeOfInteraction.UNDO_REDO

        # Rect info
        self.image = pygame.image.load(button_image)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def check_events(self, event, pos, *args, **kwargs):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(pos):
            self.selected = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def do_action(self, image):
        """
        Performs the action to redo the last image change.

        Args:
        - image: An image object.

        """
        image.redo_image()
        self.selected = False
