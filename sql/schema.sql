PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ============================================================
-- SCHEMA: it_kpi_monterrey.db
-- Sector IT Monterrey, Nuevo León — 2023-2024
-- ============================================================

CREATE TABLE IF NOT EXISTS empresas (
    empresa_id        TEXT PRIMARY KEY,
    nombre            TEXT NOT NULL,
    tipo              TEXT NOT NULL,
    empleados_base    INTEGER NOT NULL,
    fundacion         INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS empleados (
    empleado_id               TEXT PRIMARY KEY,
    nombre                    TEXT NOT NULL,
    genero                    TEXT NOT NULL CHECK (genero IN ('M', 'F')),
    empresa_id                TEXT NOT NULL REFERENCES empresas(empresa_id),
    empresa                   TEXT NOT NULL,
    tipo_empresa              TEXT NOT NULL,
    rol                       TEXT NOT NULL,
    nivel                     TEXT NOT NULL CHECK (nivel IN ('Junior', 'Mid', 'Senior')),
    salario_mensual_neto_mxn  INTEGER NOT NULL,
    anios_experiencia         INTEGER NOT NULL,
    tecnologias_principales   TEXT,
    ingles                    TEXT NOT NULL,
    modalidad                 TEXT NOT NULL CHECK (modalidad IN ('Presencial', 'Híbrido', 'Home Office')),
    colonia_oficina           TEXT,
    fecha_ingreso             TEXT NOT NULL,
    activo                    INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS proyectos (
    proyecto_id                  TEXT PRIMARY KEY,
    nombre_proyecto              TEXT NOT NULL,
    empresa_id                   TEXT NOT NULL REFERENCES empresas(empresa_id),
    empresa                      TEXT NOT NULL,
    cliente_sector               TEXT NOT NULL,
    lider_proyecto_id            TEXT,
    fecha_inicio                 TEXT NOT NULL,
    fecha_fin_estimada           TEXT NOT NULL,
    estado                       TEXT NOT NULL,
    presupuesto_mxn              REAL NOT NULL,
    costo_real_mxn               REAL NOT NULL,
    desviacion_presupuesto_pct   REAL NOT NULL,
    num_recursos                 INTEGER NOT NULL,
    metodologia                  TEXT NOT NULL,
    satisfaccion_cliente         REAL
);

CREATE TABLE IF NOT EXISTS contrataciones (
    contratacion_id           TEXT PRIMARY KEY,
    empresa_id                TEXT NOT NULL REFERENCES empresas(empresa_id),
    empresa                   TEXT NOT NULL,
    anio                      INTEGER NOT NULL,
    mes                       INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    mes_nombre                TEXT NOT NULL,
    trimestre                 TEXT NOT NULL,
    rol                       TEXT NOT NULL,
    candidatos_recibidos      INTEGER NOT NULL,
    entrevistados             INTEGER NOT NULL,
    ofertas_enviadas          INTEGER NOT NULL,
    contratados               INTEGER NOT NULL,
    tasa_conversion_pct       REAL NOT NULL,
    tiempo_contratacion_dias  INTEGER NOT NULL,
    fuente_principal          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS satisfaccion (
    encuesta_id               TEXT PRIMARY KEY,
    empleado_id               TEXT NOT NULL,
    empresa_id                TEXT NOT NULL REFERENCES empresas(empresa_id),
    empresa                   TEXT NOT NULL,
    rol                       TEXT NOT NULL,
    nivel                     TEXT NOT NULL,
    anio                      INTEGER NOT NULL,
    satisfaccion_general      REAL NOT NULL,
    satisfaccion_salario      REAL NOT NULL,
    satisfaccion_ambiente     REAL NOT NULL,
    satisfaccion_crecimiento  REAL NOT NULL,
    satisfaccion_liderazgo    REAL NOT NULL,
    intencion_salida          TEXT NOT NULL CHECK (intencion_salida IN ('No', 'Tal vez', 'Sí')),
    razon_posible_salida      TEXT
);

CREATE TABLE IF NOT EXISTS ingresos (
    ingreso_id                 TEXT PRIMARY KEY,
    empresa_id                 TEXT NOT NULL REFERENCES empresas(empresa_id),
    empresa                    TEXT NOT NULL,
    tipo_empresa               TEXT NOT NULL,
    anio                       INTEGER NOT NULL,
    mes                        INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    mes_nombre                 TEXT NOT NULL,
    trimestre                  TEXT NOT NULL,
    ingresos_mxn               REAL NOT NULL,
    costos_mxn                 REAL NOT NULL,
    margen_bruto_mxn           REAL NOT NULL,
    margen_pct                 REAL NOT NULL,
    empleados_activos          INTEGER NOT NULL,
    revenue_por_empleado_mxn   REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_empleados_empresa    ON empleados(empresa_id);
CREATE INDEX IF NOT EXISTS idx_empleados_rol        ON empleados(rol);
CREATE INDEX IF NOT EXISTS idx_empleados_nivel      ON empleados(nivel);
CREATE INDEX IF NOT EXISTS idx_empleados_activo     ON empleados(activo);
CREATE INDEX IF NOT EXISTS idx_proyectos_empresa    ON proyectos(empresa_id);
CREATE INDEX IF NOT EXISTS idx_proyectos_estado     ON proyectos(estado);
CREATE INDEX IF NOT EXISTS idx_contrataciones_anio  ON contrataciones(anio, mes);
CREATE INDEX IF NOT EXISTS idx_contrataciones_emp   ON contrataciones(empresa_id);
CREATE INDEX IF NOT EXISTS idx_satisfaccion_empresa ON satisfaccion(empresa_id);
CREATE INDEX IF NOT EXISTS idx_satisfaccion_anio    ON satisfaccion(anio);
CREATE INDEX IF NOT EXISTS idx_ingresos_empresa     ON ingresos(empresa_id);
CREATE INDEX IF NOT EXISTS idx_ingresos_periodo     ON ingresos(anio, mes);
