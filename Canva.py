import pygame
from InterfaceElement import ElementBase
from ImageClass import IEPImage


class Canvas(ElementBase):
    """
    A class that displays image onto the screen.

    Attributes:
    - screen: The Pygame screen surface
    - position: The position of the canvas
    - width: The width of the canvas
    - height: The height of the canvas
    - color: The background color of the canvas
    - name: The name of the canvas
    """
    def __init__(self, screen, position: tuple, width, height, color, name="Canvas"):
        super().__init__(screen, position, name)
        self.width = width
        self.height = height
        self.color = color
        self.main_image = None
        self.image_data = None
        self.has_image = False
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def is_hovered(self, mouse_pos):
        """
        Checks if the mouse is hovered over the image.

        Args:
        - mouse_pos: The position of the mouse.

        Returns:
        - True if the mouse is hovering over the image, False otherwise.
        """
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def get_display_pixels(self):
        """
        Gets the pixel data from the canvas.

        Returns:
        - Pixel data of the canvas in a 3D array.
        """
        sub_surface = self.screen.subsurface(self.rect)
        return pygame.surfarray.array3d(sub_surface)

    def draw(self):
        """
        Draws the canvas on the Pygame screen.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
        if self.has_image:
            x_pos = self.pos[0] + (self.rect.width/2) - (self.image_data.get_width()//2)
            y_pos = self.pos[1] + (self.rect.height/2) - (self.image_data.get_height()//2)
            self.screen.blit(self.image_data, (x_pos, y_pos))

    def add_image(self, image: IEPImage):
        """
        Adds an image to the canvas.

        Args:
        - image: An instance of IEPImage to be added to the canvas.
         """
        self.main_image = image
        im = image.pil_image.convert("RGBA")
        image_data = im.tobytes()
        image_dimensions = im.size
        self.image_data = pygame.image.fromstring(image_data, image_dimensions, "RGBA")
        self.has_image = True
        self.fit_image_on_screen()

    def update(self):
        """
        Updates the canvas.
        """
        if self.has_image:
            if self.main_image.changed:
                im = self.main_image.pil_image.convert("RGBA")
                image_data = im.tobytes()
                image_dimensions = im.size
                self.image_data = pygame.image.fromstring(image_data, image_dimensions, "RGBA")
                self.main_image.disable_changed()
                self.fit_image_on_screen()

    def fit_image_on_screen(self):
        """
        Fits the image on the screen if size of the image is bigger than the screen.
        """
        if (self.image_data.get_height() > self.rect.height) or (self.image_data.get_width() > self.rect.width):
            self.image_data = pygame.transform.scale(self.image_data, (self.rect.width, self.rect.height))
