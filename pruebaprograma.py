class Token:
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"Token({self.tipo}, '{self.lexema}', {self.linea}, {self.columna})"
