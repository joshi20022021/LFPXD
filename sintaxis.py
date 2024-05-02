def encontrar_errores_sintacticos(texto):
    errores = []

    # Analizar cada línea del texto
    lineas = texto.split('\n')
    for i, linea in enumerate(lineas, start=1):
        # Verificar paréntesis balanceados
        if linea.count("(") != linea.count(")"):
            errores.append(f"Error sintáctico en la línea {i}: Paréntesis no balanceados")

        # Verificar formato de cadenas JSON
        if "JSON" in linea:
            if "{" not in linea or "}" not in linea:
                errores.append(f"Error sintáctico en la línea {i}: Formato de cadena JSON incorrecto")

    return errores

# Ejemplo de uso:
texto = """
CrearDB cali = nueva CrearDB();
CrearColleccion colec = nueva CrearColeccion("Coleccion1");
CrearColleccion colec2 = nueva CrearColeccion("Coleccion2");
CrearColecction colec3 = nueva CreacColeccion("Coleccion3");
InsertarUnico uno = nueva InsertarUnico("Coleccion1",
{
	"id": 1,
	"nombre": "Calificacion 1",
	"anio": 2023,
	"curso": "Lenguajes Formales y de Programacion"
}
);@@

InsertarUnico dos = nueva InsertarUnico("Coleccion1",
{
	"id": 1,
	"nombre": "Calificacion 2",
	"anio": 2023,
	"curso": "Introduccion a la Programacion 2"
}
);

EliminarColeccion c1 = nueva EliminarColeccion("Coleccion2");

ActualizarUnico ac1 = nueva ActualizarUnico("Coleccion1",
{
	"id" : 1
},
{
	$set: {"curso": "Oficialmente estoy en Compi 1"}
}
);

EliminarUnico el1 = nueva EliminarUnico("Coleccion1",
{
	"id" : 2
}

);

BuscarTodo todo = nueva BuscarTodo("Coleccion1");
"""

errores_sintacticos = encontrar_errores_sintacticos(texto)
if errores_sintacticos:
    print("Se encontraron errores sintácticos:")
    for error in errores_sintacticos:
        print(error)
else:
    print("No se encontraron errores sintácticos.")
