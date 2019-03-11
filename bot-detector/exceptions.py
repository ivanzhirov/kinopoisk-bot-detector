class KinopoiskBotDetectorException(Exception):
    # Base application exception
    pass


class ParsingException(KinopoiskBotDetectorException):
    # Happens when site has changed their markup
    pass
