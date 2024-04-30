from Errores import Error
from Tokens import Token

class AnalizadorLexico:
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

    def analizar(self, cadena):
        estado = 0
        buffer = ''
        linea = 1
        columna = 1
        i = 0

        while i < len(cadena):
            caracter = cadena[i]

            if estado == 0:
                if caracter == '-':
                    estado = 1
                    buffer += caracter
                elif caracter == '/':
                    estado = 6
                    buffer += caracter
                elif caracter.isalpha():
                    estado = 11
                    buffer += caracter
                elif caracter == '=':
                    estado = 12
                    buffer += caracter
                elif caracter == '(':
                    estado = 13
                    buffer += caracter
                elif caracter == ')':
                    estado = 14
                    buffer += caracter
                elif caracter == ';':
                    estado = 15
                    buffer += caracter
                elif caracter == ',':
                    estado = 16
                    buffer += caracter
                elif caracter == '"':
                    estado = 17
                    buffer += caracter
                elif caracter in [' ']:
                    pass
                elif caracter == '\n':
                    linea += 1
                    columna = 1
                elif caracter == '#':
                    pass
                else:
                    self.agregarError('Léxico', linea, columna, caracter, descripcion=f"Carácter no reconocido: {caracter}")
                    estado = 0
                    buffer = ''

            elif estado == 1:
                if caracter == '-':
                    estado = 2
                    buffer += caracter
                else:
                    self.agregarError('Léxico', linea, columna, buffer, "Se esperaba un '-'")
                    estado = 0
                    buffer = ''

            elif estado == 2:
                if caracter == '-':
                    estado = 3
                    buffer += caracter
                else:
                    self.agregarError(buffer, linea, columna)
                    estado = 0
                    buffer = ''

            elif estado == 3:
                if caracter != '\n':
                    estado = 4
                    buffer += caracter
                else:
                    estado = 5
                    linea += 1
                    columna = 1

            elif estado == 4:
                if caracter != '\n':
                    buffer += caracter
                else:
                    estado = 5
                    linea += 1
                    columna = 1

            elif estado == 5:
                self.agregarToken('Comentario', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 6:
                if caracter == '*':
                    estado = 7
                    buffer += caracter
                else:
                    self.agregarError('Caracter no reconocido', caracter, linea, columna)  # Aquí se debe pasar el carácter específico
                    estado = 0
                    buffer = ''

            elif estado == 7:
                if caracter != '*':
                    estado = 8
                    buffer += caracter
                else:
                    estado = 9
                    buffer += caracter

            elif estado == 8:
                if caracter != '*':
                    buffer += caracter
                else:
                    estado = 9
                    buffer += caracter

            elif estado == 9:
                if caracter != '/':
                    estado = 8
                    buffer += caracter
                else:
                    estado = 10
                    buffer += caracter

            elif estado == 10:
                self.agregarToken('Comentario', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 11:
                if caracter.isalpha():  
                    buffer += caracter
                    columna += 1  # Incrementa la columna para cada carácter alfanumérico
                else:
                    if buffer in ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion', 'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']:
                        self.agregarToken(f'Resevada_{buffer}', buffer, linea, columna - len(buffer))
                        buffer = ''
                        estado = 0
                    else:
                        self.agregarToken('Identificador', buffer, linea, columna - len(buffer))
                        buffer = ''
                        estado = 0
                    continue

            elif estado == 12:
                self.agregarToken('Igual', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 13:
                self.agregarToken('Parentesis_A', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 14:
                self.agregarToken('Parentesis_C', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 15:
                self.agregarToken('Punto_Comma', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 16:
                self.agregarToken('Coma', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 17:
                if caracter != '"':
                    if caracter == '\n':
                        linea += 1
                        columna = 1
                    elif caracter == '{':
                        estado = 20
                        buffer += caracter
                    else:
                        estado = 18
                        buffer += caracter
                else:
                    estado = 19
                    buffer += caracter

            elif estado == 18:
                if caracter != '"':
                    buffer += caracter
                else:
                    estado = 19
                    buffer += caracter

            elif estado == 19:
                self.agregarToken('Cadena', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            elif estado == 20:
                if caracter != '}':
                    estado = 21
                    if caracter == '\n':
                        linea += 1
                        columna = 1
                    else:
                        buffer += caracter
                else:
                    estado = 22
                    buffer += caracter

            elif estado == 21:
                if caracter != ')':
                    estado = 21
                    if caracter == '\n':
                        linea += 1
                        columna = 1
                    else:
                        buffer += caracter
                else:
                    estado = 22
                    buffer += caracter

            elif estado == 22:
                try:
                    buffer = buffer[:-1]
                except:
                    pass
                self.agregarToken('Data', buffer, linea, columna)
                buffer = ''
                estado = 0
                i -= 1

            i += 1

        return self.tokens, self.errores