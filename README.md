# 📊 Tappx Data Model - Multi-Source EDA Explorer
---

## 📌 Resumen Ejecutivo de la Solución

### 1. ¿Qué se ha construido? (Propósito)
* **Mapa visual e interactivo de metadatos:** Aplicación web que unifica la infraestructura de datos de Tappx (ClickHouse, MySQL-SL y BigQuery) en una sola interfaz interactiva[cite: 6].
* **Descubrimiento de datos simplificado:** Elimina la necesidad de ejecutar consultas SQL de inspección (`DESCRIBE`, `INFORMATION_SCHEMA`) para ubicar tablas y campos[cite: 6].
* **Cero costo de infraestructura:** Compilada en **WebAssembly (WASM)** y alojada en **GitHub Pages**, ejecutándose 100% en el navegador del cliente sin consumo de servidores[cite: 6].

---

### 2. ¿Cómo está configurado? (Arquitectura Técnica)
* **Pipeline de Metadatos:**
  * Dataset maestro (`schema_metadata.csv`) que consolida **más de 7,600 columnas** de las 3 fuentes de datos principales[cite: 6].
  * Script automatizado (`merge.py`) para procesar y actualizar nuevos esquemas[cite: 6].
* **Stack Frontend:**
  * Desarrollado en **Python 3.11** mediante **Marimo** (framework reactivo basado en DAGs)[cite: 6].
  * **Canvas interactivo (HTML5 / CSS3 / JS):** Tarjetas con funcionalidades *drag & drop*, redimensionado en tiempo real y conexiones vectoriales dinámicas en SVG[cite: 6].
* **Despliegue CI/CD:** Pipeline automatizado en GitHub Actions (`deploy.yml`) que compila a HTML/WASM con cada *push* a la rama `master`[cite: 6].

---

### 3. ¿Qué muestra? (Funcionalidades Clave)
* **Filtros en cascada:** Selección dinámica del motor de BD (`clickhouse`, `mysql-sl`, `bigquery`) que filtra instantáneamente tablas y columnas disponibles[cite: 6].
* **Inspección de Payloads JSON (OpenRTB):** Desglose del esquema interno de objetos complejos como `ext`, `json_data`, `json_prices` y `json_device` con valores de muestra[cite: 6].
* **Canvas ERD Interactivo:** Diagrama visual entidad-relación donde se pueden reordenar las tablas y visualizar las conexiones recalculadas al vuelo[cite: 6].
* **Matriz de Trazabilidad Inter-Fuente:** Mapeo directo de claves y dimensiones comunes (`publisher`, `bundle`, `ad_unit`) para cruzar información entre la base operacional, los logs en tiempo real y el Data Warehouse[cite: 6].

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen?logo=github)](https://lucianoavalos.github.io/tappx-data-model-eda/)
[![Marimo](https://img.shields.io/badge/Powered%20by-Marimo-10B981?logo=python)](https://marimo.io/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

### 💡 ¿Qué es esta aplicación? (Resumen para perfil no técnico)
Esta herramienta es un **mapa interactivo e inteligente** de toda la infraestructura de datos de **Tappx**. Permite a cualquier persona explora y entender en segundos qué información guardan nuestros diferentes motores de base de datos (**ClickHouse**, **MySQL** y **BigQuery**), cómo se conectan las tablas entre sí y qué contiene cada campo dentro de las transacciones publicitarias en tiempo real (OpenRTB). Elimina la necesidad de hacer consultas técnicas complejas (SQL) para descubrir dónde reside cada dato.

---

## 🚀 Características Principales

* **🗄️ Arquitectura Multi-Fuente Unificada:** Análisis integrado de más de 7,600 columnas distribuidas entre bases de datos operacionales, réplicas de lectura y Data Warehouse.
* **🔎 Inspección de Campos y Payloads JSON:** Desglose detallado de variables clave OpenRTB (`ext`, `json_data`, `json_prices`, `json_device`) con esquemas internos de objetos y valores de muestra.
* **⚙️ Filtros Excluyentes en Cascada:** Selección dinámica y enlazada de fuentes de datos (`clickhouse`, `mysql-sl`, `bigquery`) que filtra en tiempo real las tablas y columnas disponibles.
* **🎨 Canvas SVG Interactivo:** Diagrama visual de tablas con tarjetas arrastrables (*drag & drop*) y redimensionables. Las líneas de relación entre campos se recalculan fluidamente en tiempo real durante el movimiento.
* **🌐 Matriz de Trazabilidad Transversal:** Mapeo de conexiones y claves de unión inter-fuente (e.g., `publisher`, `bundle`, `ad_unit`) entre diferentes tecnologías de bases de datos.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.11+
* **Framework Interactivo:** [Marimo Notebooks](https://marimo.io/)
* **Compilación WebAssembly (WASM):** Pyodide
* **Procesamiento de Datos:** Pandas, PyArrow
* **Visualización:** HTML5, CSS3, JavaScript (Drag & Drop, ResizeObserver, SVG Dinámico)
* **CI/CD & Deployment:** GitHub Actions + GitHub Pages

---

## 📂 Estructura del Proyecto

```text
tappx-data-model-eda/
├── .github/workflows/
│   └── deploy.yml          # Automation pipeline for GitHub Pages (WASM build)
├── eda_data_model.py       # Main reactive Marimo notebook script
├── merge.py                # CSV schemas unification tool
├── schema_metadata.csv     # Master unified dataset (ClickHouse + MySQL + BigQuery)
├── schema_mysql.csv        # Metadata export from MySQL-SL
├── schema_bigquery.csv     # Metadata export from BigQuery (tappx_us_east4)
├── index.html              # WASM compiled entrypoint
└── README.md               # Project documentation

⚙️ Instalación y Configuración Local
1. Clonar el Repositorio
Bash
git clone [https://github.com/Lucianoavalos/tappx-data-model-eda.git](https://github.com/Lucianoavalos/tappx-data-model-eda.git)
cd tappx-data-model-eda

2. Configurar el Entorno Virtual e Instalar Dependencias
Bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual (Git Bash en Windows)
source .venv/Scripts/activate

# Instalar librerías requeridas
pip install marimo pandas pyarrow

💻 Uso de la Aplicación
Abrir el Explorador en Modo Desarrollo
Bash
.venv/Scripts/marimo edit eda_data_model.py
Unificar Nuevos Esquemas CSV
Bash
.venv/Scripts/python merge.py
Probar el Build WASM Localmente
Bash
.venv/Scripts/marimo export html-wasm eda_data_model.py -o index.html --no-show-code
python -m http.server 8000
👨‍💻 Autor y Contacto
Luciano Ávalos

GitHub: @Lucianoavalos

Demo En Vivo: Tappx Data Model Dashboard

📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

---

### Comando Final Único para Subir Todo a GitHub

Guarda el `README.md` en VSCode y ejecuta esta sola línea en tu terminal de Git Bash:

```bash
git add . && git commit -m "docs: readme actualizado con resumen no tecnico, badges e instrucciones" && git push origin master