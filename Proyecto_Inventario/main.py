import os
import sqlite3 as sql
import textwrap


DB_NAME = "inventario.db"

def connect_db(db_name: str) -> None:
    """
    
    """
    
    with sql.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL,
                proveedor TEXT NOT NULL,
                descripcion TEXT NOT NULL
            )
        """)
        db.commit()

def clear() -> None:
    os.system("cls")

def contar_registros(db_name: str) -> int:
    with sql.connect(db_name) as db:
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM inventario")
        return cur.fetchone()[0]

def obtener_datos(db_name:str, limite: int | None = None, offset: int = 0) -> list[tuple]:
    with sql.connect(db_name) as db:
        cur = db.cursor()

        query = """
            SELECT id, producto, categoria, marca, modelo, precio, stock, proveedor, descripcion
            FROM inventario
            ORDER BY id ASC
        """

        params = []
        if limite is not None:
            query += " LIMIT ? OFFSET ?"
            params = [limite, offset]

        cur.execute(query, params)
        return cur.fetchall()

def dividir_texto(texto: str, ancho: int) -> list[str]:
    if ancho <= 0:
        return [""]
    return textwrap.wrap(str(texto), width=ancho) or [""]

def filas_x_celda(ancho_columna: list[int], texto_columna: list[str]) -> tuple[list[list[str]], int]:
        celdas_divididas = []
        lineas_x_celda = 1
        for ancho,texto in zip(ancho_columna,texto_columna):
            lineas = dividir_texto(texto,ancho)
            celdas_divididas.append(lineas)
            if len(lineas) > lineas_x_celda:
                lineas_x_celda = len(lineas)
        return celdas_divididas, lineas_x_celda

def print_fila(lineas_x_celdas: int, celdas_divididas: list[list[str]], anchos_texto: list[int]) -> None:
    for linea_idx in range(lineas_x_celdas):
        linea = "|"
        for i, lineas_celda in enumerate(celdas_divididas):
            if linea_idx < len(lineas_celda):
                contenido = lineas_celda[linea_idx]
            else:
                contenido = ""
            linea += f" {contenido:<{anchos_texto[i]}} |"
        print(linea)

def imprimir_tabla(columnas: list[str], filas: list[list[str]], porcentajes: list[float], ancho_total: int = 200) -> None:
    if not filas:
        print("\nNo hay registros para mostrar.\n")
        return

    num_cols = len(columnas)
    # Quitamos del total los bordes correspondientes a los divisores de cada columna
    ancho_disponible = ancho_total - (num_cols + 1) 
    # Calculamos el ancho por cada porcentaje
    anchos_col = [int(ancho_disponible * p / 100) for p in porcentajes]
    # Anchos reales
    suma_anchos = sum(anchos_col) + num_cols + 1
    diferencia = ancho_total - suma_anchos
    if diferencia != 0:
        anchos_col[-1] += diferencia
    anchos_col[-1] += 2 # Por los margenes
    # Ancho de texto disponible por columna sin los bordes de columna
    anchos_texto = [max(1, a - 2) for a in anchos_col]
    # Imprimir borde superior
    #print("+" + "+".join("=" * a for a in anchos_col) + "+") # Feo
    
    # Titulos de columnas
    titulos_divididos, max_lineas_titulo = filas_x_celda(anchos_texto,columnas)
    print_fila(max_lineas_titulo,titulos_divididos,anchos_texto)
    print("+" + "+".join("=" * a for a in anchos_col) + "+")

    # Filas
    for fila in filas:
        celdas_divididas,max_lineas = filas_x_celda(anchos_texto,fila)
        print_fila(max_lineas,celdas_divididas,anchos_texto)
        print("+" + "+".join("." * a for a in anchos_col) + "+")



def menu_principal(ancho: int = 98)-> None:
    print("\n" + "+" + "-" * ancho + "+")
    print("|" + " MENÚ ".center(ancho, " ") + "|")
    print("+" + "-" * ancho + "+")
    print("  1) Ver todos los registros")
    print("  2) Crear nuevo registro")
    print("  3) Consultar")
    print("  4) Actualizar registro")
    print("  5) Eliminar registro")
    print("  6) Salir")
    print("+" + "-" * ancho + "+")

def ventana(titulo: str, ancho: int = 98)-> None:
    print("+" + "=" * ancho + "+")
    print("|" + titulo.center(ancho) + "|")
    print("+" + "=" * ancho + "+")
    

def insertar_producto(db_name: str, producto: str, categoria: str, marca: str, modelo: str, precio: float, stock: int, proveedor: str, descripcion: str)-> int:
    with sql.connect(db_name) as db:
        cur = db.cursor()
        cur.execute("""
            INSERT INTO inventario (producto, categoria, marca, modelo, precio, stock, proveedor, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (producto, categoria, marca, modelo, precio, stock, proveedor, descripcion))
        db.commit()
        return cur.lastrowid 

def pedir_float(msg: str, minimo: float | None = None)-> float:
    while True:
        try:
            valor = float(input(msg).strip())
            if minimo is not None and valor < minimo:
                print(f" Debe ser >= {minimo}")
                continue
            return valor
        except ValueError:
            print(" Ingresa un número valido.")

def pedir_int(msg: str, minimo: int | None = None)-> int:
    while True:
        try:
            valor = int(input(msg).strip())
            if minimo is not None and valor < minimo:
                print(f" Debe ser >= {minimo}")
                continue
            return valor
        except ValueError:
            print(" Ingresa un entero válido.")

def crear_registro(db_name: str, ancho_ventana: int)-> None:
    clear()
    ventana("CREAR NUEVO PRODUCTO", ancho_ventana)

    producto = input("Producto: ").strip()
    categoria = input("Categoría: ").strip()
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    precio = pedir_float("Precio: ", minimo=0)
    stock = pedir_int("Stock: ", minimo=0)
    proveedor = input("Proveedor: ").strip()
    descripcion = input("Descripción: ").strip()

    if not all([producto, categoria, marca, modelo, proveedor, descripcion]):
        input("\n Campos vaciós no son validos. Enter para regresar...")
        return

    nuevo_id = insertar_producto(
        db_name, producto, categoria, marca, modelo, precio, stock, proveedor, descripcion
    )

    input(f"\n Registro creado con ID {nuevo_id}. Enter para continuar...")



def consultar_x_id(db_name: str, id: int) -> list[tuple]:
    with sql.connect(db_name) as db:
        cur = db.cursor()
        cur.execute("""
            SELECT id, producto, categoria, marca, modelo, precio, stock, proveedor, descripcion
            FROM inventario
            WHERE id = ?
        """, (id,))
        return cur.fetchall()

def actualizar_campo(db_name: str, id_registro: int, campo: str, valor: str | float | int) -> int:
    campos_validos = {
        "producto", "categoria", "marca", "modelo",
        "precio", "stock", "proveedor", "descripcion"
    }
    if campo not in campos_validos:
        raise ValueError("Campo no permitido")
    
    with sql.connect(db_name) as db:
        cur = db.cursor()
        cur.execute(f"UPDATE inventario SET {campo} = ? WHERE id = ?", (valor, id_registro))
        db.commit()
        return cur.rowcount 


def actualizar_registro(db_name: str, columnas: list, porcentajes: list, ancho_ventana: int)-> None:
    clear()
    ventana("ACTUALIZAR REGISTRO", ancho_ventana)

    id_registro = pedir_int("Ingresa el ID del producto a modificar: ",0)

    fila = consultar_x_id(db_name, id_registro)
    if not fila:
        input("No existe un registro con ese ID. Enter para volver...")
        return

    clear()
    ventana("REGISTRO ENCONTRADO", ancho_ventana)
    imprimir_tabla(columnas, fila, porcentajes, ancho_ventana)

    # Menú de edición
    while True:
        print("\n¿Qué campo deseas modificar?")
        print("  1) Producto")
        print("  2) Categoría")
        print("  3) Marca")
        print("  4) Modelo")
        print("  5) Precio")
        print("  6) Stock")
        print("  7) Proveedor")
        print("  8) Descripción")
        print("  9) Terminar y mostrar registro modificado")
        op = input("\nOpción: ").strip()

        map = {
            "1": "producto",
            "2": "categoria",
            "3": "marca",
            "4": "modelo",
            "5": "precio",
            "6": "stock",
            "7": "proveedor",
            "8": "descripcion"
        }

        if op == "9":
            break

        if op not in map:
            print("Opción inválida.")
            continue

        campo = map[op]

        # Pedir nuevo valor según el tipo
        if campo == "precio":
            nuevo_valor = pedir_float("Nuevo precio: ", minimo=0)
        elif campo == "stock":
            nuevo_valor = pedir_int("Nuevo stock: ", minimo=0)
        else:
            nuevo_valor = input("Nuevo valor: ").strip()
            if not nuevo_valor:
                print("No puede quedar vacío.")
                continue

        actualizar_campo(db_name, id_registro, campo, nuevo_valor)

        fila = consultar_x_id(db_name, id_registro)
        clear()
        ventana("REGISTRO ACTUALIZADO", ancho_ventana)
        imprimir_tabla(columnas, fila, porcentajes, ancho_ventana)



def consultar_x_columna(db_name: str, campo: str, texto: str) -> list[tuple]:
    campos_validos = {"producto", "categoria", "marca", "modelo"}
    if campo not in campos_validos:
        raise ValueError("Campo no permitido")

    patron = f"%{texto.strip()}%"
    with sql.connect(db_name) as db:
        cur = db.cursor()
        cur.execute(f"""
            SELECT id, producto, categoria, marca, modelo, precio, stock, proveedor, descripcion
            FROM inventario
            WHERE LOWER({campo}) LIKE LOWER(?)
            ORDER BY id ASC
        """, (patron,))
        return cur.fetchall()



def consultar_registros(db_name: str, columnas: list, ancho_celda: list, ancho_ventana: int)-> None:
    while True:
        clear()
        ventana("CONSULTAR INVENTARIO", ancho_ventana)

        print("Elige criterio de búsqueda:")
        print("  1) Por ID")
        print("  2) Por Producto")
        print("  3) Por Categoría")
        print("  4) Por Marca")
        print("  5) Por Modelo")
        print("  6) Volver al menú")

        op = input("\nOpción: ").strip()

        if op == "6":
            return

        if op == "1":
            id_buscar = pedir_int("Ingresa el ID: ", 0)
            filas = consultar_x_id(db_name, id_buscar)

        elif op in {"2", "3", "4", "5"}:
            texto = input("Texto a buscar (puede ser parcial): ").strip()
            if not texto:
                input(" No dejes el texto vacío. Enter para continuar...")
                continue

            mapa = {"2": "producto", "3": "categoria", "4": "marca", "5": "modelo"}
            campo = mapa[op]
            filas = consultar_x_columna(db_name, campo, texto)

        else:
            input(" Opción inválida. Enter para continuar...")
            continue

        clear()
        ventana("RESULTADOS DE BÚSQUEDA", ancho_ventana)

        if filas:
            imprimir_tabla(columnas, filas, ancho_celda, ancho_ventana)
            input("\nEnter para volver a consultar...")
        else:
            input("\nNo se encontraron resultados. Enter para volver a consultar...")

def eliminar(db_name: str, id_registro: int) -> int:
    with sql.connect(db_name) as db:
        cur = db.cursor()
        cur.execute("DELETE FROM inventario WHERE id = ?", (id_registro,))
        db.commit()
        return cur.rowcount  # 1 

def eliminar_registro(db_name: str, columnas: list, porcentajes: list, ancho_ventana: int)-> None:
    clear()
    ventana("ELIMINAR REGISTRO", ancho_ventana)

    id_registro = pedir_int("Ingresa el ID del producto a eliminar: ",0) 
    # Buscar y mostrar
    fila = consultar_x_id(db_name, id_registro)
    if not fila:
        input("No existe un registro con ese ID. Enter para volver...")
        return

    clear()
    ventana("CONFIRMAR ELIMINACIÓN", ancho_ventana)
    imprimir_tabla(columnas, fila, porcentajes, ancho_ventana)

    conf = input("\n¿Seguro que deseas eliminar este registro? (s/n): ").strip().lower()
    if conf != "s":
        input("Cancelado. Enter para volver al menú...")
        return

    # Eliminar
    borrados = eliminar(db_name, id_registro)
    if borrados == 1:
        input("Registro eliminado correctamente. Enter para volver al menú...")
    else:
        input("No se pudo eliminar. Enter para volver al menú...")


if __name__ == "__main__":
    connect_db(DB_NAME)
    COLUMNAS = ["ID", "Producto", "Categoría", "Marca", "Modelo", "Precio", "Stock", "Proveedor", "Descripción"]
    TITULO = "INVENTARIO - ELECTRÓNICA DE MUY MUY LEJANO......."
    PORCENTAJES = [3, 15, 8, 8, 8, 6, 5, 10, 37] 
    ANCHO_VENTANA = 200

    while True:

        clear()
        ventana(TITULO,ANCHO_VENTANA)
        filas = obtener_datos(DB_NAME, limite=10, offset=0)
        imprimir_tabla(COLUMNAS, filas, PORCENTAJES, ANCHO_VENTANA)
        menu_principal(ANCHO_VENTANA)

        op = input("Elije una opción:  ").strip()
        
        if op == "1":
            limite = 20
            total = contar_registros(DB_NAME)
            offset = 0

            while True:
                clear()
                ventana(TITULO, ANCHO_VENTANA)
                filas = obtener_datos(DB_NAME, limite=limite, offset=offset)
                if not filas:
                    print("\nNo hay más registros.\n")
                    input("Enter para volver al menú...")
                    break
                imprimir_tabla(COLUMNAS, filas, PORCENTAJES, ANCHO_VENTANA)

                # flag
                inicio = offset + 1
                fin = min(offset + limite, total)
                print(f"\nMostrando registros {inicio}-{fin} de {total}")

                tecla = input("Enter = siguiente | q = salir: ").strip().lower()

                if tecla == "q":
                    break

                offset += limite
                if offset >= total:
                    input("\nFin de registros. Enter para volver al menú...")
                    break

        elif op == "2":
            crear_registro(DB_NAME, ANCHO_VENTANA)

        elif op == "3":
            consultar_registros(DB_NAME, COLUMNAS, PORCENTAJES, ANCHO_VENTANA)

        elif op == "4":
            actualizar_registro(DB_NAME, COLUMNAS, PORCENTAJES, ANCHO_VENTANA)

        elif op == "5":
            eliminar_registro(DB_NAME, COLUMNAS, PORCENTAJES, ANCHO_VENTANA)

        elif op == "6":
            print("Saliendo...")
            break

        else:
            input("Opción inválida. Enter para continuar...")
    
