import PIL.ImageEnhance
from PIL import Image, ImageFilter
from PIL import ImageOps
from abc import ABC, abstractmethod
from enum import Enum


class ElementType(Enum):
    """
    An enumeration defining different types of element values.

    Attributes:
    - NUMERIC_VALUE: Represents a numeric value (value: 1)
    - TOGGLE_VALUE: Represents a toggle value (value: 2)
    """
    NUMERIC_VALUE = 1
    TOGGLE_VALUE = 2


class Command(ABC):
    """
    An abstract base class defining a command interface.

    Attributes:
    - type: Represents the type of command.
    - save_needed: Indicates if saving the command is necessary.
    """
    def __init__(self, save=True):
        self.type = None
        self.save_needed = save

    @abstractmethod
    def execute(self, image):
        """
        Abstract method to execute the command on an image.

        Args:
        - image: The image object on which the command is to be executed.
        """
        pass


class NumericCommand(Command):
    """
    A class representing a numeric command.

    Attributes:
    - Inherits attributes from the Command class.
    - type: Represents the type of command (numeric value).
    - data: Stores data related to the command.
    """
    def __init__(self):
        super().__init__()
        self.type = ElementType.NUMERIC_VALUE
        self.data = {}

    @abstractmethod
    def execute(self, image):
        """
        Abstract method to execute the numeric command on an image.

        Args:
        - image: The image object on which the command is to be executed.
        """
        pass

    def assign_data(self, data):
        """
        Assigns data to the command.

        Args:
        - data: The data to be assigned to the command.
        """
        self.data = data


class ChangePixelSize(NumericCommand):
    """
    A class representing a command to change the size of an image.

    Attributes:
    - Inherits attributes from the NumericCommand class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to change the size of the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new resized image based on the provided data.
        """
        if "x" in self.data:
            new_image = image.resize((self.data["x"], image.height), resample=Image.BOX)
            return new_image
        if "y" in self.data:
            new_image = image.resize((image.width, self.data["y"]), resample=Image.BOX)
            return new_image


class SimpleBlur(Command):
    """
    A class representing a command to apply a simple blur effect to an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to apply a simple blur effect to the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with the applied blur effect.
        """
        new_image = image.filter(ImageFilter.BLUR)
        return new_image


class GaussianBlur(Command):
    """
    A class representing a command to apply Gaussian blur to an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to apply Gaussian blur to the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with the applied Gaussian blur effect.
        """
        # Adjust Radius
        new_image = image.filter(ImageFilter.GaussianBlur(radius=3))
        return new_image


class Sharpen(Command):
    """
    A class representing a command to apply sharpening to an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to apply sharpening to the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with the applied sharpening effect.
        """
        new_image = image.filter(ImageFilter.SHARPEN)
        return new_image


class EdgeEnhance(Command):
    """
    A class representing a command to enhance edges in an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to enhance edges in the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with the enhanced edges.
        """
        new_image = image.filter(ImageFilter.EDGE_ENHANCE)
        return new_image


class Emboss(Command):
    """
    A class representing a command to apply an emboss effect to an image.

    Attributes:
    - Inherits attributes from the Command class.
    """

    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to apply an emboss effect to the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with the emboss effect.
        """
        new_image = image.filter(ImageFilter.EMBOSS)
        return new_image


class Contour(Command):
    """
    A class representing a command to apply a contour effect to an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to apply a contour effect to the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with the applied contour effect.
        """
        new_image = image.filter(ImageFilter.CONTOUR)
        return new_image


class Detail(Command):
    """
    A class representing a command to enhance details in an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to enhance details in the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with enhanced details.
        """
        new_image = image.filter(ImageFilter.DETAIL)
        return new_image


class Smooth(Command):
    """
    A class representing a command to apply a smoothing effect to an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to apply a smoothing effect to the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with the applied smoothing effect.
        """
        new_image = image.filter(ImageFilter.SMOOTH)
        return new_image


class Saturation(NumericCommand):
    """
    A class representing a command to adjust the saturation level of an image.

    Attributes:
    - Inherits attributes from the NumericCommand class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to adjust the saturation level of the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with the adjusted saturation level.
        """
        converter = PIL.ImageEnhance.Color(image)
        new_image = converter.enhance(self.data["Saturation level"])
        return new_image


class Inversion(Command):
    """
    A class representing a command to invert colors in an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to invert colors in the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with inverted colors.
        """
        new_image = image.convert("RGB")
        new_image = ImageOps.invert(new_image)
        return new_image


class HistogramEqualization(Command):
    """
    A class representing a command to perform histogram equalization on an image.

    Attributes:
    - Inherits attributes from the Command class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to perform histogram equalization on the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with histogram equalization applied.
        """
        new_image = ImageOps.grayscale(image)
        new_image = ImageOps.equalize(new_image)
        return new_image


class ColorBalance(NumericCommand):
    """
    A class representing a command to adjust color balance in an image.

    Attributes:
    - Inherits attributes from the NumericCommand class.
    """
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """
        Executes the command to adjust color balance in the image.

        Args:
        - image: The image object on which the command is to be executed.

        Returns:
        - A new image with adjusted color balance.
        """
        new_image = image.convert("RGB")
        r, g, b = new_image.split()
        if "r" in self.data:
            r = r.point(lambda i: i * self.data["r"])
        if "g" in self.data:
            g = g.point(lambda i: i * self.data["g"])
        if "b" in self.data:
            b = b.point(lambda i: i * self.data["b"])
        new_image = Image.merge("RGB", (r, g, b))
        return new_image
