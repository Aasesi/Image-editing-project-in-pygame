from PIL import Image
from custom_exceptions import NoImageError


class IEPImage:
    """
    A class representing an image object.

    Attributes:
    - path_file: The file path of the image.
    - pil_image: The PIL image object.
    - changed: Indicates if the image has been modified.
    - changes_history: History of changes made to the image.
    - size_history: History of image sizes.
    - history_index: Index to track the history of changes made to the image.
    """
    def __init__(self):
        self.path_file = ""
        self.pil_image = None
        self.changed = False
        self.changes_history = []
        self.size_history = []
        self.history_index = -1

    def assign_image(self, path):
        """
        Assigns an image to the object.

        Args:
        - path: The file path of the image to be assigned.
        """
        self.path_file = path
        self.pil_image = Image.open(path)
        self.pil_image = self.pil_image.convert("RGBA")
        self.changes_history.append(self.pil_image.getdata())
        self.size_history.append(self.pil_image.size)
        self.history_index += 1

    def create_new_image(self, new_data):
        """
        Creates a new image based on the data.

        Args:
        - new_data: The new data to create the image.
        """
        self.pil_image.close()
        self.pil_image = Image.fromarray(new_data.astype('uint8'))

    def save_image(self, path):
        """
        Saves the current image to a file.

        Args:
        - path: The file path to save the image.
        """
        self.pil_image.save(path)

    def execute_command(self, command):
        """
        Executes a command on the image.

        Args:
        - command: The command to be executed on the image.
        """
        if self.pil_image is None:
            raise NoImageError("No image is being used!")
        self.changed = True
        self.pil_image = command.execute(self.pil_image)
        if command.save_needed:
            self.save_current_image_data()

    def disable_changed(self):
        """Disables the 'changed' flag."""
        self.changed = False

    def save_current_image_data(self):
        """
        Saves the current image data to the history.
        """
        self.history_index += 1
        if len(self.changes_history) > self.history_index:
            self.changes_history = self.changes_history[:self.history_index+1]
            pixel_data = self.pil_image.getdata()
            self.changes_history.append(pixel_data)
            self.size_history.append(self.pil_image.size)
        else:
            pixel_data = self.pil_image.getdata()
            self.changes_history.append(pixel_data)
            self.size_history.append(self.pil_image.size)

    def undo_image(self):
        """
        Undo the last image change.
        """
        if self.history_index != 0:
            self.history_index -= 1
            new_image = Image.new('RGBA', self.size_history[self.history_index])
            new_image.putdata(self.changes_history[self.history_index])
            self.changed = True
            self.pil_image = new_image

    def redo_image(self):
        """
        Redo the last image change.
        """
        if (self.history_index + 1) < len(self.changes_history):
            self.history_index += 1
            new_image = Image.new('RGBA', self.size_history[self.history_index])
            new_image.putdata(self.changes_history[self.history_index])
            self.changed = True
            self.pil_image = new_image
