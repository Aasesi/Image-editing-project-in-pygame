import pygame
import sys
from Settings import Settings
from Buttons import LoadButton, NormalButton, SaveButton, UndoButton, RedoButton
from Canva import Canvas
from Menu import CommandMenu, Section
from Commands import *
from Boxes import NumericalBox
from ImageClass import IEPImage
from InterfaceElement import TypeOfInteraction
from custom_exceptions import *


class ImageEdit:
    """
    The ImageEdit class manages an image editing application using Pygame and Pillow.

    Attributes:
    - settings (Settings): Holds the application's settings.
    - screen (pygame.Surface): Pygame window for the application.
    - clock (pygame.time.Clock): Manages the application's fps.
    - buttons (list): Stores various buttons for user interactions.
    - canvas (Canvas): Manages the drawing canvas within the application.
    - pil_image (Image): Placeholder for the loaded PIL image.
    - image (IEPImage): Manages the image editing functionalities.
    - menus (dict): Stores different menus for the application.
    - current_menu: Current menu in use.
    """
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("ImageEdit")
        self.icon = pygame.image.load("Resources/icon.png")
        pygame.display.set_icon(self.icon)
        self.buttons = []
        self.canvas = Canvas(self.screen, self.settings.canvas_pos, 1100, 900, (100, 100, 100))
        self.pil_image: Image = None
        self.image = IEPImage()
        self.menus = {}
        self.current_menu = None

    def run_app(self):
        """
        Runs the main application loop handling events, updates, and rendering.
        """
        while True:
            self.check_events()
            self.update()
            self.render()

    def load_elements(self):
        """
         Loads various UI elements like buttons and menus required for the application.
        """
        self.buttons.append(LoadButton(self.screen, (70, 225), button_image="Resources/load_button.png"))
        self.buttons.append(SaveButton(self.screen, (70, 625), button_image="Resources/save_button.png"))

        # Resize
        self.buttons.append(NormalButton(self.screen, (70, 325), "Resize",
                                         button_image="Resources/resize_button.png"))
        self.menus["Resize"] = CommandMenu()
        self.menus["Resize"].add_element(Section(self.screen, (1400, 125), "Pixel size",
                                                 [NumericalBox(self.screen, (1310, 160), 70,
                                                               30, "x", 100, 1),
                                                  NumericalBox(self.screen, (1410, 160), 70, 30,
                                                               "y", 1100, 900)],
                                                 ElementType.NUMERIC_VALUE), ChangePixelSize())

        # Filters
        self.buttons.append(NormalButton(self.screen, (70, 425), "Filters",
                                         button_image="Resources/filters_button.png"))
        self.menus["Filters"] = CommandMenu()
        self.menus["Filters"].add_element(Section(self.screen, (1400, 125), "Blur",
                                                  [NormalButton(self.screen, (1369, 140), "Simple Blur")],
                                                  ElementType.TOGGLE_VALUE), SimpleBlur())
        self.menus["Filters"].add_element(Section(self.screen, (1400, 225), "Edge enhance",
                                                  [NormalButton(self.screen, (1369, 240), "Edge enhance")],
                                                  ElementType.TOGGLE_VALUE), EdgeEnhance())
        self.menus["Filters"].add_element(Section(self.screen, (1400, 325), "Emboss",
                                                  [NormalButton(self.screen, (1369, 340), "Emboss")],
                                                  ElementType.TOGGLE_VALUE), Emboss())
        self.menus["Filters"].add_element(Section(self.screen, (1400, 425), "Contour",
                                                  [NormalButton(self.screen, (1369, 440), "Contour")],
                                                  ElementType.TOGGLE_VALUE), Contour())
        self.menus["Filters"].add_element(Section(self.screen, (1400, 525), "Detail",
                                                  [NormalButton(self.screen, (1369, 540), "Detail")],
                                                  ElementType.TOGGLE_VALUE), Detail())
        self.menus["Filters"].add_element(Section(self.screen, (1400, 625), "Smooth",
                                                  [NormalButton(self.screen, (1369, 640), "Smooth")],
                                                  ElementType.TOGGLE_VALUE), Smooth())

        # Color interactions
        self.buttons.append(NormalButton(self.screen, (70, 525), "Color",
                                         button_image="Resources/color_button.png"))
        self.menus["Color"] = CommandMenu()
        self.menus["Color"].add_element(Section(self.screen, (1400, 125), "Saturation",
                                                [NumericalBox(self.screen, (1365, 160), 70,
                                                              30, "Saturation level", 100, 0)],
                                                ElementType.NUMERIC_VALUE), Saturation())
        self.menus["Color"].add_element(Section(self.screen, (1400, 225), "Inversion of colors",
                                                [NormalButton(self.screen, (1369, 240),
                                                              "Inversion")], ElementType.TOGGLE_VALUE), Inversion())
        self.menus["Color"].add_element(Section(self.screen, (1400, 325), "Histogram equalization",
                                                [NormalButton(self.screen, (1369, 340),
                                                              "equalization")], ElementType.TOGGLE_VALUE),
                                        HistogramEqualization())
        self.menus["Color"].add_element(Section(self.screen, (1400, 425), "Color Balance",
                                                [NumericalBox(self.screen, (1310, 460), 70,
                                                              30, "r", 100, 0),
                                                 NumericalBox(self.screen, (1410, 460), 70,
                                                              30, "g", 100, 0),
                                                 NumericalBox(self.screen, (1365, 525), 70,
                                                              30, "b", 100, 0)],
                                                ElementType.NUMERIC_VALUE), ColorBalance())

        # Undo/Redo buttons
        self.buttons.append(UndoButton(self.screen, (148, 25), "Undo", button_image="Resources/undo_button.png"))
        self.buttons.append(RedoButton(self.screen, (1300, 25), "Redo", button_image="Resources/redo_button.png"))

    def check_events(self):
        """
        Handles Pygame events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_events(event, pos)
                try:
                    if button.get_selection():
                        if button.type_name == TypeOfInteraction.LOAD:
                            self.image.assign_image(button.load_image())
                            self.canvas.add_image(self.image)
                        elif button.type_name == TypeOfInteraction.SAVE:
                            button.save_image(self.image)
                        elif button.type_name == TypeOfInteraction.UNDO_REDO:
                            button.do_action(self.image)
                        elif button.type_name == TypeOfInteraction.DEFAULT:
                            self.current_menu = self.menus[button.name]
                except NoFileSelectedError as e:
                    print(e)
                if self.current_menu is not None:
                    self.current_menu.check_events(event, pos)

    def render(self):
        """
        Handles rendering.
        """
        self.screen.fill(self.settings.bg_color)
        for button in self.buttons:
            button.draw()
        if self.current_menu is not None:
            self.current_menu.draw()
        self.canvas.draw()
        pygame.display.update()
        self.clock.tick(60)

    def update(self):
        """
        Updates the application state
        """
        if self.current_menu is not None:
            try:
                self.current_menu.update(self.image)
            except NoImageError as e:
                print(e)
        self.canvas.update()
