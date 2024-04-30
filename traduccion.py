def analizar_linea(linea):
    tipo_funcion, funcion = linea.split(" ", 1)
    if tipo_funcion in ("CrearBD", "EliminarBD", "BuscarTodo", "BuscarUnico"):
        return tipo_funcion, funcion.strip()
    elif tipo_funcion == "CrearColeccion":
        if funcion.startswith("createCollection "):
            return tipo_funcion, funcion[16:].strip("(); '\"")
        else:
            return "Error", f"Sintaxis incorrecta en línea: {linea}"
    elif tipo_funcion == "EliminarColeccion":
        if funcion.startswith("dropCollection "):
            return tipo_funcion, funcion[14:].strip("(); '\"")
        else:
            return "Error", f"Sintaxis incorrecta en línea: {linea}"
    elif tipo_funcion in ("InsertarUnico", "ActualizarUnico", "EliminarUnico"):
        if funcion.startswith("insertOne ") or funcion.startswith("updateOne ") or funcion.startswith("deleteOne "):
            nombre_coleccion = funcion.split("(")[0].strip()
            contenido = funcion.split("(")[1].strip("(); '\"")
            return tipo_funcion, nombre_coleccion, contenido
        else:
            return "Error", f"Sintaxis incorrecta en línea: {linea}"
    else:
        return "Error", f"Tipo de función desconocido en línea: {linea}"

def traducir_comandos(texto):
    traducciones = {
        "CrearBD": "use '{nombre}';",
        "EliminarBD": "db.dropDatabase();",
        "CrearColeccion": "db.createCollection('{nombre}');",
        "EliminarColeccion": "db.dropCollection('{nombre}');",
        "InsertarUnico": "db.{coleccion}.insertOne({contenido});",
        "ActualizarUnico": "db.{coleccion}.updateOne({filtro}, {accion});",
        "EliminarUnico": "db.{coleccion}.deleteOne({filtro});",
        "BuscarTodo": "db.{nombre}.find();",
        "BuscarUnico": "db.{nombre}.findOne();"
    }

    comandos_mongodb = []
    errores_sintacticos = []

    lineas = texto.split('\n')
    for linea in lineas:
        tipo_funcion, *args = analizar_linea(linea)
        if tipo_funcion != "Error":
            if tipo_funcion in ("CrearColeccion", "EliminarColeccion"):
                comando_mongo = traducciones[tipo_funcion].format(nombre=args[0])
            elif tipo_funcion in ("InsertarUnico", "ActualizarUnico", "EliminarUnico"):
                comando_mongo = traducciones[tipo_funcion].format(coleccion=args[0], filtro=args[1], accion=args[2])
            else:
                comando_mongo = traducciones[tipo_funcion].format(nombre=args[0])
            comandos_mongodb.append(comando_mongo)
        else:
            errores_sintacticos.append(args[0])

    return '\n'.join(comandos_mongodb), errores_sintacticos
