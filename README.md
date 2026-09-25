# 📊 Tappx Data Model - Multi-Source EDA Explorer

Un explorador interactivo y dashboard de arquitectura de datos desarrollado con **Marimo** y **Python**. Esta herramienta permite realizar un Análisis Exploratorio de Datos (EDA) sobre el modelo de datos multifuente de **Tappx**, unificando metadatos de sistemas analíticos y transaccionales: **ClickHouse**, **MySQL-SL** y **BigQuery**.

---

## 🚀 Características Principales

* **🗄️ Arquitectura Multi-Fuente Unificada:** Análisis integrado de más de 7,600 columnas distribuidas entre bases de datos operacionales, réplicas de lectura y Data Warehouse.
* **🔎 Inspección de Campos y Payloads JSON:** Desglose detallado de variables clave OpenRTB (`ext`, `json_data`, `json_prices`, `json_device`) con esquemas internos de objetos y valores de muestra.
* **⚙️ Filtros Excluyentes en Cascada:** Selección dinámica y enlazada de fuentes de datos (`clickhouse`, `mysql-sl`, `bigquery`) que filtra en tiempo real las tablas y columnas disponibles.
* **🎨 Canvas SVG Interactivo:** Diagrama visual de tablas con tarjetas arrastrables (*drag & drop* mediante clic sostenido) y redimensionables. Las líneas de relación SVG se recalculan fluidamente en tiempo real durante el movimiento.
* **🌐 Matriz de Trazabilidad Transversal:** Sección dedicada a mapear las conexiones y claves de unión inter-fuente (e.g., `publisher`, `bundle`, `ad_unit`) entre diferentes tecnologías de bases de datos.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework Interactivo:** [Marimo Notebooks](https://marimo.io/)
* **Procesamiento de Datos:** Pandas
* **Visualización:** HTML5, CSS3, JavaScript (Drag & Drop, ResizeObserver, SVG Dinámico)
* **Control de Versiones:** Git & GitHub

---

## 📂 Estructura del Proyecto

```text
tappx-data-model-eda/
├── .venv/                      # Entorno virtual de Python
├── eda_data_model.py           # Script principal y reactivo de Marimo
├── reporte_data_model.html     # Reporte HTML final exportado (interactivo sin código)
├── merge.py                    # Script de unificación de catálogos CSV
├── schema_metadata.csv         # Catálogo unificado maestro (ClickHouse + MySQL + BigQuery)
├── schema_mysql_sl.csv         # Exportación de metadata desde mysql-sl.db.tappx.com
├── schema_bigquery.csv         # Exportación de metadata desde BigQuery (tappx_us_east4)
└── README.md                   # Documentación del proyecto