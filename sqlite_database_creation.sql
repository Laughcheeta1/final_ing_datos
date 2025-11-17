PRAGMA foreign_keys = ON;

-- =========================
-- Dimension tables
-- =========================

CREATE TABLE Dim_Transporte (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo          TEXT,
    pais_bandera  TEXT
);

CREATE TABLE Dim_Modalidad (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    id_modalidad TEXT,
    descripcion  TEXT
);

CREATE TABLE Dim_Destino (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_pais            TEXT,
    nombre_ciudad          TEXT
);

CREATE TABLE Dim_Fecha (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    año       INTEGER,
    mes       INTEGER,
    dia       INTEGER,
    trimestre INTEGER,
    semestre  INTEGER
);

CREATE TABLE Dim_Transaccion (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    moneda  TEXT,
    fob_usd REAL
);

CREATE TABLE Dim_Producto (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    unidad             TEXT,
    cantidad_unidades  INTEGER,
    peso_total_producto REAL,
    peso_empaque        REAL
);

CREATE TABLE Dim_Aduana (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_aduana TEXT,
    nombre_aduana TEXT,
    region        TEXT
);

CREATE TABLE Dim_Origen (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT
);

CREATE TABLE Dim_Empresa (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nit          TEXT,
    direccion    TEXT,
    razon_social TEXT
);

-- =========================
-- Fact table
-- =========================

CREATE TABLE Hecho_Exportacion (
    fecha       INTEGER NOT NULL,
    empresa     INTEGER NOT NULL,
    aduana      INTEGER NOT NULL,
    destino     INTEGER NOT NULL,
    producto    INTEGER NOT NULL,
    origen      INTEGER NOT NULL,
    modalidad   INTEGER NOT NULL,
    transporte  INTEGER NOT NULL,
    transaccion INTEGER NOT NULL,

    FOREIGN KEY (fecha)       REFERENCES Dim_Fecha(id),
    FOREIGN KEY (empresa)     REFERENCES Dim_Empresa(id),
    FOREIGN KEY (aduana)      REFERENCES Dim_Aduana(id),
    FOREIGN KEY (destino)     REFERENCES Dim_Destino(id),
    FOREIGN KEY (producto)    REFERENCES Dim_Producto(id),
    FOREIGN KEY (origen)      REFERENCES Dim_Origen(id),
    FOREIGN KEY (modalidad)   REFERENCES Dim_Modalidad(id),
    FOREIGN KEY (transporte)  REFERENCES Dim_Transporte(id),
    FOREIGN KEY (transaccion) REFERENCES Dim_Transaccion(id)
);
