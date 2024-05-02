from Tokens import Token

class AnalizadorLexicoSintactico:
    def __init__(self):
        self.tokens = []
        self.errores_lexicos = []
        self.errores_sintacticos = []
        self.caracteres_validos = ['{', '}', '"', '“', '”', ',', ':', '=', ';', '-', '*', '/']
        self.palabras_reservadas = ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion',
                                    'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']
        self.analizador_sintactico = AnalizadorSintactico()

    def agregarError(self, tipo, linea, columna, caracter=None, token_esperado=None, descripcion=None):
        self.errores_lexicos.append({
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
                elif caracter not in self.caracteres_validos:
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
                    self.agregarError('Léxico', linea, columna, buffer, "Se esperaba un segundo '-'")
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
                    self.agregarError('Léxico', linea, columna, buffer, "Se esperaba un '*'")
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
                    if buffer in self.palabras_reservadas:
                        self.agregarToken(f'Reservada_{buffer}', buffer, linea, columna - len(buffer))
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
                if caracter in ['"', '“', '”', ':', '{', '}']:
                    estado = 19
                    buffer += caracter
                elif caracter == '\n':
                    linea += 1
                    columna = 1
                elif caracter.isspace():
                    tokens_dentro_comillas = buffer.split()
                    for token in tokens_dentro_comillas:
                        if token in self.palabras_reservadas:
                            self.agregarToken(f'Reservada_{token}', token, linea, columna - len(token))
                        else:
                            self.agregarToken('Identificador', token, linea, columna - len(token))
                    buffer = ''
                    estado = 17
                else:
                    estado = 18
                    buffer += caracter

            elif estado == 18:
                if caracter in ['"', '”']:
                    estado = 19
                    buffer += caracter
                else:
                    buffer += caracter

            elif estado == 19:
                self.agregarToken('Cadena', buffer, linea, columna)
                buffer = ''
                estado = 0
                continue

            i += 1

        self.analizador_sintactico.analizar_sintacticamente(self.tokens)

        return self.tokens, self.errores_lexicos, self.errores_sintacticos

    def traducir_comandos_nosql_a_mongodb(texto_nosql):
        comandos_mongodb = []
        errores = []

        lineas = texto_nosql.split('\n')

        for linea in lineas:
            linea = linea.strip()

            if linea.startswith('CrearBD'):
                partes = linea.split()
                if len(partes) >= 4 and partes[2] == '=':
                    nombre_bd = partes[3]
                    comando_mongodb = f'db = use("{nombre_bd}");'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif linea.startswith('EliminarBD'):
                partes = linea.split()
                if len(partes) >= 4 and partes[2] == '=':
                    nombre_bd = partes[3]
                    comando_mongodb = f'db.dropDatabase("{nombre_bd}");'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif linea.startswith('CrearColeccion'):
                partes = linea.split('"')
                if len(partes) >= 2:
                    nombre_coleccion = partes[1]
                    comando_mongodb = f'db.createCollection("{nombre_coleccion}");'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif linea.startswith('EliminarColeccion'):
                partes = linea.split('"')
                if len(partes) >= 2:
                    nombre_coleccion = partes[1]
                    comando_mongodb = f'db.{nombre_coleccion}.drop();'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif 'InsertarUnico' in linea:
                partes = linea.split('"')
                if len(partes) >= 2:
                    nombre_coleccion = partes[1]
                    json_data = linea[linea.find('{'):]
                    comando_mongodb = f'db.{nombre_coleccion}.insertOne({json_data});'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif 'ActualizarUnico' in linea:
                partes = linea.split('"')
                if len(partes) >= 6:
                    nombre_coleccion = partes[1]
                    filtro = partes[3]
                    actualizacion = partes[5]
                    comando_mongodb = f'db.{nombre_coleccion}.updateOne({filtro},{actualizacion});'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif 'EliminarUnico' in linea:
                partes = linea.split('"')
                if len(partes) >= 4:
                    nombre_coleccion = partes[1]
                    filtro = partes[3]
                    comando_mongodb = f'db.{nombre_coleccion}.deleteOne({filtro});'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif 'BuscarTodo' in linea:
                partes = linea.split('"')
                if len(partes) >= 2:
                    nombre_coleccion = partes[1]
                    comando_mongodb = f'db.{nombre_coleccion}.find();'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif 'BuscarUnico' in linea:
                partes = linea.split('"')
                if len(partes) >= 2:
                    nombre_coleccion = partes[1]
                    comando_mongodb = f'db.{nombre_coleccion}.findOne();'
                    comandos_mongodb.append(comando_mongodb)
                else:
                    errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})
            elif linea.startswith('//') or linea.startswith('#') or linea.startswith('---'):
                # Comentarios de una línea, se traducen a #
                comando_mongodb = f'# {linea[2:].strip()}'
                comandos_mongodb.append(comando_mongodb)
            elif linea.startswith('/*'):
                # Inicio de comentario multilínea
                comando_mongodb = '"""'
                comandos_mongodb.append(comando_mongodb)
                while linea and not linea.startswith('*/'):
                    try:
                        linea = next(iter(lineas), '')
                        linea = linea.strip()
                        if linea:
                            comando_mongodb = f'{linea}'
                            comandos_mongodb.append(comando_mongodb)
                    except StopIteration:
                        errores.append({"tipo": "Error sintáctico", "descripcion": "Comentario multilínea sin cerrar"})
                        break
                if linea.startswith('*/'):
                    comando_mongodb = '"""'
                    comandos_mongodb.append(comando_mongodb)
            elif not linea:
                # Línea vacía, no se traduce
                pass
            else:
                errores.append({"tipo": "Error sintáctico", "descripcion": f"Línea no reconocida: {linea}"})

        return comandos_mongodb, errores

class AnalizadorSintactico:
    def __init__(self):
        self.errores_sintacticos = []
        self.palabras_reservadas = ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion',
                                    'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']

    def agregarError(self, tipo, linea, columna, caracter=None, token_esperado=None, descripcion=None):
        self.errores_sintacticos.append({
            "tipo": tipo,
            "linea": linea,
            "columna": columna,
            "caracter": caracter,
            "token_esperado": token_esperado,
            "descripcion": descripcion
        })

    def analizar_sintacticamente(self, tokens):
        for token in tokens:
            if token.tipo.startswith('Reservada'):
                if token.contenido not in self.palabras_reservadas:
                    self.agregarError('Sintáctico', token.linea, token.columna,
                                      caracter=token.contenido,
                                      token_esperado="Palabra reservada válida",
                                      descripcion=f"Palabra reservada incorrecta: {token.contenido}")


