from Errores import Error
from Tokens import Token
from prettytable import PrettyTable

class AnalizadorSintactico:
    def __init__(self):
        self.tokens = []
        self.errores = []

    def agregarError(self, tipo, linea, columna, caracter=None, token_esperado=None, descripcion=None):
        self.errores.append({
            "tipo": tipo,
            "linea": linea,
            "columna": columna,
            "caracter": caracter,
            "token_esperado": token_esperado,
            "descripcion": descripcion
        })

    def agregarToken(self, tipo, token, linea, columna):
        self.tokens.append(Token(tipo, token, linea, columna))

    def obtener_token_actual(self):
        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]
        else:
            return None

    def avanzar(self):
        self.posicion += 1

    def error(self, mensaje):
        token_actual = self.obtener_token_actual()
        if token_actual:
            self.errores.append({
                "tipo": "Sintáctico",
                "mensaje": mensaje,
                "token": token_actual
            })

    def emparejar(self, tipo_esperado):
        token_actual = self.obtener_token_actual()
        if token_actual and token_actual.tipo == tipo_esperado:
            self.avanzar()
        else:
            self.error(f"Se esperaba un token de tipo '{tipo_esperado}' pero se encontró '{token_actual.tipo}'")

    def analizar(self, tokens):
        self.tokens = tokens
        self.posicion = 0
        while self.obtener_token_actual():
            self.instruccion()

    def instruccion(self):
        token_actual = self.obtener_token_actual()

        if token_actual.tipo == "CrearBD":
            self.emparejar("CrearBD")
            self.emparejar("Identificador")
            self.emparejar("Igual")
            self.emparejar("nueva")
            self.emparejar("CrearBD")
            self.emparejar("Punto_Comma")
        elif token_actual.tipo == "EliminarBD":
            self.emparejar("EliminarBD")
            self.emparejar("Identificador")
            self.emparejar("Igual")
            self.emparejar("nueva")
            self.emparejar("EliminarBD")
            self.emparejar("Punto_Comma")
        elif token_actual.tipo == "CrearColeccion":
            self.emparejar("CrearColeccion")
            self.emparejar("Identificador")
            self.emparejar("Igual")
            self.emparejar("nueva")
            self.emparejar("CrearColeccion")
            self.emparejar("Parentesis_A")
            self.emparejar("Cadena")
            self.emparejar("Parentesis_C")
            self.emparejar("Punto_Comma")
        else:
            self.error(f"Instrucción no válida: '{token_actual.tipo}'")
            self.avanzar()

    def ver_errores(self):
        if self.errores:
            table = PrettyTable(["Tipo de Error", "Línea", "Columna", "Caracter", "Token Esperado", "Descripción"])
            for error in self.errores:
                table.add_row([error["tipo"], error["linea"], error["columna"], error["caracter"], error.get("token_esperado", ""), error.get("descripcion", "")])
            print(table)
        else:
            print("No se encontraron errores.")
