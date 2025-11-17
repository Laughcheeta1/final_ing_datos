import pandas as pd
import os


columns = [
    "NIT_EXPORTADOR",
    "RAZON_SOCIAL_EXPORTADOR",
    "DIREC_EXPORTADOR",
    "REGION_DE_ORIGEN",
    "COD_ADUANA_DESPACHO",
    "ADUANA_SALIDA",
    "COD_LUG_SALIDA_ALF",
    "COD_UNIDAD_FISICA_ALF",
    "CANTIDAD_UNIDADES_FISICAS",
    "PESO_NETO_KGS",
    "PESO_BRUTO_KGS",
    "COD_MONEDA_TRANSACCION",
    "VALOR_FOB_USD",
    "FECHA_DECLARACION_EXPORTACION",
    "PAIS_DESTINO_FINAL",
    "CIUDAD_DESTINATARIO",
    "COD_MODALIDAD_EXPORTACION",
    "MODALIDAD_EXPORTACION",
    "MODO_TRANSPORTE",
    "NACIONALIDAD_BANDERA"
]

for file_name in os.listdir("./raw"):
    file_name = f"./raw/{file_name}"
    df = pd.read_excel(file_name)
    df = df[columns]
    output_file = f"./cleaned/{file_name}"
    df.to_parquet(output_file, index=False)
