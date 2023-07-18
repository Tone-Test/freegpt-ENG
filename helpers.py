from discord import Embed, Colour

class ErrorEmbed(Embed):
    def __init__(self, text):
        super().__init__(color=Colour.red(), title='Ошибка', description=text)