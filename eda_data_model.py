import marimo

app = marimo.App(width="full")


# ==========================================
# CELDA BASE: Carga de Datos y Constantes
# ==========================================
@app.cell
def __():
    import hashlib
    import json
    import marimo as mo
    import pandas as pd

    # Carga del catálogo unificado (ClickHouse, MySQL-SL, BigQuery)
    df_schema = pd.read_csv("schema_metadata.csv")
    if "source_type" not in df_schema.columns:
        df_schema["source_type"] = "clickhouse"

    # Mapeo de subcampos para estructuras JSON complejas
    JSON_SCHEMAS_MAP = {
        "ext": {
            "descripcion": "Objeto de extensión OpenRTB / Tappx con metadatos de subasta, cookies y adaptadores de demanda.",
            "subcampos": [
                {"subcampo": "ext.bidder", "tipo": "Object/JSON", "ejemplo": "{'tappx': {'seat': '101'}}", "descripcion": "Parámetros del adaptador de demanda/DSP."},
                {"subcampo": "ext.prebid", "tipo": "Object/JSON", "ejemplo": "{'storedrequest': {'id': 'adunit_1'}}", "descripcion": "Configuración de Prebid Server."},
                {"subcampo": "ext.gpid", "tipo": "String", "ejemplo": "/12345/app_banner_main", "descripcion": "Global Placement ID (GAM/AdServer)."},
                {"subcampo": "ext.schain", "tipo": "Object/JSON", "ejemplo": "{'ver':'1.0','nodes':[{'asi':'tappx.com'}]}", "descripcion": "SupplyChain validation (ads.txt / sellers.json)."},
                {"subcampo": "ext.consents", "tipo": "Object/JSON", "ejemplo": "{'gdpr': 1, 'consent_string': 'CP123...'}", "descripcion": "Cadenas de consentimiento TCFv2 / CCPA."}
            ]
        },
        "json_data": {
            "descripcion": "Payload crudo con metadatos completos de la solicitud (device, geo, imp).",
            "subcampos": [
                {"subcampo": "json_data.device.ip", "tipo": "String", "ejemplo": "185.12.34.5", "descripcion": "IP de origen del dispositivo."},
                {"subcampo": "json_data.device.ua", "tipo": "String", "ejemplo": "Mozilla/5.0 (iPhone...)", "descripcion": "User-Agent del navegador o app."},
                {"subcampo": "json_data.device.ifa", "tipo": "String", "ejemplo": "EA7583CD-A667-48BC-B806-42ECB2B48D12", "descripcion": "Identificador publicitario (IDFA / GAID)."},
                {"subcampo": "json_data.imp[].banner.w", "tipo": "Int", "ejemplo": "320", "descripcion": "Ancho del banner en píxeles."},
                {"subcampo": "json_data.imp[].banner.h", "tipo": "Int", "ejemplo": "50", "descripcion": "Alto del banner en píxeles."}
            ]
        },
        "json_prices": {
            "descripcion": "Desglose financiero completo de la subasta (Floor prices, net bids, márgenes y comisiones).",
            "subcampos": [
                {"subcampo": "json_prices.price_request_publisher", "tipo": "Decimal", "ejemplo": "0.4500", "descripcion": "Floor price mínimo exigido por el publisher."},
                {"subcampo": "json_prices.price_request_network", "tipo": "Decimal", "ejemplo": "0.6000", "descripcion": "Floor price ajustado enviado al DSP/Red."},
                {"subcampo": "json_prices.price_response_network_net", "tipo": "Decimal", "ejemplo": "1.2000", "descripcion": "Precio neto devuelto por la red ganadora."},
                {"subcampo": "json_prices.price_response_publisher", "tipo": "Decimal", "ejemplo": "0.9500", "descripcion": "Precio final pagado al publisher."},
                {"subcampo": "json_prices.margen_base", "tipo": "Decimal", "ejemplo": "0.1500", "descripcion": "Margen de beneficio retenido por Tappx."}
            ]
        },
        "json_price": {
            "descripcion": "Variante del desglose financiero de subasta.",
            "subcampos": [
                {"subcampo": "json_price.price_request_publisher", "tipo": "Decimal", "ejemplo": "0.4500", "descripcion": "Floor price mínimo del publisher."},
                {"subcampo": "json_price.price_response_network_net", "tipo": "Decimal", "ejemplo": "1.2000", "descripcion": "Puja neta devuelta por la red."}
            ]
        },
        "json_device": {
            "descripcion": "Atributos técnicos del dispositivo cliente.",
            "subcampos": [
                {"subcampo": "json_device.ip", "tipo": "String", "ejemplo": "185.12.34.5", "descripcion": "IP pública del usuario."},
                {"subcampo": "json_device.ua", "tipo": "String", "ejemplo": "Mozilla/5.0 (Android...)", "descripcion": "User-Agent completo."},
                {"subcampo": "json_device.ifa", "tipo": "String", "ejemplo": "EA7583CD-A667...", "descripcion": "IDFA / GAID / AAID."},
                {"subcampo": "json_device.os", "tipo": "String", "ejemplo": "android", "descripcion": "Sistema operativo detectado."}
            ]
        }
    }

    SAMPLE_VALUES_MAP = {
        "json_data": "JSON: {'id': 'req_981', 'imp': [{'id': '1', 'banner': {'w': 320, 'h': 50}}]}",
        "json_prices": "JSON: {'price_request_publisher': 0.45, 'price_request_network': 0.60, 'price_response_network_net': 1.20, 'price_response_publisher': 0.95}",
        "json_price": "JSON: {'price_request_publisher': 0.45, 'price_request_network': 0.60, 'price_response_network_net': 1.20, 'price_response_publisher': 0.95}",
        "json_device": "JSON: {'ip': '185.12.34.5', 'ua': 'Mozilla/5.0...', 'ifa': 'EA7583CD-A667-48BC-B806-42ECB2B48D12', 'os': 'android'}",
        "json_extra": "JSON: {'app_version': '2.1.0', 'sdk_version': 'Tappx_4.2', 'schain': {'ver':'1.0'}}",
        "json_qa": "JSON: {'qa_status': 'passed', 'latency_ms': 42, 'fraud_score': 0.01}",
        "json_cache": "JSON: {'cache_id': 'c_98123', 'ttl': 300, 'stored_price': 0.85}",
        "delivery_json_data": "JSON: {'adm': '<script...>','nurl': 'https://tappx.com/win'}",
        "delivery_json_cache": "JSON: {'cached_at': '2026-09-25 12:00:00', 'status': 'valid'}",
        "ext": "JSON: {'bidder': {'tappx': {'seat': '101'}}, 'gpid': '/1234/banner', 'schain': {'ver':'1.0'}}",
        "extra": "JSON: {'internal_tag': 'test_group_a'}",
        "publisher": "'pub_9812', 'tappx_direct_102', 'app_publisher_55'",
        "ad_unit": "'interstitial_bottom', 'banner_top_300x250', 'rewarded_video_1'",
        "adunit": "'interstitial_bottom', 'banner_top_300x250', 'rewarded_video_1'",
        "bundle": "'com.game.racing3d', 'com.news.portal', 'id123456789'",
        "country": "'ES', 'US', 'DE', 'FR', 'BR', 'MX'",
        "ad_size": "'300x250', '320x50', '728x90', '1920x1080'",
        "network": "'net_pubmatic', 'net_rubicon', 'net_applovin', 'bidder_internal'",
        "device_os": "'android', 'ios', 'windows', 'tizen', 'webos'"
    }

    mo.md("# 📊 Explorador Multi-Fuente del Modelo de Datos - Tappx")
    return (
        JSON_SCHEMAS_MAP,
        SAMPLE_VALUES_MAP,
        df_schema,
        hashlib,
        json,
        mo,
        pd,
    )


# ==========================================================
# BLOQUE 1: Filtro de Fuente
# ==========================================================
@app.cell
def __(df_schema, mo):
    motores_disponibles = sorted(df_schema["source_type"].dropna().unique().tolist())

    filtro_fuente_b1 = mo.ui.multiselect(
        options=motores_disponibles,
        value=motores_disponibles,
        label="🗄️ Paso 1: Selecciona las Fuentes de Datos (ClickHouse / MySQL-SL / BigQuery):"
    )

    mo.vstack([
        mo.md("## 1️⃣ Bloque de Inspección de Campos Multi-Fuente"),
        filtro_fuente_b1
    ])
    return filtro_fuente_b1, motores_disponibles


# ==========================================================
# BLOQUE 1: Filtro Excluyente de Campos en Cascada
# ==========================================================
@app.cell
def __(df_schema, filtro_fuente_b1, mo):
    fuentes_activas = filtro_fuente_b1.value
    campos_excluyentes = sorted(
        df_schema[df_schema["source_type"].isin(fuentes_activas)]["column_name"]
        .dropna().unique().tolist()
    )

    filtro_campo = mo.ui.multiselect(
        options=campos_excluyentes,
        value=["json_prices", "publisher"] if "json_prices" in campos_excluyentes and "publisher" in campos_excluyentes else [campos_excluyentes[0]] if campos_excluyentes else [],
        label="🔎 Paso 2: Campos disponibles en las fuentes seleccionadas:"
    )

    filtro_campo
    return campos_excluyentes, filtro_campo, fuentes_activas


# ==========================================================
# BLOQUE 1: Renderizado de Resultados
# ==========================================================
@app.cell
def __(
    JSON_SCHEMAS_MAP,
    SAMPLE_VALUES_MAP,
    df_schema,
    filtro_campo,
    filtro_fuente_b1,
    mo,
):
    campos_seleccionados = filtro_campo.value
    fuentes_seleccionadas = filtro_fuente_b1.value

    if not campos_seleccionados or not fuentes_seleccionadas:
        bloque_1_output = mo.md("⚠️ Selecciona al menos una fuente de datos y un campo para inspeccionar.")
    else:
        df_presencia = df_schema[
            (df_schema["source_type"].isin(fuentes_seleccionadas))
            & (df_schema["column_name"].isin(campos_seleccionados))
        ][
            ["source_type", "column_name", "database_name", "table_name", "data_type", "column_key"]
        ].drop_duplicates().sort_values(by=["source_type", "column_name", "database_name", "table_name"])

        df_presencia["Valores de Muestra"] = df_presencia["column_name"].apply(
            lambda col: SAMPLE_VALUES_MAP.get(
                str(col).lower(), 
                f"Valores alfanuméricos / numéricos estándar de '{col}'"
            )
        )

        df_presencia.columns = ["Fuente (Engine)", "Campo", "Base de Datos / Dataset", "Tabla", "Tipo de Dato", "Key", "Valores de Muestra"]

        json_html_list = []
        for c_sel in campos_seleccionados:
            json_info = JSON_SCHEMAS_MAP.get(str(c_sel).lower(), None)
            if json_info:
                filas = ""
                for s in json_info["subcampos"]:
                    filas += f"""
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 6px 10px; font-weight: bold; color: #1E293B;">{s['subcampo']}</td>
                        <td style="padding: 6px 10px; color: #0284C7; font-family: monospace;">{s['tipo']}</td>
                        <td style="padding: 6px 10px; color: #475569; font-family: monospace; font-size: 11px;">{s['ejemplo']}</td>
                        <td style="padding: 6px 10px; color: #334155;">{s['descripcion']}</td>
                    </tr>
                    """
                json_card = f"""
                <div style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 12px; margin-top: 15px;">
                    <h4 style="color: #0369A1; margin-bottom: 6px;">📦 Estructura Interna del Campo JSON: <code>{c_sel}</code></h4>
                    <p style="font-size: 12px; color: #0C4A6E; margin-bottom: 10px;">{json_info['descripcion']}</p>
                    <table style="width: 100%; border-collapse: collapse; font-size: 12px; background: white; border-radius: 6px; overflow: hidden;">
                        <thead>
                            <tr style="background-color: #E0F2FE; text-align: left; color: #0369A1;">
                                <th style="padding: 8px 10px;">Subcampo</th>
                                <th style="padding: 8px 10px;">Tipo</th>
                                <th style="padding: 8px 10px;">Ejemplo</th>
                                <th style="padding: 8px 10px;">Descripción</th>
                            </tr>
                        </thead>
                        <tbody>{filas}</tbody>
                    </table>
                </div>
                """
                json_html_list.append(mo.Html(json_card))

        bloque_1_output = mo.vstack([
            mo.md(f"### 🎯 Coincidencias ({len(df_presencia)} registros en {', '.join(fuentes_seleccionadas)}):"),
            mo.ui.table(df_presencia),
            *json_html_list,
            mo.md("---")
        ])

    bloque_1_output
    return (
        bloque_1_output,
        c_sel,
        campos_seleccionados,
        df_presencia,
        filas,
        fuentes_seleccionadas,
        json_card,
        json_html_list,
        json_info,
    )


# ==========================================================
# BLOQUE 2: Controles Excluyentes para Canvas
# ==========================================================
@app.cell
def __(df_schema, mo):
    mo.md("## 2️⃣ Bloque de Diagrama de Arquitectura Inter-Fuente")
    
    fuentes_canvas_disponibles = sorted(df_schema["source_type"].dropna().unique().tolist())
    
    filtro_fuente_b2 = mo.ui.multiselect(
        options=fuentes_canvas_disponibles,
        value=fuentes_canvas_disponibles,
        label="⚙️ Paso 1: Selecciona las Fuentes para el Canvas:"
    )

    filtro_fuente_b2
    return filtro_fuente_b2, fuentes_canvas_disponibles


@app.cell
def __(df_schema, filtro_fuente_b2, mo):
    df_fuentes_diagrama = df_schema[
        df_schema["source_type"].isin(filtro_fuente_b2.value)
    ].copy()
    
    tablas_excluyentes_diagrama = sorted(
        (df_fuentes_diagrama["source_type"] + " :: " + df_fuentes_diagrama["database_name"] + "." + df_fuentes_diagrama["table_name"])
        .unique().tolist()
    )

    filtro_tablas_diagrama = mo.ui.multiselect(
        options=tablas_excluyentes_diagrama,
        value=tablas_excluyentes_diagrama[:6] if len(tablas_excluyentes_diagrama) >= 6 else tablas_excluyentes_diagrama,
        label="📌 Paso 2: Tablas / Datasets disponibles en las fuentes seleccionadas:"
    )

    filtro_tablas_diagrama
    return df_fuentes_diagrama, filtro_tablas_diagrama, tablas_excluyentes_diagrama


# ==========================================================
# BLOQUE 2: Canvas SVG Interactivo
# ==========================================================
@app.cell
def __(
    df_schema,
    filtro_fuente_b2,
    filtro_tablas_diagrama,
    hashlib,
    json,
    mo,
    pd,
):
    if not filtro_tablas_diagrama.value or not filtro_fuente_b2.value:
        bloque_2_output = mo.md("⚠️ Selecciona al menos una fuente y una tabla para renderizar el diagrama.")
    else:
        tablas_seleccionadas_str = filtro_tablas_diagrama.value
        
        df_canvas_list = []
        for item in tablas_seleccionadas_str:
            parts = item.split(" :: ")
            s_type = parts[0]
            db_tb = parts[1].split(".")
            db_n = db_tb[0]
            tb_n = db_tb[1]
            
            sub = df_schema[
                (df_schema["source_type"] == s_type) &
                (df_schema["database_name"] == db_n) &
                (df_schema["table_name"] == tb_n)
            ]
            df_canvas_list.append(sub)

        df_canvas = pd.concat(df_canvas_list, ignore_index=True) if df_canvas_list else pd.DataFrame()

        conteo_cols = df_canvas["column_name"].value_counts()
        cols_compartidas = conteo_cols[conteo_cols > 1].index.tolist()

        PALETA = [
            {"bg": "#FEF08A", "text": "#854D0E", "border": "#FACC15"},
            {"bg": "#BFDBFE", "text": "#1E40AF", "border": "#60A5FA"},
            {"bg": "#BBF7D0", "text": "#166534", "border": "#4ADE80"},
            {"bg": "#FBCFE8", "text": "#9D174D", "border": "#F472B6"},
            {"bg": "#DDD6FE", "text": "#5B21B6", "border": "#A78BFA"},
            {"bg": "#FED7AA", "text": "#9A3412", "border": "#FB923C"},
            {"bg": "#CCFBF1", "text": "#115E59", "border": "#2DD4BF"},
            {"bg": "#E2E8F0", "text": "#334155", "border": "#94A3B8"},
        ]

        def obtener_color(col):
            if col not in cols_compartidas:
                return {"bg": "#FFFFFF", "text": "#1F2937", "border": "transparent"}
            idx = int(hashlib.md5(col.encode("utf-8")).hexdigest(), 16) % len(PALETA)
            return PALETA[idx]

        tables_payload = []
        grid_cols = 3
        spacing_x = 360
        spacing_y = 380

        for idx, ((stype, capa, tabla), grp) in enumerate(df_canvas.groupby(["source_type", "database_name", "table_name"])):
            t_id = f"{stype}__{capa}__{tabla}"
            pos_x = 40 + (idx % grid_cols) * spacing_x
            pos_y = 40 + (idx // grid_cols) * spacing_y

            cols_data = []
            for _, row in grp.iterrows():
                c_name = str(row["column_name"])
                c_type = (
                    str(row["data_type"])
                    .replace("LowCardinality(", "")
                    .replace("Nullable(", "")
                    .replace(")", "")
                )
                is_pk = str(row.get("column_key", "")).upper() == "PRI"
                c_style = obtener_color(c_name)

                cols_data.append({
                    "name": c_name,
                    "type": c_type,
                    "is_pk": is_pk,
                    "is_shared": c_name in cols_compartidas,
                    "bg": c_style["bg"],
                    "text": c_style["text"],
                    "border": c_style["border"],
                })

            tables_payload.append({
                "id": t_id,
                "engine": str(stype).lower().replace(".", "_"),
                "engine_label": str(stype),
                "layer": capa.lower(),
                "name": tabla,
                "x": pos_x,
                "y": pos_y,
                "columns": cols_data,
            })

        connections = []
        drawn_pairs = set()
        for i in range(len(tables_payload)):
            t1 = tables_payload[i]
            c1 = {c["name"]: c for c in t1["columns"]}

            for j in range(i + 1, len(tables_payload)):
                t2 = tables_payload[j]
                c2 = {c["name"]: c for c in t2["columns"]}

                comunes = set(c1.keys()).intersection(set(c2.keys())).intersection(cols_compartidas)
                claves_prioritarias = [
                    "publisher", "ad_unit", "adunit", "bundle", "country", "size",
                    "network", "app", "id", "user"
                ]
                comunes_ordenados = sorted(
                    list(comunes),
                    key=lambda x: any(k in x.lower() for k in claves_prioritarias),
                    reverse=True,
                )

                for campo in comunes_ordenados:
                    pair_key = tuple(sorted([f"{t1['id']}:{campo}", f"{t2['id']}:{campo}"]))
                    if pair_key not in drawn_pairs:
                        drawn_pairs.add(pair_key)
                        style = obtener_color(campo)
                        connections.append({
                            "from_table": t1["id"],
                            "to_table": t2["id"],
                            "field": campo,
                            "color": style["border"],
                        })

        html_canvas = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    background-color: #F8FAFC;
                    overflow: auto;
                    height: 100vh;
                    position: relative;
                }}
                #board {{
                    position: relative;
                    min-width: 1600px;
                    min-height: 1000px;
                    padding: 20px;
                }}
                svg#connections {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 1;
                }}
                .table-card {{
                    position: absolute;
                    width: 320px;
                    min-width: 220px;
                    min-height: 130px;
                    background: #FFFFFF;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
                    border: 1px solid #E2E8F0;
                    z-index: 2;
                    cursor: grab;
                    resize: both;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }}
                .table-card:active {{ cursor: grabbing; z-index: 10; }}
                .card-header {{
                    padding: 10px 12px;
                    color: #FFFFFF;
                    font-weight: 700;
                    font-size: 12px;
                    border-top-left-radius: 7px;
                    border-top-right-radius: 7px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-shrink: 0;
                }}
                .engine-clickhouse {{ background: #C2410C; }}
                .engine-mysql-sl {{ background: #0284C7; }}
                .engine-bigquery {{ background: #4F46E5; }}
                
                .engine-tag {{
                    font-size: 9px;
                    padding: 2px 6px;
                    border-radius: 4px;
                    background: rgba(255,255,255,0.25);
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                }}
                .col-list {{
                    flex-grow: 1;
                    overflow-y: auto;
                    font-size: 11px;
                }}
                .col-row {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 5px 10px;
                    border-bottom: 1px solid #F1F5F9;
                    transition: background 0.15s;
                }}
                .col-name {{
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                }}
                .pk-pill {{
                    font-size: 8px;
                    background: #FEF08A;
                    color: #854D0E;
                    border: 1px solid #EAB308;
                    border-radius: 3px;
                    padding: 1px 4px;
                    font-weight: 800;
                }}
                .col-type {{
                    font-size: 10px;
                    color: #64748B;
                    font-family: monospace;
                }}
                path.rel-line {{
                    stroke-width: 2.5;
                    fill: none;
                    stroke-dasharray: 4, 3;
                    opacity: 0.75;
                    transition: stroke-width 0.2s, opacity 0.2s;
                }}
                path.rel-line:hover {{
                    stroke-width: 4.5;
                    opacity: 1;
                }}
            </style>
        </head>
        <body>
            <div id="board">
                <svg id="connections"></svg>
                <div id="cards-container"></div>
            </div>

            <script>
                const tables = {json.dumps(tables_payload)};
                const connections = {json.dumps(connections)};
                const board = document.getElementById('board');
                const svg = document.getElementById('connections');
                const container = document.getElementById('cards-container');

                tables.forEach(t => {{
                    const card = document.createElement('div');
                    card.className = 'table-card';
                    card.id = t.id;
                    card.style.left = t.x + 'px';
                    card.style.top = t.y + 'px';

                    let colsHtml = '';
                    t.columns.forEach(c => {{
                        const pkBadge = c.is_pk ? '<span class="pk-pill">🔑 PK</span>' : '';
                        const borderStyle = c.is_shared ? `border-left: 4px solid ${{c.border}}; background-color: ${{c.bg}}; color: ${{c.text}};` : '';
                        colsHtml += `
                            <div class="col-row" id="${{t.id}}__${{c.name}}" style="${{borderStyle}}">
                                <span class="col-name">${{pkBadge}} ${{c.name}}</span>
                                <span class="col-type">${{c.type}}</span>
                            </div>
                        `;
                    }});

                    card.innerHTML = `
                        <div class="card-header engine-${{t.engine}}">
                            <span>${{t.layer}} . ${{t.name}}</span>
                            <span class="engine-tag">${{t.engine_label}}</span>
                        </div>
                        <div class="col-list">${{colsHtml}}</div>
                    `;

                    container.appendChild(card);
                    makeDraggableAndResizable(card);
                }});

                function drawLines() {{
                    svg.innerHTML = '';
                    const boardRect = board.getBoundingClientRect();

                    connections.forEach(conn => {{
                        const el1 = document.getElementById(`${{conn.from_table}}__${{conn.field}}`);
                        const el2 = document.getElementById(`${{conn.to_table}}__${{conn.field}}`);

                        if (el1 && el2) {{
                            const card1 = el1.closest('.table-card');
                            card2 = el2.closest('.table-card');

                            const r1 = el1.getBoundingClientRect();
                            const r2 = el2.getBoundingClientRect();
                            const c1Rect = card1.getBoundingClientRect();
                            const c2Rect = card2.getBoundingClientRect();

                            const isVisible1 = (r1.top >= c1Rect.top) && (r1.bottom <= c1Rect.bottom);
                            const isVisible2 = (r2.top >= c2Rect.top) && (r2.bottom <= c2Rect.bottom);

                            if (isVisible1 && isVisible2) {{
                                const isCard1Left = c1Rect.left < c2Rect.left;

                                const x1 = isCard1Left ? (c1Rect.right - boardRect.left) : (c1Rect.left - boardRect.left);
                                const y1 = (r1.top + r1.bottom) / 2 - boardRect.top;

                                const x2 = isCard1Left ? (c2Rect.left - boardRect.left) : (c2Rect.right - boardRect.left);
                                const y2 = (r2.top + r2.bottom) / 2 - boardRect.top;

                                const dx = Math.min(Math.abs(x2 - x1) * 0.5, 150);
                                const d = `M ${{x1}} ${{y1}} C ${{x1 + (isCard1Left ? dx : -dx)}} ${{y1}}, ${{x2 + (isCard1Left ? -dx : dx)}} ${{y2}}, ${{x2}} ${{y2}}`;

                                const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                                path.setAttribute('d', d);
                                path.setAttribute('class', 'rel-line');
                                path.setAttribute('stroke', conn.color);
                                svg.appendChild(path);
                            }}
                        }}
                    }});
                }}

                function makeDraggableAndResizable(el) {{
                    let isDragging = false;
                    let startX, startY, initX, initY;

                    const resizeObserver = new ResizeObserver(() => {{
                        drawLines();
                    }});
                    resizeObserver.observe(el);

                    el.addEventListener('mousedown', e => {{
                        const rect = el.getBoundingClientRect();
                        const isResizeHandle = (e.clientX > rect.right - 16) && (e.clientY > rect.bottom - 16);
                        
                        if (e.target.closest('.col-list') || isResizeHandle) return;
                        
                        isDragging = true;
                        startX = e.clientX;
                        startY = e.clientY;
                        initX = el.offsetLeft;
                        initY = el.offsetTop;
                        document.addEventListener('mousemove', onMouseMove);
                        document.removeEventListener('mouseup', onMouseUp);
                    }});

                    function onMouseMove(e) {{
                        if (!isDragging) return;
                        el.style.left = (initX + e.clientX - startX) + 'px';
                        el.style.top = (initY + e.clientY - startY) + 'px';
                        drawLines();
                    }}

                    function onMouseUp() {{
                        isDragging = false;
                        document.removeEventListener('mousemove', onMouseMove);
                        document.removeEventListener('mouseup', onMouseUp);
                    }}
                }}

                setTimeout(drawLines, 100);
                window.addEventListener('resize', drawLines);
            </script>
        </body>
        </html>
        """

        bloque_2_output = mo.vstack([
            mo.iframe(html=html_canvas, width="100%", height="750px"),
            mo.md("---")
        ])

    bloque_2_output
    return (
        bloque_2_output,
        cols_compartidas,
        cols_data,
        comunes,
        comunes_ordenados,
        connections,
        conteo_cols,
        db_tb,
        db_n,
        df_canvas,
        df_canvas_list,
        drawn_pairs,
        grid_cols,
        html_canvas,
        idx,
        item,
        obtener_color,
        parts,
        s_type,
        spacing_x,
        spacing_y,
        sub,
        t_id,
        tables_payload,
        tablas_seleccionadas_str,
        tb_n,
    )


# ==========================================================
# SECCIÓN 3: Matriz de Trazabilidad sin Nombres Duplicados
# ==========================================================
@app.cell
def __(df_schema, mo):
    mo.md("## 3️⃣ Sección de Trazabilidad Transversal de Tablas y Fuentes")

    df_agrupado_rel = df_schema.groupby("column_name")["source_type"].nunique()
    claves_inter_fuente = sorted(df_agrupado_rel[df_agrupado_rel > 1].index.tolist())

    filtro_relacion = mo.ui.multiselect(
        options=claves_inter_fuente,
        value=claves_inter_fuente[:5] if len(claves_inter_fuente) >= 5 else claves_inter_fuente,
        label="🔗 Selecciona los campos clave de unión entre Fuentes de Datos:"
    )

    filtro_relacion
    return claves_inter_fuente, df_agrupado_rel, filtro_relacion


@app.cell
def __(df_schema, filtro_relacion, mo, pd):
    campos_rel = filtro_relacion.value

    if not campos_rel:
        bloque_3_output = mo.md("⚠️ Selecciona al menos un campo clave arriba para analizar la matriz de trazabilidad.")
    else:
        df_sub_rel = df_schema[df_schema["column_name"].isin(campos_rel)].copy()

        relaciones_lista = []
        for col_nombre, grp_rel in df_sub_rel.groupby("column_name"):
            tablas_lista = grp_rel[["source_type", "database_name", "table_name", "data_type"]].drop_duplicates().to_dict("records")
            
            for idx_a in range(len(tablas_lista)):
                tab_a = tablas_lista[idx_a]
                for idx_b in range(idx_a + 1, len(tablas_lista)):
                    tab_b = tablas_lista[idx_b]
                    
                    es_inter = "🔀 Inter-Fuente" if tab_a["source_type"] != tab_b["source_type"] else "🏠 Intra-Fuente"
                    
                    relaciones_lista.append({
                        "Campo Clave": col_nombre,
                        "Tipo Cruzado": es_inter,
                        "Fuente A": tab_a["source_type"],
                        "Tabla Origen": f"{tab_a['database_name']}.{tab_a['table_name']}",
                        "Tipo A": tab_a["data_type"],
                        "Fuente B": tab_b["source_type"],
                        "Tabla Destino": f"{tab_b['database_name']}.{tab_b['table_name']}",
                        "Tipo B": tab_b["data_type"]
                    })

        df_relaciones = pd.DataFrame(relaciones_lista)

        bloque_3_output = mo.vstack([
            mo.md(f"### 🌐 Matriz de Mapeo de Relaciones ({len(df_relaciones)} conexiones detectadas)"),
            mo.ui.table(df_relaciones)
        ])

    bloque_3_output
    return (
        bloque_3_output,
        campos_rel,
        col_nombre,
        df_relaciones,
        df_sub_rel,
        es_inter,
        grp_rel,
        idx_a,
        idx_b,
        relaciones_lista,
        tab_a,
        tab_b,
        tablas_lista,
    )


if __name__ == "__main__":
    app.run()