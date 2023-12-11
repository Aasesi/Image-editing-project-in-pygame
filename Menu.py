from InterfaceElement import ElementBase
from Commands import ElementType
from ImageClass import IEPImage


class CommandMenu:
    """
    A class representing a command menu.

    Attributes:
    - _sections: Dictionary storing elements and their associated commands.
    """
    def __init__(self):
        self._sections = {}

    def draw(self):
        """Draws all elements in the command menu."""
        for element in self._sections:
            element.draw()

    def check_events(self, event, pos):
        """
        Checks events for elements in the menu.

        Args:
        - event: The Pygame event to check.
        - pos: The position of the mouse.
        """
        for element in self._sections:
            element.check_events(event, pos)

    def add_element(self, element, command):
        """
        Adds an element with its associated command to the menu.

        Args:
        - element: The element to add.
        - command: The command associated with the element.
        """
        self._sections[element] = command

    def update(self, image: IEPImage):
        """
        Updates elements in the menu and executes commands if ready.

        Args:
        - image: An instance of IEPImage.
        """
        for section in self._sections:
            section.update()
            if section.ready:
                if section.value_type == ElementType.NUMERIC_VALUE:
                    self._sections[section].assign_data(section.return_elements)
                section.change_to_not_ready()
                image.execute_command(self._sections[section])


class Section(ElementBase):
    """
    A class representing a section in the menu.

    Attributes:
    - elements: A list of elements in the section.
    - name: The name of the section.
    - size: The number of elements in the section.
    - ready: Indicates if there was a change in the section.
    - value_type: The type of value the section holds.
    - return_elements: Dictionary storing return elements.
    """
    def __init__(self, screen, position, name, elements: list, value_type: ElementType):
        super().__init__(screen, position, name)
        self.elements: list = elements
        self.name = name
        self.size = len(self.elements)
        self.ready = False
        self.value_type = value_type
        self.return_elements = {}

        # Text information
        self.text_descr_color = (255, 255, 255)

    def draw(self):
        """Draws the section and its elements."""
        descr_text = self.font.render(self.name, False, self.text_descr_color)
        descr_text_rect = descr_text.get_rect(center=(self.pos[0], self.pos[1]))
        self.screen.blit(descr_text, descr_text_rect)
        for i in self.elements:
            i.draw()

    def add_element(self, element):
        """
        Adds an element to the section.

        Args:
        - element: The element to add.
        """
        self.elements.append(element)
        self.size += 1

    def check_events(self, event, mouse_pos,  *args, **kwargs):
        """
        Checks events for elements in the section.

        Args:
        - event: The Pygame event to check.
        - mouse_pos: The position of the mouse.
        """
        for i in self.elements:
            i.check_events(event, mouse_pos)

    def update(self):
        """Updates the section's elements."""
        for i in self.elements:
            if i.get_selection() is True:
                if self.value_type == ElementType.NUMERIC_VALUE:
                    self.return_elements[i.name] = i.value
                self.ready = True

    def change_to_not_ready(self):
        """Resets the section to not ready state."""
        self.ready = False
        self.return_elements = {}
