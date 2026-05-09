import pandas as pd
import numpy as np
import os
from datetime import date, timedelta
import random

np.random.seed(2024)
random.seed(2024)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

EMPRESAS = [
    {"id": "E01", "nombre": "Accenture Monterrey",       "tipo": "Consultoría Global",     "empleados_base": 1800, "fundacion": 2008},
    {"id": "E02", "nombre": "Tata Consultancy Services", "tipo": "Outsourcing Global",     "empleados_base": 1200, "fundacion": 2010},
    {"id": "E03", "nombre": "Neoris",                    "tipo": "Consultoría Regional",   "empleados_base": 950,  "fundacion": 2000},
    {"id": "E04", "nombre": "Infosys Monterrey",         "tipo": "Outsourcing Global",     "empleados_base": 820,  "fundacion": 2015},
    {"id": "E05", "nombre": "Globant Monterrey",         "tipo": "Software Factory",       "empleados_base": 680,  "fundacion": 2018},
    {"id": "E06", "nombre": "BairesDev",                 "tipo": "Software Factory",       "empleados_base": 510,  "fundacion": 2019},
    {"id": "E07", "nombre": "Hexaware Technologies",     "tipo": "Outsourcing Global",     "empleados_base": 440,  "fundacion": 2016},
    {"id": "E08", "nombre": "AZKA IT Consulting",        "tipo": "Consultoría Local",      "empleados_base": 320,  "fundacion": 2012},
    {"id": "E09", "nombre": "Deintec",                   "tipo": "Consultoría Local",      "empleados_base": 280,  "fundacion": 2008},
    {"id": "E10", "nombre": "Axsis Tecnología",          "tipo": "Desarrollo de Software", "empleados_base": 210,  "fundacion": 1999},
    {"id": "E11", "nombre": "Skye Group",                "tipo": "Consultoría Regional",   "empleados_base": 190,  "fundacion": 2011},
    {"id": "E12", "nombre": "TI Monterrey",              "tipo": "Consultoría Local",      "empleados_base": 150,  "fundacion": 2004},
]

ROLES = {
    "Data Analyst":          {"nivel_min": "Junior", "demanda": 0.14},
    "Software Developer":    {"nivel_min": "Junior", "demanda": 0.22},
    "Backend Developer":     {"nivel_min": "Junior", "demanda": 0.13},
    "Frontend Developer":    {"nivel_min": "Junior", "demanda": 0.09},
    "Full Stack Developer":  {"nivel_min": "Junior", "demanda": 0.11},
    "DevOps Engineer":       {"nivel_min": "Mid",    "demanda": 0.07},
    "Cloud Architect":       {"nivel_min": "Mid",    "demanda": 0.05},
    "Scrum Master":          {"nivel_min": "Mid",    "demanda": 0.06},
    "Project Manager":       {"nivel_min": "Mid",    "demanda": 0.06},
    "Cybersecurity Analyst": {"nivel_min": "Junior", "demanda": 0.07},
}

SALARIOS = {
    "Data Analyst":          {"Junior": (22000, 28000), "Mid": (30000, 42000), "Senior": (45000, 65000)},
    "Software Developer":    {"Junior": (20000, 27000), "Mid": (32000, 45000), "Senior": (48000, 72000)},
    "Backend Developer":     {"Junior": (22000, 30000), "Mid": (35000, 48000), "Senior": (52000, 78000)},
    "Frontend Developer":    {"Junior": (19000, 26000), "Mid": (28000, 40000), "Senior": (42000, 62000)},
    "Full Stack Developer":  {"Junior": (21000, 29000), "Mid": (33000, 46000), "Senior": (50000, 75000)},
    "DevOps Engineer":       {"Junior": (28000, 36000), "Mid": (40000, 55000), "Senior": (60000, 88000)},
    "Cloud Architect":       {"Junior": (32000, 42000), "Mid": (48000, 65000), "Senior": (70000, 105000)},
    "Scrum Master":          {"Junior": (28000, 36000), "Mid": (42000, 54000), "Senior": (56000, 80000)},
    "Project Manager":       {"Junior": (30000, 40000), "Mid": (45000, 60000), "Senior": (62000, 90000)},
    "Cybersecurity Analyst": {"Junior": (25000, 34000), "Mid": (38000, 52000), "Senior": (55000, 82000)},
}

TECNOLOGIAS = {
    "Data Analyst":          ["SQL", "Python", "Power BI", "Excel", "Tableau", "Databricks"],
    "Software Developer":    ["Java", "Python", "C#", ".NET", "Spring Boot", "Kotlin"],
    "Backend Developer":     ["Node.js", "Python", "Java", "Go", "FastAPI", "PostgreSQL"],
    "Frontend Developer":    ["React", "Angular", "Vue.js", "TypeScript", "Next.js", "Tailwind"],
    "Full Stack Developer":  ["React", "Node.js", "MongoDB", "PostgreSQL", "Docker", "GraphQL"],
    "DevOps Engineer":       ["Docker", "Kubernetes", "Jenkins", "Terraform", "AWS", "GitHub Actions"],
    "Cloud Architect":       ["AWS", "Azure", "GCP", "Kubernetes", "Terraform", "CDK"],
    "Scrum Master":          ["Jira", "Confluence", "Azure DevOps", "SAFe", "Kanban", "OKRs"],
    "Project Manager":       ["MS Project", "Jira", "SAP", "PMP", "Prince2", "Clarity"],
    "Cybersecurity Analyst": ["SIEM", "Nessus", "Palo Alto", "ISO 27001", "CISSP", "Splunk"],
}

COLONIAS = [
    "San Pedro Garza García", "Col. Del Valle", "Col. Obispado", "Col. Contry",
    "Cintermex Business Park", "Santa Catarina", "Col. Cumbres", "Apodaca",
    "Col. Residencial San Agustín", "García", "Escobedo", "Col. Centro",
]

CLIENTES_SECTOR = [
    "Manufactura Automotriz", "Banca y Finanzas", "Retail y E-commerce",
    "Salud y Farmacéutico", "Energía y Utilities", "Gobierno y Sector Público",
    "Telecomunicaciones", "Logística y Cadena de Suministro",
]

PROYECTOS_NOMBRES = [
    "Transformación Digital ERP", "Migración a la Nube AWS", "Implementación SAP S/4HANA",
    "Plataforma de Analytics BI", "Modernización de Infraestructura", "Automatización RPA",
    "Ciberseguridad Zero Trust", "Portal Omnicanal Cliente", "Data Lake Empresarial",
    "DevOps Pipeline CI/CD", "Chatbot IA Servicio al Cliente", "Integración Sistemas Legados",
    "Dashboard KPI Ejecutivo", "API Gateway Microservicios", "Nearshoring Center of Excellence",
]

NOMBRES_M = ["Carlos", "Alejandro", "Luis", "Miguel", "Javier", "Roberto", "Fernando",
             "Eduardo", "David", "Ricardo", "Jorge", "Andrés", "Daniel", "Héctor",
             "Óscar", "Rodrigo", "Arturo", "Gerardo", "Sergio", "Manuel"]
NOMBRES_F = ["María", "Ana", "Sofía", "Valentina", "Fernanda", "Paola", "Karla",
             "Laura", "Diana", "Claudia", "Andrea", "Gabriela", "Verónica", "Daniela",
             "Mónica", "Patricia", "Adriana", "Elena", "Ximena", "Brenda"]
APELLIDOS  = ["García", "Martínez", "López", "González", "Rodríguez", "Pérez", "Sánchez",
              "Ramírez", "Torres", "Flores", "Rivera", "Morales", "Jiménez", "Hernández",
              "Díaz", "Vázquez", "Cruz", "Reyes", "Garza", "Treviño", "Salinas", "Cantú",
              "Villarreal", "Cavazos", "Elizondo", "Guajardo", "Longoria", "Cárdenas"]


def generar_empleados():
    registros = []
    emp_id = 1
    pesos_rol = [ROLES[r]["demanda"] for r in ROLES]
    nivel_pesos = {"Junior": 0.35, "Mid": 0.45, "Senior": 0.20}

    for empresa in EMPRESAS:
        n = empresa["empleados_base"] + np.random.randint(-30, 80)
        for _ in range(n):
            genero = random.choice(["M", "F"])
            nombre = random.choice(NOMBRES_M if genero == "M" else NOMBRES_F)
            apellido = f"{random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"
            rol = random.choices(list(ROLES.keys()), weights=pesos_rol)[0]

            niveles_disponibles = ["Junior", "Mid", "Senior"] if ROLES[rol]["nivel_min"] == "Junior" else ["Mid", "Senior"]
            nivel = random.choices(
                niveles_disponibles,
                weights=[nivel_pesos[n] for n in niveles_disponibles]
            )[0]

            rango = SALARIOS[rol][nivel]
            salario = int(round(np.random.uniform(rango[0], rango[1]), -2))
            anios_exp = {"Junior": np.random.randint(0, 3), "Mid": np.random.randint(3, 7), "Senior": np.random.randint(7, 18)}[nivel]
            fecha_ingreso = date(2023, 1, 1) - timedelta(days=np.random.randint(0, 365 * 3))
            modalidad = random.choices(["Presencial", "Híbrido", "Home Office"], weights=[0.25, 0.50, 0.25])[0]
            tech = " | ".join(random.sample(TECNOLOGIAS[rol], k=3))
            ingles = random.choices(["Básico", "Intermedio", "Avanzado", "Bilingüe"], weights=[0.15, 0.30, 0.35, 0.20])[0]

            registros.append({
                "empleado_id":            f"EMP{emp_id:05d}",
                "nombre":                 f"{nombre} {apellido}",
                "genero":                 genero,
                "empresa_id":             empresa["id"],
                "empresa":                empresa["nombre"],
                "tipo_empresa":           empresa["tipo"],
                "rol":                    rol,
                "nivel":                  nivel,
                "salario_mensual_neto_mxn": salario,
                "anios_experiencia":      anios_exp,
                "tecnologias_principales": tech,
                "ingles":                 ingles,
                "modalidad":              modalidad,
                "colonia_oficina":        random.choice(COLONIAS),
                "fecha_ingreso":          fecha_ingreso.strftime("%Y-%m-%d"),
                "activo":                 random.choices([1, 0], weights=[0.92, 0.08])[0],
            })
            emp_id += 1

    return pd.DataFrame(registros)


def generar_proyectos(df_emp):
    registros = []
    proy_id = 1

    for empresa in EMPRESAS:
        n = int(empresa["empleados_base"] / 40) + np.random.randint(2, 8)
        emp_empresa = df_emp[df_emp["empresa_id"] == empresa["id"]]

        for _ in range(n):
            inicio = date(2023, 1, 1) + timedelta(days=np.random.randint(0, 730))
            duracion = np.random.randint(60, 540)
            fin = inicio + timedelta(days=duracion)
            estado = "En Curso" if fin > date(2024, 12, 31) else "Completado"
            if inicio > date(2024, 6, 1):
                estado = random.choice(["En Curso", "En Planeación"])

            presupuesto = np.random.uniform(800_000, 15_000_000)
            desviacion  = np.random.uniform(-0.10, 0.25)
            costo_real  = presupuesto * (1 + desviacion)
            n_recursos  = np.random.randint(4, 25)
            lider       = emp_empresa.iloc[0]["empleado_id"] if len(emp_empresa) > 0 else "N/A"

            registros.append({
                "proyecto_id":           f"PRY{proy_id:04d}",
                "nombre_proyecto":       random.choice(PROYECTOS_NOMBRES),
                "empresa_id":            empresa["id"],
                "empresa":               empresa["nombre"],
                "cliente_sector":        random.choice(CLIENTES_SECTOR),
                "lider_proyecto_id":     lider,
                "fecha_inicio":          inicio.strftime("%Y-%m-%d"),
                "fecha_fin_estimada":    fin.strftime("%Y-%m-%d"),
                "estado":                estado,
                "presupuesto_mxn":       round(presupuesto, 2),
                "costo_real_mxn":        round(costo_real, 2),
                "desviacion_presupuesto_pct": round(desviacion * 100, 2),
                "num_recursos":          n_recursos,
                "metodologia":           random.choices(
                    ["Agile/Scrum", "SAFe", "Waterfall", "Kanban", "Híbrida"],
                    weights=[0.40, 0.20, 0.15, 0.10, 0.15]
                )[0],
                "satisfaccion_cliente":  round(np.random.uniform(3.0, 5.0), 1),
            })
            proy_id += 1

    return pd.DataFrame(registros)


def generar_contrataciones():
    registros = []
    cnt_id = 1

    for empresa in EMPRESAS:
        for anio in [2023, 2024]:
            for mes in range(1, 13):
                for rol, info in ROLES.items():
                    volumen = max(0, int(np.random.poisson(
                        empresa["empleados_base"] / 120 * info["demanda"] * 12
                    )))
                    if volumen == 0 and random.random() > 0.55:
                        continue

                    candidatos  = max(5, volumen * np.random.randint(8, 20))
                    entrevistas = int(candidatos * np.random.uniform(0.25, 0.45))
                    ofertas     = max(1, int(entrevistas * np.random.uniform(0.20, 0.40)))
                    contratados = max(0, int(ofertas * np.random.uniform(0.60, 0.90)))

                    registros.append({
                        "contratacion_id":                  f"CNT{cnt_id:05d}",
                        "empresa_id":                       empresa["id"],
                        "empresa":                          empresa["nombre"],
                        "anio":                             anio,
                        "mes":                              mes,
                        "mes_nombre":                       date(anio, mes, 1).strftime("%B"),
                        "trimestre":                        f"Q{((mes - 1) // 3) + 1}",
                        "rol":                              rol,
                        "candidatos_recibidos":             candidatos,
                        "entrevistados":                    entrevistas,
                        "ofertas_enviadas":                 ofertas,
                        "contratados":                      contratados,
                        "tasa_conversion_pct":              round(contratados / candidatos * 100, 2) if candidatos > 0 else 0,
                        "tiempo_contratacion_dias":         np.random.randint(18, 65),
                        "fuente_principal":                 random.choices(
                            ["LinkedIn", "OCC Mundial", "Glassdoor", "Referidos", "Csoftmty Jobs", "Universidad UANL/ITESM"],
                            weights=[0.35, 0.20, 0.12, 0.18, 0.08, 0.07]
                        )[0],
                    })
                    cnt_id += 1

    return pd.DataFrame(registros)


def generar_satisfaccion(df_emp):
    registros = []
    enc_id = 1
    modalidad_bonus = {"Home Office": 0.30, "Híbrido": 0.15, "Presencial": 0.00}

    for _, emp in df_emp.iterrows():
        for anio in [2023, 2024]:
            if random.random() > 0.72:
                continue

            base = {"Junior": np.random.uniform(3.0, 4.5),
                    "Mid":    np.random.uniform(3.2, 4.7),
                    "Senior": np.random.uniform(3.5, 5.0)}[emp["nivel"]]

            sat = min(5.0, base + modalidad_bonus[emp["modalidad"]] + np.random.normal(0, 0.2))

            registros.append({
                "encuesta_id":            f"ENC{enc_id:06d}",
                "empleado_id":            emp["empleado_id"],
                "empresa_id":             emp["empresa_id"],
                "empresa":                emp["empresa"],
                "rol":                    emp["rol"],
                "nivel":                  emp["nivel"],
                "anio":                   anio,
                "satisfaccion_general":   round(sat, 1),
                "satisfaccion_salario":   round(min(5.0, sat + np.random.normal(-0.2, 0.3)), 1),
                "satisfaccion_ambiente":  round(min(5.0, sat + np.random.normal(0.1, 0.2)), 1),
                "satisfaccion_crecimiento": round(min(5.0, sat + np.random.normal(-0.1, 0.3)), 1),
                "satisfaccion_liderazgo": round(min(5.0, sat + np.random.normal(0.0, 0.25)), 1),
                "intencion_salida":       random.choices(["No", "Tal vez", "Sí"], weights=[0.55, 0.30, 0.15])[0],
                "razon_posible_salida":   random.choices(
                    ["Mejor salario", "Trabajo remoto", "Crecimiento profesional",
                     "Cambio de ciudad", "Startup propia", "N/A"],
                    weights=[0.30, 0.20, 0.25, 0.08, 0.07, 0.10]
                )[0],
            })
            enc_id += 1

    return pd.DataFrame(registros)


def generar_ingresos():
    registros = []
    ing_id = 1
    revenue_por_empleado = {
        "Consultoría Global":     (850_000, 1_200_000),
        "Outsourcing Global":     (700_000,   950_000),
        "Consultoría Regional":   (600_000,   850_000),
        "Software Factory":       (650_000,   900_000),
        "Consultoría Local":      (500_000,   750_000),
        "Desarrollo de Software": (550_000,   800_000),
    }
    estacionalidad = {1: 0.07, 2: 0.07, 3: 0.08, 4: 0.08, 5: 0.09, 6: 0.09,
                      7: 0.08, 8: 0.09, 9: 0.09, 10: 0.09, 11: 0.08, 12: 0.09}

    for empresa in EMPRESAS:
        rango = revenue_por_empleado[empresa["tipo"]]
        rev_base = np.random.uniform(rango[0], rango[1])
        crecimiento = np.random.uniform(0.08, 0.35)

        for anio in [2023, 2024]:
            factor = 1.0 if anio == 2023 else (1 + crecimiento)
            ingreso_anual = empresa["empleados_base"] * rev_base * factor

            for mes in range(1, 13):
                ingresos  = ingreso_anual * estacionalidad[mes] * np.random.uniform(0.92, 1.08)
                costos    = ingresos * np.random.uniform(0.58, 0.72)
                margen    = ingresos - costos
                emp_mes   = empresa["empleados_base"] + np.random.randint(-20, 50)

                registros.append({
                    "ingreso_id":              f"ING{ing_id:05d}",
                    "empresa_id":              empresa["id"],
                    "empresa":                 empresa["nombre"],
                    "tipo_empresa":            empresa["tipo"],
                    "anio":                    anio,
                    "mes":                     mes,
                    "mes_nombre":              date(anio, mes, 1).strftime("%B"),
                    "trimestre":               f"Q{((mes - 1) // 3) + 1}",
                    "ingresos_mxn":            round(ingresos, 2),
                    "costos_mxn":              round(costos, 2),
                    "margen_bruto_mxn":        round(margen, 2),
                    "margen_pct":              round((margen / ingresos) * 100, 2),
                    "empleados_activos":       emp_mes,
                    "revenue_por_empleado_mxn": round(ingresos / emp_mes, 2),
                })
                ing_id += 1

    return pd.DataFrame(registros)


def main():
    print("=" * 65)
    print("  IT KPI Dashboard — Sector Tecnología Monterrey, N.L.")
    print("  Fuentes de calibración salarial:")
    print("    · Hireline Reporte Mercado Laboral TI 2023-2024")
    print("    · CodersLink Reporte Salarios TI México 2023")
    print("    · RHPlus Consultores Encuesta Compensaciones TI 2023")
    print("    · Csoftmty: 14,000+ ingenieros NL, crecimiento 30%/año")
    print("    · Executrain: Data Analyst Mty $24k-$27k MXN (junior)")
    print("=" * 65)

    df_emp  = generar_empleados()
    df_proy = generar_proyectos(df_emp)
    df_cnt  = generar_contrataciones()
    df_sat  = generar_satisfaccion(df_emp.sample(min(900, len(df_emp)), random_state=42))
    df_ing  = generar_ingresos()
    df_emp_cat = pd.DataFrame(EMPRESAS)

    datasets = {
        "empleados.csv":      df_emp,
        "proyectos.csv":      df_proy,
        "contrataciones.csv": df_cnt,
        "satisfaccion.csv":   df_sat,
        "ingresos.csv":       df_ing,
        "empresas_cat.csv":   df_emp_cat,
    }

    for nombre, df in datasets.items():
        ruta = os.path.join(OUTPUT_DIR, nombre)
        df.to_csv(ruta, index=False, encoding="utf-8-sig")
        print(f"  ✓ {nombre:<26} {len(df):>6,} filas")

    total = sum(len(d) for d in datasets.values())
    print(f"\n  Total: {total:,} filas  |  {len(datasets)} archivos")
    print(f"  Directorio: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 65)


if __name__ == "__main__":
    main()
