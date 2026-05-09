import pandas as pd
import sqlite3
import os
import sys
from datetime import datetime

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
RAW_DIR     = os.path.join(BASE_DIR, "..", "data", "raw")
PROC_DIR    = os.path.join(BASE_DIR, "..", "data", "processed")
SQL_DIR     = os.path.join(BASE_DIR, "..", "sql")
DB_PATH     = os.path.join(PROC_DIR, "it_kpi_monterrey.db")

os.makedirs(PROC_DIR, exist_ok=True)

SALARY_FLOOR = 8_000
SALARY_CEIL  = 200_000
SAT_MIN      = 1.0
SAT_MAX      = 5.0


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def leer_csv(nombre):
    ruta = os.path.join(RAW_DIR, nombre)
    if not os.path.exists(ruta):
        log(f"ERROR: No existe {ruta}")
        sys.exit(1)
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    log(f"Leído  {nombre:<26} {len(df):>6,} filas")
    return df


def limpiar_empleados(df):
    df = df.copy()
    df.drop_duplicates(subset=["empleado_id"], inplace=True)
    df.dropna(subset=["empleado_id", "empresa_id", "rol", "nivel", "salario_mensual_neto_mxn"], inplace=True)
    df["salario_mensual_neto_mxn"] = pd.to_numeric(df["salario_mensual_neto_mxn"], errors="coerce")
    df = df[(df["salario_mensual_neto_mxn"] >= SALARY_FLOOR) & (df["salario_mensual_neto_mxn"] <= SALARY_CEIL)]
    df["nombre"] = df["nombre"].str.strip().str.title()
    df["nivel"]  = df["nivel"].str.strip()
    df["activo"] = df["activo"].fillna(1).astype(int)
    df["anios_experiencia"] = df["anios_experiencia"].fillna(0).astype(int)
    df["fecha_ingreso"] = pd.to_datetime(df["fecha_ingreso"], errors="coerce").dt.strftime("%Y-%m-%d")
    df.dropna(subset=["fecha_ingreso"], inplace=True)
    return df


def limpiar_proyectos(df):
    df = df.copy()
    df.drop_duplicates(subset=["proyecto_id"], inplace=True)
    df.dropna(subset=["proyecto_id", "empresa_id", "presupuesto_mxn"], inplace=True)
    df["presupuesto_mxn"]  = pd.to_numeric(df["presupuesto_mxn"], errors="coerce").fillna(0)
    df["costo_real_mxn"]   = pd.to_numeric(df["costo_real_mxn"],  errors="coerce").fillna(0)
    df["satisfaccion_cliente"] = pd.to_numeric(df["satisfaccion_cliente"], errors="coerce")
    df["satisfaccion_cliente"] = df["satisfaccion_cliente"].clip(1.0, 5.0)
    df["desviacion_presupuesto_pct"] = pd.to_numeric(df["desviacion_presupuesto_pct"], errors="coerce").fillna(0)
    df["fecha_inicio"]       = pd.to_datetime(df["fecha_inicio"],       errors="coerce").dt.strftime("%Y-%m-%d")
    df["fecha_fin_estimada"] = pd.to_datetime(df["fecha_fin_estimada"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["nombre_proyecto"] = df["nombre_proyecto"].str.strip()
    df["estado"] = df["estado"].str.strip()
    return df


def limpiar_contrataciones(df):
    df = df.copy()
    df.drop_duplicates(subset=["contratacion_id"], inplace=True)
    df.dropna(subset=["contratacion_id", "empresa_id", "anio", "mes"], inplace=True)
    for col in ["candidatos_recibidos", "entrevistados", "ofertas_enviadas", "contratados"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        df[col] = df[col].clip(lower=0)
    df["tasa_conversion_pct"] = pd.to_numeric(df["tasa_conversion_pct"], errors="coerce").fillna(0).clip(0, 100)
    df["tiempo_contratacion_dias"] = pd.to_numeric(df["tiempo_contratacion_dias"], errors="coerce").fillna(30).astype(int)
    df["anio"] = df["anio"].astype(int)
    df["mes"]  = df["mes"].astype(int)
    return df


def limpiar_satisfaccion(df):
    df = df.copy()
    df.drop_duplicates(subset=["encuesta_id"], inplace=True)
    df.dropna(subset=["encuesta_id", "empleado_id", "empresa_id", "anio"], inplace=True)
    sat_cols = ["satisfaccion_general", "satisfaccion_salario", "satisfaccion_ambiente",
                "satisfaccion_crecimiento", "satisfaccion_liderazgo"]
    for col in sat_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].clip(SAT_MIN, SAT_MAX)
    df["intencion_salida"] = df["intencion_salida"].fillna("No")
    df["razon_posible_salida"] = df["razon_posible_salida"].fillna("N/A")
    df["anio"] = df["anio"].astype(int)
    return df


def limpiar_ingresos(df):
    df = df.copy()
    df.drop_duplicates(subset=["ingreso_id"], inplace=True)
    df.dropna(subset=["ingreso_id", "empresa_id", "anio", "mes"], inplace=True)
    for col in ["ingresos_mxn", "costos_mxn", "margen_bruto_mxn"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        df[col] = df[col].clip(lower=0)
    df["margen_pct"] = pd.to_numeric(df["margen_pct"], errors="coerce").fillna(0).clip(-100, 100)
    df["revenue_por_empleado_mxn"] = pd.to_numeric(df["revenue_por_empleado_mxn"], errors="coerce").fillna(0)
    df["empleados_activos"] = pd.to_numeric(df["empleados_activos"], errors="coerce").fillna(0).astype(int)
    df["anio"] = df["anio"].astype(int)
    df["mes"]  = df["mes"].astype(int)
    return df


def limpiar_empresas(df):
    df = df.copy()
    df = df.rename(columns={"id": "empresa_id"})
    df.drop_duplicates(subset=["empresa_id"], inplace=True)
    df.dropna(subset=["empresa_id", "nombre"], inplace=True)
    df["fundacion"] = pd.to_numeric(df["fundacion"], errors="coerce").fillna(2000).astype(int)
    df["empleados_base"] = pd.to_numeric(df["empleados_base"], errors="coerce").fillna(0).astype(int)
    return df


def guardar_csv_limpio(df, nombre):
    ruta = os.path.join(PROC_DIR, nombre)
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    log(f"  → processed/{nombre}")


def aplicar_schema(conn):
    schema_path = os.path.join(SQL_DIR, "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()


def cargar_tabla(conn, df, tabla, columnas):
    df_sel = df[columnas].copy()
    df_sel.to_sql(tabla, conn, if_exists="replace", index=False)
    log(f"  → tabla '{tabla}' cargada  ({len(df_sel):,} filas)")


def main():
    log("=" * 60)
    log("ETL — IT KPI Dashboard Monterrey")
    log("=" * 60)

    log("PASO 1: Lectura de CSV raw")
    df_emp  = leer_csv("empleados.csv")
    df_proy = leer_csv("proyectos.csv")
    df_cnt  = leer_csv("contrataciones.csv")
    df_sat  = leer_csv("satisfaccion.csv")
    df_ing  = leer_csv("ingresos.csv")
    df_co   = leer_csv("empresas_cat.csv")

    log("PASO 2: Limpieza y validación")
    df_emp  = limpiar_empleados(df_emp)
    df_proy = limpiar_proyectos(df_proy)
    df_cnt  = limpiar_contrataciones(df_cnt)
    df_sat  = limpiar_satisfaccion(df_sat)
    df_ing  = limpiar_ingresos(df_ing)
    df_co   = limpiar_empresas(df_co)

    log("PASO 3: Exportar CSVs limpios")
    guardar_csv_limpio(df_emp,  "empleados_clean.csv")
    guardar_csv_limpio(df_proy, "proyectos_clean.csv")
    guardar_csv_limpio(df_cnt,  "contrataciones_clean.csv")
    guardar_csv_limpio(df_sat,  "satisfaccion_clean.csv")
    guardar_csv_limpio(df_ing,  "ingresos_clean.csv")
    guardar_csv_limpio(df_co,   "empresas_clean.csv")

    log("PASO 4: Crear base de datos SQLite")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    aplicar_schema(conn)

    log("PASO 5: Carga a SQLite")
    cargar_tabla(conn, df_co, "empresas", [
        "empresa_id", "nombre", "tipo", "empleados_base", "fundacion"
    ])
    cargar_tabla(conn, df_emp, "empleados", [
        "empleado_id", "nombre", "genero", "empresa_id", "empresa", "tipo_empresa",
        "rol", "nivel", "salario_mensual_neto_mxn", "anios_experiencia",
        "tecnologias_principales", "ingles", "modalidad", "colonia_oficina",
        "fecha_ingreso", "activo"
    ])
    cargar_tabla(conn, df_proy, "proyectos", [
        "proyecto_id", "nombre_proyecto", "empresa_id", "empresa", "cliente_sector",
        "lider_proyecto_id", "fecha_inicio", "fecha_fin_estimada", "estado",
        "presupuesto_mxn", "costo_real_mxn", "desviacion_presupuesto_pct",
        "num_recursos", "metodologia", "satisfaccion_cliente"
    ])
    cargar_tabla(conn, df_cnt, "contrataciones", [
        "contratacion_id", "empresa_id", "empresa", "anio", "mes", "mes_nombre",
        "trimestre", "rol", "candidatos_recibidos", "entrevistados",
        "ofertas_enviadas", "contratados", "tasa_conversion_pct",
        "tiempo_contratacion_dias", "fuente_principal"
    ])
    cargar_tabla(conn, df_sat, "satisfaccion", [
        "encuesta_id", "empleado_id", "empresa_id", "empresa", "rol", "nivel",
        "anio", "satisfaccion_general", "satisfaccion_salario", "satisfaccion_ambiente",
        "satisfaccion_crecimiento", "satisfaccion_liderazgo", "intencion_salida",
        "razon_posible_salida"
    ])
    cargar_tabla(conn, df_ing, "ingresos", [
        "ingreso_id", "empresa_id", "empresa", "tipo_empresa", "anio", "mes",
        "mes_nombre", "trimestre", "ingresos_mxn", "costos_mxn", "margen_bruto_mxn",
        "margen_pct", "empleados_activos", "revenue_por_empleado_mxn"
    ])

    log("PASO 6: Verificación de integridad")
    tablas = ["empresas", "empleados", "proyectos", "contrataciones", "satisfaccion", "ingresos"]
    for tabla in tablas:
        n = conn.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
        log(f"  {tabla:<18} {n:>6,} registros  ✓")

    conn.close()
    log("=" * 60)
    log(f"Base de datos creada: {os.path.abspath(DB_PATH)}")
    log("ETL completado exitosamente.")
    log("=" * 60)


if __name__ == "__main__":
    main()
