import pygame
from enum import Enum


class TypeOfInteraction(Enum):
    """
    An enumeration defining different types of interactions.

    Attributes:
    - DEFAULT: Default interaction (value: 1)
    - LOAD: Interaction type for loading (value: 2)
    - SAVE: Interaction type for saving (value: 3)
    - INSTANT_ACTION: Interaction type for instant action (value: 4)
    - UNDO_REDO: Interaction type for undo/redo (value: 5)
    """
    DEFAULT = 1
    LOAD = 2
    SAVE = 3
    INSTANT_ACTION = 4
    UNDO_REDO = 5


class ElementBase:
    """
    Base class for elements.

    Attributes:
    - name: The name of the element.
    - screen: The Pygame screen surface.
    - pos: The position of the element.
    - font: The font used for text rendering.
    - selected: Indicates if the element is selected.
    - type_name: The type of interaction associated with the element.
    """
    def __init__(self, screen, position: tuple, name):
        self.name = name
        self.screen = screen
        self.pos = position
        self.font = pygame.font.Font("Resources/Metamorphous-Regular.ttf", 15)
        self.selected = False
        self.type_name = TypeOfInteraction.DEFAULT

    def draw(self):
        """Method to draw the element."""
        pass

    def check_events(self, event, mouse_pos,  *args, **kwargs):
        """Method to check events for the element."""
        pass

    def is_hovered(self, mouse_pos):
        """
        Checks if the mouse cursor is hovering over the element.

        Args:
        - mouse_pos: The position of the mouse.
        """
        pass

    def get_selection(self):
        """
        Gets the selection status of the element and toggles the selection.

        Returns:
        - True if the element is selected, False otherwise.
        """
        if self.selected:
            self.selected = False
            return True
        else:
            return False
