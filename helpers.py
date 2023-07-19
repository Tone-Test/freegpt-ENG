from discord import Embed, Colour

class ErrorEmbed(Embed):
    def __init__(self, text):
        super().__init__(color=Colour.red(), title='Ошибка', description=text)

class InfoEmbed(Embed):
    def __init__(self, title, text):
        super().__init__(color=Colour.blurple(), title=title, description=text)

class MessageEmbed(Embed):
    def __init__(self, title, text):
        super().__init__(color=Colour.green(), title=title, description=text)