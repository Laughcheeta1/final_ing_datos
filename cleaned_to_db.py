import pandas as pd
import sqlite3
import os

DB_FILE = "exportaciones.db"

LUGARES_MAP = {
    "CUC": "Cúcuta",
    "BAQ": "Barranquilla",
    "CTG": "Cartagena",
    "SMR": "Santa Marta",
    "BUN": "Buenaventura",
    "BOG": "Bogotá",
    "MDE": "Medellín",
    "TRB": "Urabá",
    "RCH": "Riohacha",
    "CLO": "Cali",
    "LET": "Leticia",
    "MAI": "Maicao",
    "PEI": "Pereira",
    "IPI": "Ipiales",
    "YOP": "Yopal",
    "CVE": "Puerto Asís",
    "MAM": "Tumaco",
    "PUU": "Bucaramanga",
    "TCO": "Armenia",
    "BGA": "Arauca"
}

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

def add_to_db(file_name):
    df = pd.read_parquet(file_name)

    df["LUGAR_SALIDA_CIUDAD"] = df["COD_LUG_SALIDA_ALF"].map(LUGARES_MAP).fillna(df["COD_LUG_SALIDA_ALF"])


    def get_or_create(table, record):
        fields = list(record.keys())
        values = list(record.values())
        where = " AND ".join(f"{f}=?" for f in fields)
        cur.execute(f"SELECT id FROM {table} WHERE {where}", values)
        row = cur.fetchone()
        if row:
            return row[0]
        placeholders = ",".join("?" for _ in values)
        cur.execute(f"INSERT INTO {table} ({','.join(fields)}) VALUES ({placeholders})", values)
        return cur.lastrowid

    for _, r in df.iterrows():
        exportador_id = get_or_create(
            "Dim_Empresa",
            {
                "nit": r["NIT_EXPORTADOR"],
                "razon_social": r["RAZON_SOCIAL_EXPORTADOR"],
                "direccion": r["DIREC_EXPORTADOR"]
            }
        )

        origen_id = get_or_create(
            "Dim_Origen",
            {"region": r["REGION_DE_ORIGEN"]}
        )

        aduana_id = get_or_create(
            "Dim_Aduana",
            {
                "codigo_aduana": r["COD_ADUANA_DESPACHO"],
                "nombre_aduana": r["ADUANA_SALIDA"],
                "region": r["LUGAR_SALIDA_CIUDAD"]
            }
        )

        producto_id = get_or_create(
            "Dim_Producto",
            {
                "unidad": r["COD_UNIDAD_FISICA_ALF"],
                "cantidad_unidades": r["CANTIDAD_UNIDADES_FISICAS"],
                "peso_total_producto": r["PESO_NETO_KGS"],
                "peso_empaque": int(r["PESO_BRUTO_KGS"]) - int(r["PESO_NETO_KGS"])
            }
        )

        transaccion_id = get_or_create(
            "Dim_Transaccion",
            {
                "moneda": r["COD_MONEDA_TRANSACCION"],
                "fob_usd": r["VALOR_FOB_USD"]
            }
        )

        fecha = str(r["FECHA_DECLARACION_EXPORTACION"])
        year = int(fecha[0:4])
        month = int(fecha[4:6])
        fecha_id = get_or_create(
            "Dim_Fecha",
            {
                "año": year,
                "mes": month,
                "trimestre": (month - 1) // 3 + 1,
                "semestre": 1 if month <= 6 else 2
            }
        )

        destino_id = get_or_create(
            "Dim_Destino",
            {
                "nombre_pais": r["PAIS_DESTINO_FINAL"],
                "nombre_ciudad": r["CIUDAD_DESTINATARIO"]
            }
        )

        modalidad_id = get_or_create(
            "Dim_Modalidad",
            {
                "id_modalidad": r["COD_MODALIDAD_EXPORTACION"],
                "descripcion": r["MODALIDAD_EXPORTACION"]
            }
        )

        transporte_id = get_or_create(
            "Dim_Transporte",
            {
                "tipo": r["MODO_TRANSPORTE"],
                "pais_bandera": r["NACIONALIDAD_BANDERA"]
            }
        )

        cur.execute(
            """
            INSERT INTO Hecho_Exportacion
            (fecha, empresa, aduana, destino, producto, origen, modalidad, transporte, transaccion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                fecha_id,
                exportador_id,
                aduana_id,
                destino_id,
                producto_id,
                origen_id,
                modalidad_id,
                transporte_id,
                transaccion_id
            ]
        )

        print(f"Inserted row {_ + 1} of {len(df)}")

for file_name in os.listdir("./cleaned"):
    add_to_db(file_name)

conn.commit()
conn.close()
