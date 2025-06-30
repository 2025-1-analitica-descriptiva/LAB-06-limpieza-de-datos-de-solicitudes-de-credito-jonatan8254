"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


import os
import pandas as pd

def normalizar_texto(serie):
    """
    Convierte la serie a string, la pone en minúsculas, elimina espacios
    extremos y reemplaza ciertos caracteres.
    """
    return (serie.astype(str)
                .str.strip()
                .str.lower()
                .str.replace("_", " ", regex=False)
                .str.replace("-", " ", regex=False)
                .str.replace(",", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.replace(".00", "", regex=False)
                .str.strip())

def convertir_fecha(fecha_series):
    """
    Intenta convertir la serie de fechas a datetime usando dos formatos,
    combinando ambos resultados.
    """
    fmt1 = pd.to_datetime(fecha_series, format="%d/%m/%Y", errors="coerce")
    fmt2 = pd.to_datetime(fecha_series, format="%Y/%m/%d", errors="coerce")
    return fmt1.combine_first(fmt2)

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio se escribe en "files/output/solicitudes_de_credito.csv"
    """
    archivo_entrada = "files/input/solicitudes_de_credito.csv"
    archivo_salida = "files/output/solicitudes_de_credito.csv"

    # Cargar el archivo usando el primer campo como índice y el separador ";"
    df = pd.read_csv(archivo_entrada, sep=";", index_col=0, encoding="UTF-8")
    
    # Eliminar registros con valores nulos (inicialmente)
    df.dropna(inplace=True)
    
    # Normalización de la columna 'sexo'
    df["sexo"] = df["sexo"].str.lower().str.strip()
    # Convertir a 'm' o 'f' según el primer caracter (ej. "masculino" -> "m", "femenino" -> "f")
    df["sexo"] = df["sexo"].apply(lambda x: "m" if x.startswith("m") else ("f" if x.startswith("f") else x))
    
    # Normalización de 'tipo_de_emprendimiento'
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower().str.strip()
    
    # Normalización y limpieza de 'barrio'
    df["barrio"] = df["barrio"].str.lower().str.replace("_", " ", regex=False).str.replace("-", " ", regex=False)
    
    # Normalización y limpieza de 'idea_negocio'
    df["idea_negocio"] = df["idea_negocio"].str.lower().str.replace("_", " ", regex=False).str.replace("-", " ", regex=False).str.strip()
    
    # Limpieza y conversión de 'monto_del_credito'
    df["monto_del_credito"] = (df["monto_del_credito"]
                               .str.strip()
                               .str.replace("$", "", regex=False)
                               .str.replace(",", "", regex=False)
                               .str.replace(".00", "", regex=False))
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce")
    
    # Normalización y limpieza de 'línea_credito'
    df["línea_credito"] = df["línea_credito"].str.lower().str.replace("_", " ", regex=False).str.replace("-", " ", regex=False).str.strip()
    
    # Conversión de 'fecha_de_beneficio'
    fecha1 = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce")
    fecha2 = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    df["fecha_de_beneficio"] = fecha1.combine_first(fecha2)
    
    # Conversión de 'comuna_ciudadano' a número entero
    df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"], errors="coerce", downcast="integer")
    
    # Conversión de 'estrato' a entero
    df["estrato"] = df["estrato"].astype(int)
    
    # Eliminar registros duplicados y eliminar nuevamente registros con datos faltantes
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    
    # Filtrar para conservar solo registros donde "sexo" sea "m" o "f"
    df = df[df["sexo"].isin(["m", "f"])]
    
    # Crear el directorio de salida si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
    
    # Guardar el DataFrame limpio en el archivo de salida usando ";" como separador
    df.to_csv(archivo_salida, sep=";", index=False)

if __name__ == '__main__':
    pregunta_01()