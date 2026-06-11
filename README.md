# 🖥️ IT KPI Dashboard — Sector Tecnología Monterrey, N.L.

> **Análisis de métricas clave del ecosistema IT en Nuevo León** | Data Analytics · ETL · SQLite · Power BI

---

## 📋 Descripción del Proyecto / Project Description

**ES:** Este proyecto simula un pipeline completo de Data Analytics para el sector de Tecnologías de la Información en Monterrey, Nuevo León. Los datos están calibrados con fuentes públicas reales (Hireline, CodersLink, Csoftmty) y cubren 12 empresas IT reales del ecosistema regiomontano: Accenture, TCS, Neoris, Infosys, Globant, BairesDev, Hexaware, AZKA IT, Deintec, Axsis Tecnología, Skye Group y TI Monterrey.

**EN:** This project simulates a complete Data Analytics pipeline for the IT sector in Monterrey, Nuevo León. Data is calibrated against real public benchmarks (Hireline 2024, CodersLink 2023, Csoftmty cluster data) and covers 12 real IT companies from the Monterrey tech ecosystem.

---

## 🏢 Problema de Negocio / Business Problem

El clúster IT de Nuevo León (Csoftmty) agrupa más de 14,000 ingenieros con un crecimiento del 30% anual. Las empresas del sector necesitan visibilidad sobre:

- ¿Cuáles son los roles más demandados y cuánto tardan en contratarse?
- ¿Qué empresas tienen mayor margen de rentabilidad y revenue por empleado?
- ¿Cómo se comparan los salarios contra los benchmarks del mercado?
- ¿Qué tan satisfechos están los empleados y cuál es el riesgo de rotación?
- ¿Los proyectos se entregan dentro del presupuesto y con satisfacción del cliente?

---

## 📊 KPIs del Dashboard

| # | KPI | Tabla fuente |
|---|-----|-------------|
| 1 | Ingresos totales y margen bruto por empresa/año | `ingresos` |
| 2 | Crecimiento YoY de ingresos (2023 → 2024) | `ingresos` |
| 3 | Tendencia mensual de ingresos por tipo de empresa | `ingresos` |
| 4 | Benchmark salarial por rol y nivel (Junior/Mid/Senior) | `empleados` |
| 5 | Distribución de headcount por modalidad (Híbrido/HO) | `empleados` |
| 6 | Funnel de contratación: conversión y tiempo promedio | `contrataciones` |
| 7 | Top roles más contratados del sector | `contrataciones` |
| 8 | Satisfacción y riesgo de rotación por empresa | `satisfaccion` |
| 9 | Estado de proyectos: desviación de presupuesto y CSAT | `proyectos` |
| 10 | Revenue por empleado (productividad) por tipo de empresa | `ingresos` |
| 11 | Brecha salarial por género y nivel | `empleados` |
| 12 | Efectividad de canales de reclutamiento | `contrataciones` |

---

## 🛠️ Stack Tecnológico / Tech Stack

| Herramienta | Uso | Versión | Costo |
|-------------|-----|---------|-------|
| **Python 3.12** | Generación de datos y ETL | 3.12+ | Gratuito |
| **pandas** | Manipulación y limpieza de datos | 2.x | Gratuito |
| **numpy** | Generación de distribuciones estadísticas | 1.x | Gratuito |
| **SQLite** | Base de datos local (incluida en Python) | 3.x | Gratuito |
| **Power BI Desktop** | Dashboard interactivo final | Latest | Gratuito |
| **GitHub** | Control de versiones y portafolio | — | Gratuito |

---

## 📁 Estructura del Proyecto

```
it-kpi-dashboard-monterrey/
├── data/
│   ├── raw/                    # CSVs generados por generate_data.py
│   │   ├── empleados.csv
│   │   ├── proyectos.csv
│   │   ├── contrataciones.csv
│   │   ├── satisfaccion.csv
│   │   ├── ingresos.csv
│   │   └── empresas_cat.csv
│   └── processed/              # Salida del ETL
│       ├── *_clean.csv         # CSVs limpios para Power BI
│       └── it_kpi_monterrey.db # Base de datos SQLite
├── sql/
│   ├── schema.sql              # Definición de tablas e índices
│   └── queries.sql             # 12 queries analíticas para el dashboard
├── python/
│   ├── generate_data.py        # Generador de datos calibrados
│   └── etl.py                  # Pipeline ETL: limpieza y carga
├── screenshots/                # Capturas del dashboard (agregar aquí)
└── README.md
```

---

## 🚀 Cómo Ejecutar / How to Run

### Pre-requisitos

1. Instalar **Python 3.12**: https://www.python.org/downloads/  
   ⚠️ Marcar la casilla **"Add Python to PATH"** durante la instalación.

2. Instalar **Power BI Desktop** (gratuito):  
   https://powerbi.microsoft.com/es-es/desktop/

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/it-kpi-dashboard-monterrey.git
cd it-kpi-dashboard-monterrey

# 2. Instalar dependencias Python
pip install pandas numpy
```

### Ejecución

```bash
# Paso 1: Generar los datos (~12,500 filas)
python python/generate_data.py

# Paso 2: Limpiar y cargar a SQLite
python python/etl.py
```

Después del paso 2 tendrás:
- `data/processed/it_kpi_monterrey.db` — base de datos SQLite lista
- `data/processed/*_clean.csv` — CSVs limpios para importar a Power BI

### Conectar a Power BI

1. Abrir Power BI Desktop
2. **Obtener datos** → **Texto/CSV**
3. Importar los archivos `data/processed/*_clean.csv`
4. Usar las queries de `sql/queries.sql` como referencia para las medidas DAX

---

## 📐 Fuentes de Calibración de Datos

Los salarios, volúmenes de contratación y métricas de negocio están basados en:

| Fuente | Dato calibrado |
|--------|---------------|
| **Hireline — Reporte Mercado Laboral TI México 2024** | Salarios por rol y nivel (Junior $21k, Mid $32k, Senior $44k+ MXN) |
| **CodersLink — Reporte Salarios TI México 2023** | Distribución salarial y perfil del mercado NL |
| **RHPlus Consultores — Encuesta Compensaciones TI 2023** | Benchmark senior y especialidades |
| **Executrain / TripleTen 2024** | Data Analyst Monterrey $24k–$27k MXN junior |
| **Csoftmty — Clúster TIC Nuevo León** | 14,000+ ingenieros en NL, crecimiento 30% anual |

---

| Vista | Descripción |
|-------|-------------|
| `screenshots/01_revenue_overview.png` | Ingresos y margen por empresa |
| `screenshots/02_salary_benchmark.png` | Benchmark salarial por rol |
| `screenshots/03_hiring_funnel.png` | Funnel de contratación |
| `screenshots/04_satisfaction.png` | Satisfacción y rotación |
| `screenshots/05_projects.png` | Estado y desviación de proyectos |

---

## 👤 Autor

**Jesús Alejandro Basualdo** · Estudiante de Ingeniería en Tecnología de Software — FIME, UANL  
📍 Monterrey, Nuevo León, México  
🔗 [LinkedIn](https://linkedin.com/in/TU_PERFIL) · [GitHub](https://github.com/TU_USUARIO)

---

*Proyecto de portafolio para prácticas profesionales en empresas de tecnología de Nuevo León.*
