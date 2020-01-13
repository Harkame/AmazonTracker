import os


class Product:
    def __init__(self):
        self.code = ""
        self.title = ""
        self.price = 0.0
        self.url = ""
        self.available = False
        self.reduction = False

    def __str__(self):
        pass

    def __str__(self):
        str = ""

        str += "Code :"
        str += self.code
        str += os.linesep
        str += os.linesep

        str += "Title : "
        str += self.title
        str += os.linesep
        str += os.linesep

        str += "Price : "
        str += self.price
        str += os.linesep
        str += os.linesep

        str += "Url : "
        str += self.url
        str += os.linesep
        str += os.linesep

        return str
