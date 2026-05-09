-- ============================================================
-- QUERIES ANALÍTICAS — IT KPI Dashboard Monterrey
-- Base: it_kpi_monterrey.db  (SQLite 3)
-- Compatible con Power BI → ODBC SQLite o importar CSV limpio
-- ============================================================


-- ------------------------------------------------------------
-- Q01: Ingreso total y margen bruto por empresa y año
--      KPI: Revenue YoY | Margen Bruto %
-- ------------------------------------------------------------
SELECT
    empresa,
    tipo_empresa,
    anio,
    SUM(ingresos_mxn)      AS ingresos_totales,
    SUM(costos_mxn)        AS costos_totales,
    SUM(margen_bruto_mxn)  AS margen_total,
    ROUND(SUM(margen_bruto_mxn) / NULLIF(SUM(ingresos_mxn), 0) * 100, 2) AS margen_pct
FROM ingresos
GROUP BY empresa, tipo_empresa, anio
ORDER BY anio, ingresos_totales DESC;


-- ------------------------------------------------------------
-- Q02: Crecimiento YoY de ingresos por empresa (2023 → 2024)
--      KPI: Crecimiento interanual %
-- ------------------------------------------------------------
WITH base AS (
    SELECT
        empresa,
        anio,
        SUM(ingresos_mxn) AS ingresos_anuales
    FROM ingresos
    GROUP BY empresa, anio
)
SELECT
    a.empresa,
    a.ingresos_anuales                                  AS ingresos_2023,
    b.ingresos_anuales                                  AS ingresos_2024,
    ROUND((b.ingresos_anuales - a.ingresos_anuales)
          / NULLIF(a.ingresos_anuales, 0) * 100, 2)     AS crecimiento_yoy_pct
FROM base a
JOIN base b ON a.empresa = b.empresa AND a.anio = 2023 AND b.anio = 2024
ORDER BY crecimiento_yoy_pct DESC;


-- ------------------------------------------------------------
-- Q03: Ingresos mensuales por tipo de empresa (tendencia)
--      KPI: Línea de tiempo mensual para Power BI
-- ------------------------------------------------------------
SELECT
    anio,
    mes,
    mes_nombre,
    trimestre,
    tipo_empresa,
    SUM(ingresos_mxn)             AS ingresos_mes,
    ROUND(AVG(margen_pct), 2)     AS margen_promedio_pct,
    SUM(empleados_activos)        AS headcount_total
FROM ingresos
GROUP BY anio, mes, mes_nombre, trimestre, tipo_empresa
ORDER BY anio, mes;


-- ------------------------------------------------------------
-- Q04: Salario promedio por rol y nivel
--      KPI: Benchmark salarial IT Monterrey
--      Fuente calibración: Hireline 2024 | CodersLink 2023
-- ------------------------------------------------------------
SELECT
    rol,
    nivel,
    COUNT(*)                                 AS num_empleados,
    ROUND(AVG(salario_mensual_neto_mxn), 0)  AS salario_promedio,
    ROUND(MIN(salario_mensual_neto_mxn), 0)  AS salario_minimo,
    ROUND(MAX(salario_mensual_neto_mxn), 0)  AS salario_maximo,
    ROUND(AVG(anios_experiencia), 1)         AS experiencia_promedio_anios
FROM empleados
WHERE activo = 1
GROUP BY rol, nivel
ORDER BY rol, CASE nivel WHEN 'Junior' THEN 1 WHEN 'Mid' THEN 2 WHEN 'Senior' THEN 3 END;


-- ------------------------------------------------------------
-- Q05: Distribución de empleados por empresa, rol y modalidad
--      KPI: Headcount | % Home Office | % Híbrido
-- ------------------------------------------------------------
SELECT
    empresa,
    tipo_empresa,
    rol,
    nivel,
    modalidad,
    COUNT(*)                                                         AS num_empleados,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY empresa), 2) AS pct_del_total_empresa
FROM empleados
WHERE activo = 1
GROUP BY empresa, tipo_empresa, rol, nivel, modalidad
ORDER BY empresa, num_empleados DESC;


-- ------------------------------------------------------------
-- Q06: Funnel de contratación mensual por empresa y rol
--      KPI: Tasa de conversión | Tiempo promedio de contratación
-- ------------------------------------------------------------
SELECT
    anio,
    trimestre,
    empresa,
    rol,
    SUM(candidatos_recibidos)          AS candidatos_totales,
    SUM(entrevistados)                 AS entrevistados_totales,
    SUM(ofertas_enviadas)              AS ofertas_totales,
    SUM(contratados)                   AS contratados_totales,
    ROUND(SUM(contratados) * 100.0
          / NULLIF(SUM(candidatos_recibidos), 0), 2) AS tasa_conversion_pct,
    ROUND(AVG(tiempo_contratacion_dias), 1)          AS tiempo_promedio_dias,
    fuente_principal
FROM contrataciones
GROUP BY anio, trimestre, empresa, rol, fuente_principal
ORDER BY anio, trimestre, contratados_totales DESC;


-- ------------------------------------------------------------
-- Q07: Top 5 roles con mayor demanda de contratación 2023-2024
--      KPI: Roles más contratados en el sector
-- ------------------------------------------------------------
SELECT
    rol,
    SUM(contratados)           AS total_contratados,
    SUM(candidatos_recibidos)  AS total_candidatos,
    ROUND(SUM(contratados) * 100.0 / NULLIF(SUM(candidatos_recibidos), 0), 2) AS conversion_pct,
    ROUND(AVG(tiempo_contratacion_dias), 1) AS dias_promedio_contratacion,
    COUNT(DISTINCT empresa)    AS empresas_contratando
FROM contrataciones
GROUP BY rol
ORDER BY total_contratados DESC
LIMIT 10;


-- ------------------------------------------------------------
-- Q08: Satisfacción por empresa y nivel (eNPS implícito)
--      KPI: Índice de satisfacción | Intención de salida %
-- ------------------------------------------------------------
SELECT
    empresa,
    nivel,
    anio,
    COUNT(*)                                      AS encuestados,
    ROUND(AVG(satisfaccion_general), 2)           AS sat_general,
    ROUND(AVG(satisfaccion_salario), 2)           AS sat_salario,
    ROUND(AVG(satisfaccion_ambiente), 2)          AS sat_ambiente,
    ROUND(AVG(satisfaccion_crecimiento), 2)       AS sat_crecimiento,
    ROUND(AVG(satisfaccion_liderazgo), 2)         AS sat_liderazgo,
    SUM(CASE WHEN intencion_salida = 'Sí' THEN 1 ELSE 0 END)   AS quiere_salir,
    ROUND(SUM(CASE WHEN intencion_salida = 'Sí' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_riesgo_rotacion
FROM satisfaccion
GROUP BY empresa, nivel, anio
ORDER BY pct_riesgo_rotacion DESC;


-- ------------------------------------------------------------
-- Q09: Proyectos: estado, desviación de presupuesto y satisfacción
--      KPI: On-Time Delivery | Budget Variance | CSAT Proyectos
-- ------------------------------------------------------------
SELECT
    empresa,
    estado,
    metodologia,
    cliente_sector,
    COUNT(*)                                          AS num_proyectos,
    ROUND(AVG(presupuesto_mxn), 2)                   AS presupuesto_promedio,
    ROUND(AVG(costo_real_mxn), 2)                    AS costo_real_promedio,
    ROUND(AVG(desviacion_presupuesto_pct), 2)        AS desviacion_promedio_pct,
    ROUND(AVG(satisfaccion_cliente), 2)              AS csat_promedio,
    ROUND(AVG(num_recursos), 1)                      AS recursos_promedio,
    SUM(presupuesto_mxn)                             AS presupuesto_total,
    SUM(costo_real_mxn)                              AS costo_real_total
FROM proyectos
GROUP BY empresa, estado, metodologia, cliente_sector
ORDER BY empresa, num_proyectos DESC;


-- ------------------------------------------------------------
-- Q10: Revenue por empleado por tipo de empresa (productividad)
--      KPI: Revenue/FTE — métrica estándar de consultoría
-- ------------------------------------------------------------
SELECT
    tipo_empresa,
    anio,
    ROUND(AVG(revenue_por_empleado_mxn), 2)     AS rev_por_empleado_promedio,
    ROUND(MIN(revenue_por_empleado_mxn), 2)     AS rev_por_empleado_min,
    ROUND(MAX(revenue_por_empleado_mxn), 2)     AS rev_por_empleado_max,
    SUM(empleados_activos)                       AS headcount_total,
    SUM(ingresos_mxn)                            AS ingresos_totales
FROM ingresos
GROUP BY tipo_empresa, anio
ORDER BY anio, rev_por_empleado_promedio DESC;


-- ------------------------------------------------------------
-- Q11: Brecha salarial por género y nivel
--      KPI: Gender Pay Gap — diversity analytics
-- ------------------------------------------------------------
SELECT
    e.genero,
    e.nivel,
    e.rol,
    COUNT(*)                                    AS num_empleados,
    ROUND(AVG(e.salario_mensual_neto_mxn), 0)  AS salario_promedio,
    ROUND(AVG(e.anios_experiencia), 1)          AS experiencia_promedio
FROM empleados e
WHERE e.activo = 1
GROUP BY e.genero, e.nivel, e.rol
ORDER BY e.rol, e.nivel, e.genero;


-- ------------------------------------------------------------
-- Q12: Fuentes de reclutamiento más efectivas
--      KPI: Calidad por canal (conversión) | Tiempo por canal
-- ------------------------------------------------------------
SELECT
    fuente_principal,
    SUM(candidatos_recibidos)   AS candidatos_totales,
    SUM(contratados)            AS contratados_totales,
    ROUND(SUM(contratados) * 100.0 / NULLIF(SUM(candidatos_recibidos), 0), 2) AS conversion_pct,
    ROUND(AVG(tiempo_contratacion_dias), 1)  AS tiempo_promedio_dias,
    COUNT(DISTINCT empresa)     AS empresas_que_la_usan
FROM contrataciones
GROUP BY fuente_principal
ORDER BY conversion_pct DESC;
