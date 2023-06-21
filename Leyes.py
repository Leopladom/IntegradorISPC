import sqlite3
import pandas as pd


# Clase Leyes para insertar y ver leyes
class Leyes:
    def __init__(self):
        self.tipoNorma = None
        self.numNorma = None
        self.fecha = None
        self.desc = None
        self.cat = None
        self.jur = None
        self.org = None
        self.keyW = None

    def ingresar_datos(self):
        self.tipoNorma = input("Tipo de Normativa: ")
        self.numNorma = input("Numero de Normativa: ")
        self.fecha = input("Fecha: ")
        self.desc = input("Descripcion: ")
        self.cat = input("Categoria: ")
        self.jur = input("Jurisdiccion: ")
        self.org = input("Organo Legislativo: ")
        self.keyW = input("Palabra Clave: ")

    def insertar_ley_tabla1(self, P):
        cursor = P.cursor()
        cursor.execute("INSERT INTO tabla1 (TipoDeNormativa, NumeroDeNormativa, Fecha, Descripcion) VALUES (?,?,?,?)",
                       (self.tipoNorma, self.numNorma, self.fecha, self.desc))

    def insertar_ley_tabla2(self, P):
        cursor = P.cursor()
        cursor.execute("INSERT INTO tabla2 (Nro, Categoria, Jurisdiccion) VALUES (?,?,?)",
                       (self.numNorma, self.cat, self.jur))

    def insertar_ley_tabla3(self, P):
        cursor = P.cursor()
        cursor.execute("INSERT INTO tabla3 (Nro, OrganoLegislativo, PalabraClave) VALUES (?,?,?)",
                       (self.numNorma, self.org, self.keyW))

    def ver_laws_unificadas(self, P):
        cursor = P.cursor()
        cursor.execute("SELECT t1.Nro, t1.TipoDeNormativa, t1.NumeroDeNormativa, t1.Fecha, t1.Descripcion, t2.Categoria, t2.Jurisdiccion, t3.OrganoLegislativo, t3.PalabraClave "
                       "FROM tabla1 AS t1 "
                       "JOIN tabla2 AS t2 ON t1.NumeroDeNormativa = t2.Nro "
                       "JOIN tabla3 AS t3 ON t1.NumeroDeNormativa = t3.Nro")
        results = cursor.fetchall()
        results_df = pd.DataFrame(results, columns=["Nro", "TipoDeNormativa", "NumeroDeNormativa", "Fecha",
                                                    "Descripcion", "Categoria", "Jurisdiccion",
                                                    "OrganoLegislativo", "PalabraClave"])
        print(results_df)


# Clase Mods para actualizar y eliminar registros
class Mods:
    @staticmethod
    def actualizar_por_nro(P, nro):
        cursor = P.cursor()
        cursor.execute("SELECT * FROM tabla1 WHERE Nro=?", (nro,))
        registro_tabla1 = cursor.fetchone()

        if registro_tabla1 is None:
            print("No se encontró ningún registro con el número especificado.")
            return

        tipoNorma = input("Tipo de Normativa: ")
        numNorma = input("Numero de Normativa: ")
        fecha = input("Fecha: ")
        desc = input("Descripcion: ")

        cursor.execute("UPDATE tabla1 SET TipoDeNormativa=?, NumeroDeNormativa=?, Fecha=?, Descripcion=? WHERE Nro=?",
                       (tipoNorma, numNorma, fecha, desc, nro))

        cursor.execute("SELECT * FROM tabla2 WHERE Nro=?", (nro,))
        registro_tabla2 = cursor.fetchone()

        if registro_tabla2 is not None:
            cat = input("Categoria: ")
            jur = input("Jurisdiccion: ")

            cursor.execute("UPDATE tabla2 SET Categoria=?, Jurisdiccion=? WHERE Nro=?",
                           (cat, jur, nro))

        cursor.execute("SELECT * FROM tabla3 WHERE Nro=?", (nro,))
        registro_tabla3 = cursor.fetchone()

        if registro_tabla3 is not None:
            org = input("Organo Legislativo: ")
            keyW = input("Palabra Clave: ")

            cursor.execute("UPDATE tabla3 SET OrganoLegislativo=?, PalabraClave=? WHERE Nro=?",
                           (org, keyW, nro))

        P.commit()
        print("Registro actualizado con éxito.")

    @staticmethod
    def eliminar_por_keyw(P, keyw):
        cursor = P.cursor()

        cursor.execute("DELETE FROM tabla3 WHERE PalabraClave=?", (keyw,))
        cursor.execute("DELETE FROM tabla2 WHERE Nro IN (SELECT Nro FROM tabla3 WHERE PalabraClave=?)", (keyw,))
        cursor.execute("DELETE FROM tabla1 WHERE Nro IN (SELECT Nro FROM tabla3 WHERE PalabraClave=?)", (keyw,))

        P.commit()
        print("Registro eliminado con éxito.")


# Función para mostrar el menú
def menu():
    print("------------------Menu------------------")
    print("Seleccione 1 para insertar Leyes")
    print("Seleccione 2 para ver las Leyes Existentes")
    print("Seleccione 3 para salir del programa")
    print("Seleccione 4 para actualizar un registro")
    print("Seleccione 5 para eliminar un registro")


# Función para preguntar si se agregan más leyes
def preguntarOtra(objeto_leyes):
    otro = input("¿Agregar otra ley? (si/no): ")
    if otro == "si":
        objeto_leyes.ingresar_datos()
        objeto_leyes.insertar_ley_tabla1(P)
        objeto_leyes.insertar_ley_tabla2(P)
        objeto_leyes.insertar_ley_tabla3(P)
        preguntarOtra(objeto_leyes)
    elif otro == "no":
        print("Todas las leyes han sido agregadas correctamente.")


# Crear la base de datos y las tablas

with sqlite3.connect("IntegradorISPC\Proyect") as P:
    cursor = P.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tabla1 (Nro INTEGER PRIMARY KEY AUTOINCREMENT, TipoDeNormativa VARCHAR(50), NumeroDeNormativa VARCHAR(50), Fecha VARCHAR(20), Descripcion VARCHAR(550))")
    cursor.execute("CREATE TABLE IF NOT EXISTS tabla2 (Nro INTEGER PRIMARY KEY, Categoria VARCHAR(50), Jurisdiccion VARCHAR(50))")
    cursor.execute("CREATE TABLE IF NOT EXISTS tabla3 (Nro INTEGER PRIMARY KEY, OrganoLegislativo VARCHAR(50), PalabraClave VARCHAR(50))")

    # Crear objeto Leyes
    objeto_leyes = Leyes()

    # Ejecutar el menú
    while True:
        menu()
        opcion = input("Ingrese su opción: ")

        if opcion == "1":
            objeto_leyes.ingresar_datos()
            objeto_leyes.insertar_ley_tabla1(P)
            objeto_leyes.insertar_ley_tabla2(P)
            objeto_leyes.insertar_ley_tabla3(P)
            preguntarOtra(objeto_leyes)

        elif opcion == "2":
            objeto_leyes.ver_laws_unificadas(P)

        elif opcion == "3":
            print("Adios...")
            break

        elif opcion == "4":
            nro = input("Ingrese el número (Nro) del registro a actualizar: ")
            objeto_mods = Mods()
            objeto_mods.actualizar_por_nro(P, nro)

        elif opcion == "5":
            keyw = input("Ingrese la palabra clave (keyW) del registro a eliminar: ")
            objeto_mods = Mods()
            objeto_mods.eliminar_por_keyw(P, keyw)

        else:
            print("Opción incorrecta. Intente nuevamente.")
